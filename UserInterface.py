from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.download_lock = QCheckBox('Download Status Lock')
        self.download_lock.setChecked(False)

        self.result_log_box = QTextEdit(self)
        self.result_log_box.setReadOnly(True)
        self.result_log_box_label = QLabel("Download Log")

        self.image_object = QPixmap()
        self.preview_image = QLabel("")

        self.title_label = QLabel("Title : ")
        self.title_text = QLabel("")
        self.duration_time_label = QLabel("Duration : ")
        self.duration_time_text = QLabel("")
        self.start_time_label = QLabel("Start Time : ")
        self.start_time_text = QLabel("")
        self.quality_label = QLabel("Quality : ")
        self.quality_text = QLabel("")
        
        self.progress_bar = QProgressBar(self)

        self.input_value_box = QLineEdit(self)
        self.input_value_box_label = QLabel(
            "Input Vod Path (url or ID Number) (1)")

        self.target_folder_display = QLineEdit(self)
        self.target_folder_display.setReadOnly(True)
        self.target_folder_display_label = QLabel(
            "download target folder path")

        self.temp_folder_display = QLineEdit(self)
        self.temp_folder_display.setReadOnly(True)
        self.temp_folder_display_label = QLabel(
            "temp files save folder path")

        self.check_button = QPushButton("Check Vod (C)", self)
        self.start_button = QPushButton("Download Start (F2)", self)
        self.stop_button = QPushButton("Download Stop (Shift + F4)", self)
        self.option_button = QPushButton("Option (F10)", self)

        self.check_button.setMinimumHeight(80)
        self.start_button.setMinimumHeight(80)
        self.stop_button.setMinimumHeight(80)
        self.option_button.setMinimumHeight(80)

        layout = QVBoxLayout()

        # detailed information box
        infomation_box = QGridLayout()
        infomation_box.addWidget(self.title_label, 0, 0)
        infomation_box.addWidget(self.duration_time_label, 1, 0)
        infomation_box.addWidget(self.start_time_label, 2, 0)
        infomation_box.addWidget(self.quality_label, 3, 0)

        infomation_box.addWidget(self.title_text, 0, 1)
        infomation_box.addWidget(self.duration_time_text, 1, 1)
        infomation_box.addWidget(self.start_time_text, 2, 1)
        infomation_box.addWidget(self.quality_text, 3, 1)

        # preview image + detailed information layout
        merged_infomation_box = QHBoxLayout()
        merged_infomation_box.addWidget(self.preview_image)
        merged_infomation_box.addLayout(infomation_box)

        # input box
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_value_box_label)
        input_layout.addWidget(self.input_value_box)

        # folder path display box
        folder_display_layout = QGridLayout()
        folder_display_layout.addWidget(self.target_folder_display_label, 0, 0)
        folder_display_layout.addWidget(self.target_folder_display, 1, 0)

        folder_display_layout.addWidget(self.temp_folder_display_label, 0, 1)
        folder_display_layout.addWidget(self.temp_folder_display, 1, 1)

        # button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.check_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.option_button)

        # set layout
        layout.addWidget(self.download_lock)
        layout.addWidget(self.result_log_box_label)
        layout.addWidget(self.result_log_box)
        layout.addLayout(merged_infomation_box)
        layout.addWidget(self.progress_bar)
        layout.addLayout(input_layout)
        layout.addLayout(folder_display_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
