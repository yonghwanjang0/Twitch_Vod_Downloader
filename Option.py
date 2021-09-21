from PyQt5.QtWidgets import *


class OptionDialog(QDialog):
    def __init__(self, option_data:list, parent=None):
        super().__init__(parent)

        self.temp_path = option_data[0]
        self.target_path = option_data[1]

        self.target_path_label = QLabel("Save Path")
        self.temp_path_label = QLabel("Temporary Files Save Path")

        self.target_path_box = QLineEdit(self)
        self.target_path_box.setReadOnly(True)
        self.target_path_box.setText(self.target_path)
        self.target_path_box.setMinimumWidth(500)

        self.target_path_button = QPushButton("change", self)

        self.temp_path_box = QLineEdit(self)
        self.temp_path_box.setReadOnly(True)
        self.temp_path_box.setText(self.temp_path)
        self.temp_path_box.setMinimumWidth(500)

        self.temp_path_button = QPushButton("change", self)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow(self.target_path_label)
        layout.addRow(self.target_path_box, self.target_path_button)
        layout.addRow(self.temp_path_label)
        layout.addRow(self.temp_path_box, self.temp_path_button)
        layout.addRow(button_box)

        self.target_path_button.clicked.connect(self.change_target_path)
        self.temp_path_button.clicked.connect(self.change_temp_path)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def change_temp_path(self):
        self.change_path("Temp")

    def change_target_path(self):
        self.change_path("Target")

    def change_path(self, option):
        path = QFileDialog.getExistingDirectory(self)
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
