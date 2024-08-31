from .ModelInterface import ModelInterface

def load_model(model, *args, **kwargs):
    if model == 'gpt-4o':
        from .GPT_4o import GPT_4o
        return GPT_4o(*args, **kwargs)
    elif model == 'llava':
        from .LLaVA import LLaVA
        return LLaVA(*args, **kwargs)
    elif model == 'llava-ov':
        from .LLaVA_OneVision import LLaVA_OneVision
        return LLaVA_OneVision(*args, **kwargs)
    elif model == 'mllava':
        from .Math_LLaVA import Math_LLaVA
        return Math_LLaVA(*args, **kwargs)
    elif model == 'intern-vl':
        from .InternVL import InternVL
        return InternVL(*args, **kwargs)
    elif model == 'phi':
        from .Phi import Phi
        return Phi(*args, **kwargs)
    elif model == 'deepseek-vl':
        from .DeepSeek_VL import DeepSeek_VL
        return DeepSeek_VL(*args, **kwargs)
    else:
        raise ValueError('Unknown model name')

__all__ = ['ModelInterface', 'load_model']