# GIF to Ren'Py

Split GIF files for use in Ren'Py.

Requires `pillow`:

```shell
pip install pillow
```

## How to use
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