from PIL import Image, ImageSequence
from pathlib import Path

SAVE_IN: str = "gif"
MODE: str    = "RGBA"


if __name__ == "__main__":
    # Ask GIF location and set save path to a new directory with the name of the file
    gif_path: Path = Path(input("Insert the path of the .gif file here: ").replace("'",""))
    save_path: Path = gif_path.parent / gif_path.stem

    # Open the GIF file
    with Image.open(gif_path) as gif:
        # Where the frames are stored like [index from unique_frames, duration]
        frames: list[tuple[int, int]] = list()
        # Where unique frames are stored like {frame_bytes: [index, frame_copy]}
        unique_frames: dict[bytes, tuple[int, Image.Image]] = dict()
        
        for frame in ImageSequence.Iterator(gif):
            # Converting the single frame is somewhat required instead of converting the whole GIF.
            frame_copy: Image.Image = frame.convert(MODE).copy()
            frame_bytes: bytes = frame_copy.tobytes()
            if frame_bytes not in unique_frames:
                index = len(unique_frames)
                unique_frames[frame_bytes] = (index, frame_copy)
                frames.append((index, frame.info['duration']))
            else:
                frames.append((unique_frames[frame_bytes][0], frame.info['duration']))

    # In which format to print the result for Ren'Py
    # Animation: Animation(frame_1, duration, frame2, duration, ...)
    # Image: frame_1 \n duration \n frame2 \n duration ...
    animation: bool = bool(input("Animation? [no]: "))
    if animation: print("Animation(")
    for frame in frames:
        name: str = f'"{save_path / str(frame[0])}.{SAVE_IN}"'
        time: str = str(frame[1] / 1000).removeprefix('0')
        
        print(
            f'    {name}, {time},'
            if animation else
            f'{name}\n{time}'
        )
    if animation: print(')')

    if input("Save frames to memory? [no]: "):
        if not save_path.exists():
            save_path.mkdir()
        
        for i, frame in unique_frames.values():
            frame.save(save_path / f"{i}.{SAVE_IN}")
            frame.close()
