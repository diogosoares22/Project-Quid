def bits_function(module,n_players):
    from math import log2,ceil,floor
    return ceil(log2(module))+floor(log2(n_players))+1


