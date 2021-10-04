from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from StyleSheet import small_button_style, dialog_style
from Constants import dialog_box_size


class OptionDialog(QDialog):
    def __init__(self, option_data:list, parent=None):
        super().__init__(parent)

        self.setStyleSheet(dialog_style)
        self.setFixedSize(
            dialog_box_size[0], dialog_box_size[1])

        self.file_dialog = QFileDialog()

        self.temp_path = option_data[0]
        self.target_path = option_data[1]

        self.target_path_label = QLabel("Save Path")
        self.temp_path_label = QLabel("Temporary Files Save Path")

        self.target_path_box = QLineEdit(self)
        self.target_path_box.setReadOnly(True)
        self.target_path_box.setText(self.target_path)
        self.target_path_box.setMinimumWidth(500)

        self.target_path_button = QPushButton("change", self)
        self.target_path_button.setFixedSize(60, 20)
        self.target_path_button.setStyleSheet(small_button_style)

        self.temp_path_box = QLineEdit(self)
        self.temp_path_box.setReadOnly(True)
        self.temp_path_box.setText(self.temp_path)
        self.temp_path_box.setMinimumWidth(500)

        self.temp_path_button = QPushButton("change", self)
        self.temp_path_button.setFixedSize(60, 20)
        self.temp_path_button.setStyleSheet(small_button_style)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setFixedSize(80, 20)
        self.ok_button.setStyleSheet(small_button_style)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setFixedSize(80, 20)
        self.cancel_button.setStyleSheet(small_button_style)
        
        self.ok_cancel_button_box = QHBoxLayout()
        self.ok_cancel_button_box.addWidget(self.ok_button)
        self.ok_cancel_button_box.addWidget(self.cancel_button)

        layout = QFormLayout(self)
        layout.addRow(self.target_path_label)
        layout.addRow(self.target_path_box, self.target_path_button)
        layout.addRow(self.temp_path_label)
        layout.addRow(self.temp_path_box, self.temp_path_button)
        layout.addRow(self.ok_cancel_button_box)

        self.target_path_button.clicked.connect(self.change_target_path)
        self.temp_path_button.clicked.connect(self.change_temp_path)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setWindowFlags(Qt.FramelessWindowHint)

    def change_temp_path(self):
        self.change_path("Temp")

    def change_target_path(self):
        self.change_path("Target")

    def change_path(self, option):
        if option == "Temp":
            self.file_dialog.setDirectory(self.temp_path)
        else:
            self.file_dialog.setDirectory(self.target_path)

        path = self.file_dialog.getExistingDirectory()
        if path:
            path = path.replace("/", "\\")
            path = path + "\\"
            if option == "Temp":
                self.temp_path_box.setText(path)
                self.temp_path = path
            else:
                self.target_path_box.setText(path)
                self.target_path = path

    def get_values(self):
        return [self.temp_path, self.target_path]
