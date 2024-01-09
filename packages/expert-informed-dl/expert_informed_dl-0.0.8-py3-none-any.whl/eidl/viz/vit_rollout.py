import torch

import numpy as np

from eidl.Models.ExpertAttentionViT import Attention as ExpertAttentionViTAttention

from timm.models.vision_transformer import VisionTransformer

from eidl.utils.torch_utils import any_image_to_tensor


def rollout(depth, grid_size, attentions, discard_ratio, head_fusion, normalize=True, return_raw_attention=False, *args, **kwargs):
    """

    Parameters
    ----------
    depth
    grid_size
    attentions
    discard_ratio
    head_fusion
    return_raw_attention: if false, the classification token's attention will be normalized and returned as a mask
                          if true, the raw attention will be returned
    normalize: if true, the attention will be normalized by dividing by the maximum attention
    args
    kwargs

    Returns
    -------

    """
    result = torch.eye(attentions[0].size(-1))
    with torch.no_grad():
        for i, attention in enumerate(attentions):
            if head_fusion == "mean":
                attention_heads_fused = attention.mean(axis=1)
            elif head_fusion == "max":
                attention_heads_fused = attention.max(axis=1)[0]
            elif head_fusion == "min":
                attention_heads_fused = attention.min(axis=1)[0]
            else:
                raise "Attention head fusion type Not supported"

            # Drop the lowest attentions, but
            # don't drop the class token
            flat = attention_heads_fused.view(attention_heads_fused.size(0), -1)
            _, indices = flat.topk(int(flat.size(-1) * discard_ratio), -1, False)
            indices = indices[indices != 0]
            flat[0, indices] = 0

            I = torch.eye(attention_heads_fused.size(-2), attention_heads_fused.size(-1))  # TODO check why this is not square for ExpertAttentionModel
            a = (attention_heads_fused + 1.0 * I) / 2
            a = a / a.sum(dim=-1)

            result = torch.matmul(a, result)
            if i == depth:
                break

    if not return_raw_attention:
        result = result[0, 0, 1:]  # Look at the total attention between the class token, # and the image patches
    else:
        result = result[0]
    if normalize:
        result = result / torch.max(result)
    return result.numpy()

class VITAttentionRollout:
    def __init__(self, model, device, attention_layer_name='attn_drop', head_fusion="mean",
                 discard_ratio=0.9, *args, **kwargs):
        """


        Parameters
        ----------
        model
        device
        attention_layer_name
        head_fusion
        discard_ratio: discard the bottom x% of the attention
        args
        kwargs
        """
        self.model = model
        self.device = device
        self.head_fusion = head_fusion
        self.discard_ratio = discard_ratio

        self.attention_layer_count = 0
        for name, module in self.model.named_modules():
            if attention_layer_name in name or isinstance(module, ExpertAttentionViTAttention):
                module.register_forward_hook(self.get_attention)
                self.attention_layer_count += 1
        if self.attention_layer_count == 0:
            raise ValueError("No attention layer in the given model")
        if self.attention_layer_count != self.model.depth:
            raise ValueError(f"Model depth ({self.model.depth}) does not match attention layer count {self.attention_layer_count}")
        self.attentions = []

    def get_attention(self, module, input, output):
        if isinstance(module, ExpertAttentionViTAttention):
            # attention_output = rearrange(output[0], 'b n (h d) -> b h n d', h=1)  # TODO remove the hardcoding num heads
            attention_output = output[1]
        else:
            attention_output = output
        self.attentions.append(attention_output.cpu())

    def __call__(self, depth, in_data, *args, **kwargs):
        if depth > self.attention_layer_count:
            raise ValueError(f"Given depth ({depth}) is greater than the number of attenion layers in the model ({self.attention_layer_count})")
        self.attentions = []

        output = self.model(in_data, *args, **kwargs)
        # if isinstance(self.model, VisionTransformer):
        #     output = self.model(in_data)
        # elif fix_sequence is not None:
        #
        # else:
        #     output = self.model(in_data)
        # with torch.no_grad():
        #     if isinstance(self.model, ViT_LSTM):
        #         x = self.model.to_patch_embedding(input_tensor.to(self.device))
        #         b, n, _ = x.shape
        #
        #         cls_tokens = repeat(self.model.cls_token, '1 1 d -> b 1 d', b=b)
        #         x = torch.cat((cls_tokens, x), dim=1)
        #         x += self.model.pos_embedding[:, :(n + 1)]
        #         x = self.model.dropout(x)
        #
        #         # rollout the call: x, att_matrix = self.transformer(x)
        #         for i, (attn, ff) in enumerate(self.model.transformer.layers):
        #             out, attention = attn(x)
        #             x = out + x
        #             x = ff(x) + x
        #             if i + 1 == layer:
        #                 break
        #         # TODO
        #     elif isinstance(self.model, ExpertTimmVisionTransformer):
        #         x = best_model.vision_transformer.patch_embed(tensor.to(device))
        #         x = best_model.vision_transformer._pos_embed(x)
        #         x = best_model.vision_transformer.norm_pre(x)
        #
        #         for i in range(layer):  # iterate to before the designated layer
        #             x = best_model.vision_transformer.blocks[i](x)
        #
        #         this_attention = best_model.vision_transformer.blocks[
        #             layer].attn  # TODO rewrite to directly retrieve attention activation from the target block, using the ExtensionModel's redefined block
        #         B, N, C = x.shape
        #         qkv = this_attention.attention.qkv(x).reshape(B, N, 3, this_attention.attention.num_heads,
        #                                                       C // this_attention.attention.num_heads).permute(
        #             2, 0, 3, 1, 4)
        #         q, k, v = qkv.unbind(0)
        #
        #         this_q = q[0, head, 1:, channel]
        #         this_k = k[0, head, 1:, channel]
        #         query = torch.sigmoid(this_q).reshape(grid_size).cpu().detach().numpy()
        #         key = torch.sigmoid(this_k).reshape(grid_size).cpu().detach().numpy()
        #
        #         activation = q[:, head, :, channel] * k[:, head, :, channel].T
        #         class_activation = activation[0, 1:].reshape(grid_size).cpu().detach().numpy()
        #     elif isinstance(self.model, VisionTransformer):
        #         output = self.model(input_tensor)

        return rollout(depth, self.model.get_grid_size(), self.attentions, self.discard_ratio, self.head_fusion, *args, **kwargs)