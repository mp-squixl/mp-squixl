## UM SQUiXL example code enhanced

FONTS

The example microptyon code provided by UM, initially at least, only uses the standard framebuffer text font.  
This framebuffer font cannot be changed and its 8x8 pixels.  Its quite miniscule for such a nice large screen. 

An example of using various fonts is shown.  Fonts can be created with the Peter Hinch fonts-to-py library a link to that repository is:
https://github.com/peterhinch/micropython-font-to-py
However there are a number of fonts created with this utility and fonts directory in this repository has a small collection, mainly taken from the Peter Hinch nano-gui repository.  Sometimes the font is not contructed to take all the characters of the alphabet.  For example the arial_70.py font was created just to be able to write numerical characters in a large font.  If an attempt is made to use alphabetical characters that are not contained in the font then a ? character will be displayed.

The example of using fonts is entirely based on the examples provided in the SQUiXL example repository. The SQUiXL_ui.py has been copied, augmented, and renamed to SQIiXL_ui_fonts.py.  Likewise the ui_example.py has updated and called ui_example_fonts.py.

These new example files need to have access to the witer.py file (as found in the font-to-py library, a helper file called colors.py (so one can specify the likes of GREY in place of rgb_to_565(50, 50, 50) or 0xffe0), boolpalette.py (relating to the writer.py), and the aformentioned fonts directory.

There are a number of libraries that can write fonts to the framebuffer and the use of the writer.py has been used as an example.  Some other alternatives can be found in the awesome micropython collection of useful programs:
https://awesome-micropython.com

In particulat the microfont library also utilises the font-to-py fonts thus enabling a large amount of fonts to be accessed. Link is:
https://github.com/antirez/microfont
