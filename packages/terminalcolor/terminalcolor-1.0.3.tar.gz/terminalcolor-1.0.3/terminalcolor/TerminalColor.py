from enum import Enum
from typing import Any


__all__ = ['ctext', 'cprint']


class ANSIColor(Enum):
    """
    This class is Enum and is the repository for ANSI Color.
    In brightness, F stands for foreground and B stands for background.
    """

    # colors (3/4 bit)
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6

    # brightnesses (3/4 bit)
    DARK_F = 30
    DARK_B = 40
    LIGHT_F = 90
    LIGHT_B = 100

    # text types
    RESET = '0'
    BOLD = '1'
    ITALIC = '3'
    UNDERLINE = '4'


def cprint(text: str, **kwargs: Any):
    """
    :param text: Text parameters can only contain string type values.
    :param kwargs: The kwargs parameter accepts color, bg_color, and text_type values.
    :return: Print colored text.

    This function prints text colored with ctext directly to the terminal using the print function.
    """
    # color
    if 'color' not in kwargs.keys():
        kwargs['color'] = None

    # background color
    if 'bg_color' not in kwargs.keys():
        kwargs['bg_color'] = None

    # text type
    if 'text_type' not in kwargs.keys():
        kwargs['text_type'] = None

    # print color text
    print(
        ctext(
            text=text,
            color=kwargs['color'],
            bg_color=kwargs['bg_color'],
            text_type=kwargs['text_type']
        )
    )


def ctext(text: str, **kwargs: Any) -> str:
    """
    :param text: Text parameters can only contain string type values.
    :param kwargs: The kwargs parameter accepts color, bg_color, and text_type values.
    :return: Returns text with color and text type.

    ex) ctext(text="example", color='dark-green', bg_color='light-yellow', text_type='bold')

    cf. To use multiple text types, enter multiple text types in list format.
    ex) text_type=['bold', 'italic', 'underline']

    cf. To use extended color, enter it in the format 'bit mod-color code'.
    ex) color='(8 or 8Bit)-231', bg_color='(24 or 24Bit or RGB)-91;92;239'
    """
    if kwargs is not None:
        result = ''

        # color (foreground color)
        if ('color' in kwargs.keys()) and (kwargs['color'] is not None):
            result += '\033[{color}m'.format(
                color=convert(color=kwargs['color'])
            )

        # background color
        if ('bg_color' in kwargs.keys()) and (kwargs['bg_color'] is not None):
            result += '\033[{bg_color}m'.format(
                bg_color=convert(color=kwargs['bg_color'], background=True)
            )

        # text type
        if ('text_type' in kwargs.keys()) and (kwargs['text_type'] is not None):
            if type(kwargs['text_type']) is list:
                # multiple text types
                for text_type in kwargs['text_type']:
                    result += '\033[{text_type}m'.format(
                        text_type=ANSIColor[text_type.upper()].value
                    )

            else:
                # single text type
                result += '\033[{text_type}m'.format(
                    text_type=ANSIColor[kwargs['text_type'].upper()].value
                )

        # reset color and text type behind color text
        result += (text + '\033[0m')

        return str(result)

    else:
        raise ValueError('No value entered!')


def convert(color: str, background: bool = False) -> str:
    """
    :param color: It receives color information in the form of "Brightness or Bit Mode-Color".
    :param background: Receive input whether the received color is the background color.
    :return: Converts the input color to ANSI Escape Code and returns it.

    3/4bit Color
    - color_data[0] is the brightness.
    - color_data[1] is the color.

    Extended Color (8bit, 24bit(RGB))
    - color_data[0] is color bit mode.
    - color_data[1] is color code.
    """
    color_data: list = color.upper().split('-')

    # ground
    color_data[0] += '_B' if background is True else '_F'

    # 3/4bit color
    if color_data[0] in ('DARK_F', 'DARK_B', 'LIGHT_F', 'LIGHT_B'):
        color_code = (ANSIColor[color_data[0]].value + ANSIColor[color_data[1]].value)

    # 8bit color
    elif color_data[0] in ('8_F', '8_B', '8BIT_F', '8BIT_B'):
        if background is True:
            color_code = ('48;5;' + color_data[1])

        else:
            color_code = ('38;5;' + color_data[1])

    # 24bit color
    elif color_data[0] in ('24_F', '24_B', '24BIT_F', '24BIT_B', 'RGB_F', 'RGB_B'):
        if background is True:
            color_code = ('48;2;' + color_data[1])

        else:
            color_code = ('38;2;' + color_data[1])

    else:
        raise ValueError('The entered value is not a brightness or a bit mode!')

    return str(color_code)
