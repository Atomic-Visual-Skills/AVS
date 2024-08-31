from .ModelInterface import ModelInterface

def load_model(model, size=None, *args, **kwargs):
    if model == 'gpt-4o':
        from .GPT_4o import GPT_4o
        return GPT_4o('gpt-4o', *args, **kwargs)
    elif model == 'llava':
        from .LLaVA import LLaVA
        if size == None:
            raise ValueError('Enter the model size for the LLaVA-NEXT model.')
        elif size in ['7b', '7B', '7']:
            return LLaVA('llava-hf/llava-v1.6-vicuna-7b-hf', *args, **kwargs)
        elif size in ['13b', '13B', '13']:
            return LLaVA('llava-hf/llava-v1.6-vicuna-13b-hf', *args, **kwargs)
        elif size in ['72b', '72B', '72']:
            return LLaVA('llava-hf/llava-next-72b-hf', *args, **kwargs)
        elif size in ['110b', '110B', '110']:
            return LLaVA('llava-hf/llava-next-110b-hf', *args, **kwargs)
        else:
            raise ValueError(f'Size {size} doesn\'t exist. Choose the size from [7b, 13b, 72b, 110b]')
    elif model == 'llava-ov':
        from .LLaVA_OneVision import LLaVA_OneVision
        return LLaVA_OneVision(*args, **kwargs)
    elif model == 'mllava':
        from .Math_LLaVA import Math_LLaVA
        return Math_LLaVA('Zhiqiang007/Math-LLaVA', *args, **kwargs)
    elif model == 'intern-vl':
        from .InternVL import InternVL
        if size == None:
            raise ValueError('Enter the model size for the InternVL model.')
        elif size in ['1b', '1B', '1']:
            return InternVL('OpenGVLab/InternVL2-1B')
        elif size in ['2b', '2B', '2']:
            return InternVL('OpenGVLab/InternVL2-2B')
        elif size in ['4b', '4B', '4']:
            return InternVL('OpenGVLab/InternVL2-4B')
        elif size in ['8b', '8B', '8']:
            return InternVL('OpenGVLab/InternVL2-8B')
        elif size in ['26b', '26B', '26']:
            return InternVL('OpenGVLab/InternVL2-26B')
        elif size in ['40b', '40B', '40']:
            return InternVL('OpenGVLab/InternVL2-40B')
        elif size in ['76b', '76B', '76']:
            return InternVL('OpenGVLab/InternVL2-76B')
        else:
            raise ValueError(f'Size {size} doesn\'t exist. Choose the size from [1b, 2b, 4b, 8b, 26b, 40b, 76b]')
    elif model == 'phi':
        from .Phi import Phi
        return Phi('microsoft/Phi-3.5-vision-instruct', *args, **kwargs)
    elif model == 'deepseek-vl':
        from .DeepSeek_VL import DeepSeek_VL
        if size == None:
            raise ValueError('Enter the model size for the DeepSeek-VL model.')
        elif size in ['1.3b', '1.3B', '1.3']:
            return DeepSeek_VL('deepseek-ai/deepseek-vl-1.3b-chat')
        elif size in ['7b', '7B', '7']:
            return DeepSeek_VL('deepseek-ai/deepseek-vl-7b-chat')
        else:
            raise ValueError(f'Size {size} doesn\'t exist. Choose the size from [1.3b, 7b]')
    else:
        raise ValueError('Unknown model name')

__all__ = ['ModelInterface', 'load_model']