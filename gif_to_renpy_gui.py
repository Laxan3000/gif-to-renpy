#!/usr/bin/env python3
from io import BytesIO
from pathlib import Path
import sys

from PIL import Image, ImageSequence
#! Rename to PyQt6 if you have that version instead
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class GIFToRenPy(QMainWindow):
    
    def __init__(self, parent=None) -> None:
        super(GIFToRenPy, self).__init__(parent)
        self.gif_path = Path()
        self.max_screen_size = app.primaryScreen().size() # type: ignore
        self.max_frame_columns = 10
        self.min_frames_container_height = self.max_screen_size.height() // 4
        self.max_image_width = self.max_screen_size.width() // self.max_frame_columns
        self.save_in = "png"
        
        gif_input_button = QPushButton("Open GIF file (or drag and drop)")
        gif_input_button.clicked.connect(self.open_file)
        
        self.file_input_label = QLabel("Selected file:")
        self.file_input_label.hide()
        
        self.gif_input_label = QLabel()
        self.gif_input_label.hide()
        
        layout_gif_input = QHBoxLayout()
        layout_gif_input.addWidget(gif_input_button)
        layout_gif_input.addWidget(self.file_input_label)
        layout_gif_input.addWidget(self.gif_input_label)
        
        
        self.layout_frames = QGridLayout()
        self.layout_frames.setSizeConstraint(QLayout.SetMinimumSize) # type: ignore
        
        layout_frames_container = QWidget()
        layout_frames_container.setLayout(self.layout_frames)
        
        scroll_area = QScrollArea()
        scroll_area.setMinimumHeight(self.min_frames_container_height)
        # scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # type: ignore
        scroll_area.setWidget(layout_frames_container)


        copy_text_containers = QGridLayout()
        
        self.image_repeat_checkbox = QCheckBox("Repeat")
        self.image_repeat_checkbox.setChecked(True)
        self.image_repeat_checkbox.toggled.connect(lambda check: self.image_text_area.setText(f"{self.image_text_area.text()}    repeat\n" if check else self.image_text_area.text().removesuffix("    repeat\n")))
        self.image_repeat_checkbox.hide()
        
        layout_image_label = QHBoxLayout()
        layout_image_label.addWidget(QLabel("Image:"))
        layout_image_label.addWidget(self.image_repeat_checkbox)
        
        self.image_text_area = QLabel()
        self.image_text_area.setTextInteractionFlags(Qt.TextSelectableByMouse) # type: ignore
        self.animation_text_area = QLabel()
        self.animation_text_area.setTextInteractionFlags(Qt.TextSelectableByMouse) # type: ignore
        
        image_scroll_area = QScrollArea()
        image_scroll_area.setWidget(self.image_text_area)
        
        animation_scroll_area = QScrollArea()
        animation_scroll_area.setWidget(self.animation_text_area)
        
        self.copy_image_text = QPushButton("Copy to clipboard")
        self.copy_image_text.clicked.connect(lambda: self.copy_to_clipboard(self.image_text_area.text()))
        self.copy_image_text.hide()
        self.copy_animation_text = QPushButton("Copy to clipboard")
        self.copy_animation_text.clicked.connect(lambda: self.copy_to_clipboard(self.animation_text_area.text()))
        self.copy_animation_text.hide()
        
        copy_text_containers.addLayout(layout_image_label, 0, 0)
        copy_text_containers.addWidget(QLabel("Animation:"), 0, 1)
        copy_text_containers.addWidget(image_scroll_area, 1, 0)
        copy_text_containers.addWidget(animation_scroll_area, 1, 1)
        copy_text_containers.addWidget(self.copy_image_text, 2, 0)
        copy_text_containers.addWidget(self.copy_animation_text, 2, 1)


        layout_save_in = QHBoxLayout()
    
        save_in_png_radio = QRadioButton("png")
        save_in_png_radio.setChecked(True)
        save_in_gif_radio = QRadioButton("gif")
    
        save_in_group = QButtonGroup(self)
        save_in_group.buttonToggled.connect(self.save_in_button_click)
        save_in_group.addButton(save_in_png_radio)
        save_in_group.addButton(save_in_gif_radio)
        
        layout_save_in.addWidget(QLabel("Save in:"))
        layout_save_in.addWidget(save_in_png_radio)
        layout_save_in.addWidget(save_in_gif_radio)
        
        self.save_auto = QCheckBox()
        self.save_auto.setChecked(True)
        
        save_frames_button = QPushButton("Save Frames")
        save_frames_button.clicked.connect(self.save_frames)
        
        save_frames_layout = QVBoxLayout()
        save_frames_layout.addWidget(self.save_auto)
        save_frames_layout.addWidget(save_frames_button)
    
        layout_footer = QHBoxLayout()
        layout_footer.addLayout(layout_save_in)
        layout_footer.addLayout(save_frames_layout)
        
        self.widget_footer = QWidget()
        self.widget_footer.setLayout(layout_footer)
        self.widget_footer.hide()
        
        
        layout_central = QVBoxLayout()
        layout_central.addLayout(layout_gif_input)
        layout_central.addWidget(QLabel("Separated frames:"))
        layout_central.addWidget(scroll_area)
        layout_central.addLayout(copy_text_containers)
        layout_central.addWidget(self.widget_footer)
    
    
        central_widget = QWidget()
        central_widget.setLayout(layout_central)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("GIF to Ren'Py")
        self.setMaximumSize(self.max_screen_size)
        self.resize(self.max_screen_size / 4)
        self.setAcceptDrops(True)
    
    def open_file(self, file_path=None) -> None:
        if file_path or (file_path := QFileDialog.getOpenFileName(self,
            caption="Select a GIF file",
            directory=sys.path[0],
            filter="GIF file (*.gif)",
        )[0]):
            self.gif_path = Path(file_path)
            self.save_path = self.gif_path.parent / self.gif_path.stem
            self.gif_input_label.setText(file_path)
            
            self.file_input_label.show()
            self.gif_input_label.show()
            
            self.get_frames()
            self.set_text_containers()
            
            self.save_auto.setText(f"Automatically choose saving folder (./{self.gif_path.stem}/)")
            self.image_repeat_checkbox.show()
            self.copy_image_text.show()
            self.copy_animation_text.show()
            self.widget_footer.show()
    
    def save_frames(self) -> None:
        if not self.save_auto.isChecked():
            if not (save_path := QFileDialog.getExistingDirectory(self,
                caption="Select a folder to save the frames in",
                directory=str(self.gif_path.parent)
            )): return
        else:
            if not self.save_path.exists():
                self.save_path.mkdir()
                
            save_path = str(self.save_path)
      
        for i, frame in enumerate(self.unique_frames):
            frame.save(f"{save_path}/{i}.{self.save_in}", format=self.save_in)
            
        QMessageBox.information(self, "Save success", "Frames saved successfully!")

    def get_frames(self):
        self.close_unique_frames()
        
        gif_size, self.gif_frames, self.unique_frames = get_frames(self.gif_path)
        self.show_frames(gif_size)
        
    def show_frames(self, gif_size: tuple[int, int]) -> None:
        self.clear_layout(self.layout_frames)
        
        for i, (pos, duration) in enumerate(self.gif_frames):
            layout_frame = QVBoxLayout()
            
            with BytesIO() as f:
                self.unique_frames[pos].save(f, "PNG")
                f.seek(0)
                
                pixmap = QPixmap.fromImage(QImage.fromData(f.read()))
                
                label = QLabel()
                label.setPixmap(pixmap)
                label.setScaledContents(True)
                label.setFixedSize(QSize(self.max_image_width, (gif_size[1] / gif_size[0] * self.max_image_width).__floor__()))
                label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
                
            image_info = QLabel(f"{pos} - {duration} ms")
            # image_info.setAlignment(Qt.AlignCenter) # type: ignore
            
            layout_frame.addWidget(label, alignment=Qt.AlignCenter) # type: ignore
            layout_frame.addWidget(image_info)
            
            self.layout_frames.addLayout(layout_frame, i // self.max_frame_columns, i % self.max_frame_columns)
    
    def set_text_containers(self) -> None:
        animation_text = "Animation(\n"
        image_text = f"image {self.gif_path.parent.name} {self.gif_path.stem}:\n"
        
        path = f"{self.gif_path.parent.name}/{self.gif_path.stem}"
        for frame in self.gif_frames:
            name: str = f'"{path}/{frame[0]}.{self.save_in}"'
            time: str = str(frame[1] / 1000).removeprefix('0')
            
            animation_text += f"    {name}, {time},\n"
            image_text += f"    {name}\n    {time}\n"
            
        self.animation_text_area.setText(f"{animation_text})")
        self.animation_text_area.adjustSize()
        self.animation_text_area.show()
        self.image_text_area.setText(f"{image_text}    repeat\n")
        self.image_text_area.adjustSize()
        self.image_text_area.show()
    
    def save_in_button_click(self, button: QRadioButton, checked: bool) -> None:
        if not checked:
            return
        
        new_save_in = button.text()
        if self.gif_path:
            self.animation_text_area.setText(self.animation_text_area.text().replace(f".{self.save_in}", f".{new_save_in}"))
            self.animation_text_area.adjustSize()
            self.image_text_area.setText(self.image_text_area.text().replace(f".{self.save_in}", f".{new_save_in}"))
            self.image_text_area.adjustSize()
        self.save_in = new_save_in

    def close_unique_frames(self) -> None:
        if hasattr(self, "unique_frames"):
            for frame in self.unique_frames:
                frame.close()

    @staticmethod
    def copy_to_clipboard(text: str) -> None:
        if cb := QApplication.clipboard():
            cb.clear(mode=cb.Clipboard) # type: ignore
            cb.setText(text, mode=cb.Clipboard) # type: ignore
    
    @staticmethod
    def clear_layout(layout: QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() # type: ignore
            if widget is not None:
                widget.deleteLater()
            else:
                GIFToRenPy.clear_layout(item.layout()) # type: ignore
    
    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        self.close_unique_frames()
    
    def dragEnterEvent(self, event: QDragEnterEvent): # type: ignore
        mimedata = event.mimeData()
        if mimedata and mimedata.hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent): # type: ignore
        self.open_file(event.mimeData().urls()[0].toLocalFile()) # type: ignore
                

def get_frames(gif_path: Path):
    with Image.open(gif_path) as gif:
        gif_size = gif.size
        frames: list[tuple[int, int]] = list()
        unique_frames: dict[bytes, tuple[int, Image.Image]] = dict()
        
        for frame in ImageSequence.Iterator(gif):
            frame_copy: Image.Image = frame.convert("RGBA").copy()
            frame_bytes: bytes = frame_copy.tobytes()
            if frame_bytes not in unique_frames:
                index = len(unique_frames)
                unique_frames[frame_bytes] = (index, frame_copy)
                frames.append((index, frame.info['duration']))
            else:
                frames.append((unique_frames[frame_bytes][0], frame.info['duration']))
                
    return gif_size, frames, list(frame[1] for frame in unique_frames.values())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GIFToRenPy()
    window.show()
    sys.exit(app.exec())