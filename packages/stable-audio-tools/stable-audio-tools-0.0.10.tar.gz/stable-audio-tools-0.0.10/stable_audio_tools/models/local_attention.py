import torch

from einops import rearrange
from torch import nn
from local_attention.transformer import LocalMHA, FeedForward

from .adp import Attention
from .blocks import AdaRMSNorm

# Adapted from https://github.com/lucidrains/local-attention/blob/master/local_attention/transformer.py
class ContinuousLocalTransformer(nn.Module):
    def __init__(
        self,
        *,
        dim,
        depth,
        dim_in = None,
        dim_out = None,
        causal = False,
        local_attn_window_size = 64,
        heads = 8,
        ff_mult = 4,
        attn_dropout = 0.,
        ff_dropout = 0.,
        use_conv = True,
        cond_dim = 0,
        cross_attn_cond_dim = 0,
        use_rotary_pos_emb = False,
        **kwargs
    ):
        super().__init__()
        
        dim_head = dim//heads

        qk_scale = dim_head ** 0.5

        self.layers = nn.ModuleList([])

        self.project_in = nn.Linear(dim_in, dim) if dim_in is not None else nn.Identity()

        self.project_out = nn.Linear(dim, dim_out) if dim_out is not None else nn.Identity()

        self.local_attn_window_size = local_attn_window_size

        self.use_conv = use_conv

        self.cond_dim = cond_dim

        self.cross_attn_cond_dim = cross_attn_cond_dim
       
        for _ in range(depth):

            self.layers.append(nn.ModuleList([
                AdaRMSNorm(dim, cond_dim, eps=1e-8) if cond_dim > 0 else nn.LayerNorm(dim, eps=1e-8),
                LocalMHA(
                    dim = dim, 
                    dim_head = dim_head, 
                    heads = heads, 
                    qk_scale=qk_scale, 
                    dropout = attn_dropout, 
                    causal = causal, 
                    window_size = local_attn_window_size, 
                    prenorm = False, 
                    use_rotary_pos_emb = use_rotary_pos_emb,
                    **kwargs),
                Attention(features=dim, num_heads=heads, head_features=dim_head, context_features=self.cross_attn_cond_dim) if self.cross_attn_cond_dim > 0 else nn.Identity(),
                nn.Conv1d(dim, dim, kernel_size=3, padding=1) if use_conv else nn.Identity(),
                FeedForward(dim = dim, mult = ff_mult, dropout = ff_dropout)
            ]))

    def forward(self, x, mask = None, cond = None, cross_attn_cond = None, cross_attn_cond_mask = None, prepend_cond = None):
 
        x = self.project_in(x)

        if prepend_cond is not None:
            x = torch.cat([prepend_cond, x], dim=1)

        for norm, attn, xattn, conv, ff in self.layers:

            if cond is not None:
                x = norm(x, cond)
            else:
                x = norm(x)

            x = attn(x, mask = mask) + x

            if cross_attn_cond is not None:
                x = xattn(x, context=cross_attn_cond, context_mask=cross_attn_cond_mask) + x

            if self.use_conv:
                x = rearrange(x, "b n c -> b c n")
                x = conv(x) + x
                x = rearrange(x, "b c n -> b n c")
                
            x = ff(x) + x

        return self.project_out(x)


class TransformerDownsampleBlock1D(nn.Module):
    def __init__(
        self, 
        in_channels,
        embed_dim = 768,
        depth = 3,
        heads = 12,
        downsample_ratio = 2,
        local_attn_window_size = 64,
        use_conv = True,
        **kwargs
    ):
        super().__init__()

        self.downsample_ratio = downsample_ratio

        self.transformer = ContinuousLocalTransformer(
            dim=embed_dim,
            depth=depth,
            heads=heads,
            local_attn_window_size=local_attn_window_size,
            use_conv=use_conv,
            **kwargs
        )

        self.project_in = nn.Linear(in_channels, embed_dim) if in_channels != embed_dim else nn.Identity()

        self.project_down = nn.Sequential(
            nn.Linear(embed_dim * self.downsample_ratio, embed_dim, bias=False),
            nn.SiLU(),
            nn.Linear(embed_dim, embed_dim, bias=False)
        )
    
    def forward(self, x):

        x = self.project_in(x)

        # Compute
        x = self.transformer(x)

        # Trade sequence length for channels
        x = rearrange(x, "b (n r) c -> b n (c r)", r=self.downsample_ratio)

        # Project back to embed dim
        x = self.project_down(x)

        return x

