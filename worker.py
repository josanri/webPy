import PIL

from pathlib import Path
from PIL import Image

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot

class WorkerSignals(QObject):
    result = pyqtSignal(list)

class Worker(QRunnable):

    def __init__(self, filenames, **kwargs):
        super(Worker, self).__init__()
        self.filenames = filenames
        self.options = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        result = self.process_files()
        self.signals.result.emit(result)

    def process_files(self):
        unprocessed_files = []
        for filename in set(self.filenames):
            try:
                input_file = Path(filename)
                output_file = input_file.with_suffix(".webp")
                if self.options["overwrite"] or not output_file.exists():
                    self.convert_to_webp(filename, output_file)
            except (PIL.UnidentifiedImageError, FileNotFoundError):
                unprocessed_files.add(filename)
        return unprocessed_files

    def convert_to_webp(self, input_file, output_file) -> str:
        """
        Convert image to webp format.
        """
        image = Image.open(input_file)
        
        image.save(output_file, format="webp",
                    quality=self.options["quality"],
                    loseless=self.options["loseless"]
        )
        return output_file.name