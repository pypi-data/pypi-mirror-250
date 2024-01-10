# TerminalColor
![Python_Version](https://img.shields.io/pypi/pyversions/terminalcolor?label=Python%20Version&logo=python&logoColor=white&style=flat-square)
![License](https://img.shields.io/github/license/cheongwoli/PythonTerminalTextColor?label=License&logo=github&logoColor=white&style=flat-square)

![Pypi_Version](https://img.shields.io/pypi/v/terminalcolor?logo=pypi&logoColor=white&style=flat-square)
![Pypi_Package](https://img.shields.io/pypi/format/terminalcolor?label=package&logo=pypi&logoColor=white&style=flat-square)

> TerminalColor is used to change the color of the text displayed on the Python terminal.

-----

#### Brightnesses(3/4bit) and Bit modes(8bit, 24bit)
- dark
- light

- 8bit
- 24bit or rgb

#### Colors(3/4bit)
- red
- green
- yellow
- blue
- magenta
- cyan

#### Text Types
- bold
- italic
- underline

-----

3/4bit color mode
> ctext(color="brightness-color_name")

8bit color mode
> ctext(color="8bit-color_code")

24bit color mode
> ctext(color="24bit-r;g;b")

> ctext(color="rgb-r;g;b")

-----

#### Example Code
```python
from terminalcolor import ctext, cprint

"""
ctext
"""

# color
print(ctext(text="example", color="dark-blue"))
# background color
print(ctext(text="example", bg_color="light-blue"))
# single text type
print(ctext(text="example", text_type="bold"))
# multiple text type
print(ctext(text="example", text_type=["italic", "underline"]))

# 8bit color mode
print(ctext(text="example", color="8bit-231"))
# 24bit color mode
print(ctext(text="example", color="24bit-91;92;239"))
print(ctext(text="example", color="rgb-91;92;239"))

"""
cprint
"""

cprint(text="example", color="light-yellow", bg_color="dark-blue", text_type="bold")
```
