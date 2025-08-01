from einops import rearrange, einsum
import torch
from torch import nn

class Linear(nn.Module):
    """
    Linear Layer

    This implementation:
    - Applies Linear Transformation
    - Does not support bias since modern implementations of transformers does not use it (I might add it later)
    - Initialize weight with Normal distribution with parameters: 
        - mu = 0; std = 2 / (in_features + out_features)
        - clip them (-3 * std, 3 * std)
    
    Args:
        in_features: final dimension of the input
        out_features: final dimension of the output
        device: Device to store the parameters on
        dtype: Data type of the parameters 
    """
    def __init__(self, in_features: int, out_features: int, device: torch.device | None = None, dtype: torch.dtype | None = None):
        super().__init__()
        # initialize data and create linear transformation
        std = 2 / (in_features + out_features)
        data = torch.empty(out_features, in_features, dtype=dtype, device=device)
        nn.init.trunc_normal_(data, mean=0.0, std=std, a=-3.0 * std, b=3.0 * std)
        self.W = nn.Parameter(data)
    
    def forward(self, X: torch.Tensor) -> torch.Tensor:
        assert X.device == self.W.device
        Y = einsum(X, self.W, "... d_in, d_out d_in -> ... d_out")
        return Y

        
class Embedding(nn.Module):
    def __init__(self, num_embeddings, embedding_dim, device=None, dtype=None):
        super().__init__()
        # initialize data and create embedding table
        data = torch.empty(num_embeddings, embedding_dim, dtype=dtype, device=device)
        nn.init.trunc_normal_(data, mean=0.0, std=1.0, a=-3.0, b=3.0)
        self.emb = nn.Parameter(data)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        return self.emb[token_ids]