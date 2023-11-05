import sys
import PIL

from pathlib import Path
from PIL import Image

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QLabel, QWidget, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon

def convert_to_webp(input_filename) -> str:
    """
    Convert image to webp format.
    """
    input_file = Path(input_filename)
    output_file = input_file.with_suffix(".webp")

    image = Image.open(input_file)
    image.save(output_file, format="webp")
    return output_file.name


class UIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        instruction_label = QLabel(
            "<h2>Instructions:</h2>"
            "<ol>"
            "<li>Click the <span style='color: #2D7632; font-weight: bold;'>Select images</span> button to choose the images you want to transform.</li>"
            "<li>The files will be generated next to the original with the '.webp' suffix.</li>"
            "<li>You can also turned all your images inside a folder to webp at the second button.</li>"
            "</ol>"
        )
        instruction_label.setStyleSheet("QLabel { color: #333; }")
        instruction_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(instruction_label)
        
        self.warning_enabled = QCheckBox("Show results at the end.")
        self.warning_enabled.setChecked(True)
        self.layout.addWidget(self.warning_enabled)
        
        select_images_button = QPushButton("Select images in formats like .png, .jpeg or .jpg")
        select_images_button.setStyleSheet("QPushButton { background-color: #7DCE82; color: black; border-radius: 5px; padding: 5px; }")
        select_images_button.clicked.connect(lambda: self.webp_process_files(self.get_files_by_images))
        self.layout.addWidget(select_images_button)

        select_folder_button = QPushButton("Select folder to turn all the images inside to .webp")
        select_folder_button.setStyleSheet("QPushButton { background-color: #2D7632; color: white; border-radius: 5px; padding: 5px; }")
        select_folder_button.clicked.connect(lambda: self.webp_process_files(self.get_files_by_folder))
        self.layout.addWidget(select_folder_button)

        self.central_widget.setLayout(self.layout)


    def webp_process_files(self, file_getter):
        filenames = file_getter()
        if len(filenames) == 0:
            return
        unprocessed_files = set()
        for filename in set(filenames):
            try:
                convert_to_webp(filename)
            except (PIL.UnidentifiedImageError, FileNotFoundError):
                unprocessed_files.add(filename)

        if self.warning_enabled.isChecked():
            msg = QMessageBox()
            if len(unprocessed_files) > 0:
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText(f"Could not process the next file{'s' if len(unprocessed_files) > 1 else ''}:\n{','.join(unprocessed_files)}")
                msg.setWindowTitle("Warning")
            else:
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Files processed without issues.")
                msg.setWindowTitle("Info")
            msg.exec_()

    def get_files_by_images(self) -> [str]:
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filenames, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        return filenames
    
    def get_files_by_folder(self) -> [str]:
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory_folder = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if not directory_folder:
            return []
        extensions = ["png", "jpeg", "jpg"]
        filenames = []

        for ext in extensions:
            filenames.extend(file.resolve() for file in Path(directory_folder).glob(f"**/*.{ext}"))

        return filenames
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")

    window = UIMainWindow()
    window.setWindowTitle("WepPy - A Webp transformer")
    window.setGeometry(100, 100, 300, 200)

    icon = QIcon("assets/favicon.ico.web")
    if len(icon.availableSizes()) == 0:
        icon = QIcon("assets/favicon.ico")
    window.setWindowIcon(icon)

    window.show()
    sys.exit(app.exec_())
