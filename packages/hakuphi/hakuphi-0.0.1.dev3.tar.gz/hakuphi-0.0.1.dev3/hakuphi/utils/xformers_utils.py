memory_efficient_attention = None
try:
    import xformers
except:
    pass

try:
    from xformers.ops import memory_efficient_attention
    from xformers.ops.fmha import LowerTriangularMask

    XFORMERS_AVAIL = True
except:
    memory_efficient_attention = None
    XFORMERS_AVAIL = False
