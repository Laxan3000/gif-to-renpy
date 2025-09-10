# GIF to Ren'Py

Split GIF files for use in Ren'Py.

Only distinct frames will be saved (meaning that if a gif reuses the same frame twice, it will only be saved once).

Requires `pillow`:

```shell
pip install pillow
```

## How to use gif_to_renpy.py
1. Save the script anywhere you want;

2. Run with `python gif_to_renpy.py` or double click;

3. Insert the path of the GIF file (relative path is preferred, although an absolute path works as well);

4. Choose the format of the output for Ren'Py:

 - [type anything]: `Animation(frame1, duration, frame2, duration, ...)

 - [type nothing]:

  frame1

  duration

  frame2

  duration

  ...

5. Type something if you want the splitted frames to be saved.

 - Those frames will be saved in the same folder as the GIF file, but in a new folder with the same name of the file.

## How to use gif_to_renpy_gui.py

Requires either `PyQt5` or `PyQt6` to be installed. For the latter, editing the imports of the file is required (some systems may have `PyQt5` installed by default, which do not include some `pillow` methods to convert an `Image` to a `QImage` - but this script will work by saving the image to a `BytesIO` first).

- Simply double click on the .py (may require to have the executable flag activated on Linux distros) and launch the program;

- Select a .GIF file or drag and drop one on top of the window;

- The frames will be visualized and the code to import for Ren'Py will be generated. Once you're satisfied, you can decide if to save the frames separately in a new folder the program will create, or to select a folder yourself.