class TransformerUpsampleBlock1D(nn.Module):
    def __init__(
        self, 
        in_channels,
        embed_dim,
        depth = 3,
        heads = 12,
        upsample_ratio = 2,
        local_attn_window_size = 64,
        use_conv = True,
        **kwargs
    ):
        super().__init__()

        self.upsample_ratio = upsample_ratio

        self.transformer = ContinuousLocalTransformer(
            dim=embed_dim,
            depth=depth,
            heads=heads,
            local_attn_window_size = local_attn_window_size,
            use_conv=use_conv,
            **kwargs
        )

        self.project_in = nn.Linear(in_channels, embed_dim) if in_channels != embed_dim else nn.Identity()

        self.project_up = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * self.upsample_ratio, bias=False),
            nn.SiLU(),
            nn.Linear(embed_dim * self.upsample_ratio, embed_dim * self.upsample_ratio, bias=False)
        )
    

    def forward(self, x):

        # Project to embed dim
        x = self.project_in(x)

        # Project to increase channel dim
        x = self.project_up(x)

        # Trade channels for sequence length
        x = rearrange(x, "b n (c r) -> b (n r) c", r=self.upsample_ratio)

        # Compute
        x = self.transformer(x)        

        return x
   

class TransformerEncoder1D(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        embed_dims = [96, 192, 384, 768],
        heads = [12, 12, 12, 12],
        depths = [3, 3, 3, 3],
        ratios = [2, 2, 2, 2],
        local_attn_window_size = 64,
        use_conv = True,
        **kwargs
    ):
        super().__init__()
        
        layers = []
       
        for layer in range(len(depths)):
            prev_dim = embed_dims[layer - 1] if layer > 0 else embed_dims[0]

            layers.append(
                TransformerDownsampleBlock1D(
                    in_channels = prev_dim,
                    embed_dim = embed_dims[layer],
                    heads = heads[layer],
                    depth = depths[layer],
                    downsample_ratio = ratios[layer],
                    local_attn_window_size = local_attn_window_size,
                    use_conv = use_conv,
                    **kwargs
                )
            )
        
        self.layers = nn.Sequential(*layers)

        self.project_in = nn.Linear(in_channels, embed_dims[0])
        self.project_out = nn.Linear(embed_dims[-1], out_channels)

    def forward(self, x):
        x = rearrange(x, "b c n -> b n c")
        x = self.project_in(x)
        x = self.layers(x)
        x = self.project_out(x)
        x = rearrange(x, "b n c -> b c n")

        return x


class TransformerDecoder1D(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        embed_dims = [768, 384, 192, 96],
        heads = [12, 12, 12, 12],
        depths = [3, 3, 3, 3],
        ratios = [2, 2, 2, 2],
        local_attn_window_size = 64,
        use_conv = True,
        **kwargs
    ):

        super().__init__()

        layers = []
       
        for layer in range(len(depths)):
            prev_dim = embed_dims[layer - 1] if layer > 0 else embed_dims[0]

            layers.append(
                TransformerUpsampleBlock1D(
                    in_channels = prev_dim,
                    embed_dim = embed_dims[layer],
                    heads = heads[layer],
                    depth = depths[layer],
                    upsample_ratio = ratios[layer],
                    local_attn_window_size = local_attn_window_size,
                    use_conv = use_conv,
                    **kwargs
                )
            )
        
        self.layers = nn.Sequential(*layers)

        self.project_in = nn.Linear(in_channels, embed_dims[0])
        self.project_out = nn.Linear(embed_dims[-1], out_channels)

    def forward(self, x):
        x = rearrange(x, "b c n -> b n c")
        x = self.project_in(x)
        x = self.layers(x)
        x = self.project_out(x)
        x = rearrange(x, "b n c -> b c n")
        return x