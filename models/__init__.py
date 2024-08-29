from .ModelInterface import ModelInterface

def load_model(model, *args, **kwargs):
    if model == 'gpt-4o':
        from .GPT_4o import GPT_4o
        return GPT_4o(*args, **kwargs)
    elif model == 'llava':
        from .LLaVA import LLaVA
        return LLaVA(*args, **kwargs)
    elif model == 'mllava':
        from .Math_LLaVA import Math_LLaVA
        return Math_LLaVA(*args, **kwargs)
    elif model == 'intern-vl':
        from .InternVL import InternVL
        return InternVL(*args, **kwargs)
    elif model == 'phi':
        from .Phi import Phi
        return Phi(*args, **kwargs)
    else:
        raise ValueError('Unknown model name')

__all__ = ['ModelInterface', 'load_model']