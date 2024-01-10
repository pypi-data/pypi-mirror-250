import re
import ast
from itertools import cycle

re_rgba_extract = re.compile('rgb[a]?(.*?)$')


def hex_to_rgba(hex, alpha=1):
    try:
        hex = hex.strip().lower().replace(' ', '')
        if '#' in hex:
            hex = hex.replace('#', '')
            hex = [int(hex[i:i + 2], 16) for i in (0, 2, 4)]
            hex.append(alpha)

        elif 'rgb' in hex:
            hex = re_rgba_extract.findall(hex)[0]
            hex = list(ast.literal_eval(hex))
            if len(hex) == 3:
                hex.append(alpha)
            elif len(hex) == 4:
                hex[3] = alpha

        return f'rgba{tuple(hex)}'
    except:
        return f'rgba{tuple([0, 0, 0, 0])}'


def color_wheel(columns=[]):
    color = ['#2596be', '#9925be', '#be4d25', '#49be25', '#bea925', '#be2540']
    cycled = cycle(color)
    return [next(cycled) for _ in range(len(columns))]
