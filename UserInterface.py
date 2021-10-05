from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QFont
from StyleSheet import normal_button_style, checkable_button_style


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(600, 800)
        self.download_lock_button = QPushButton(
            'Download Status Lock (Ctrl+Q)', self)
        self.download_lock_button.setFixedSize(200, 40)
        self.download_lock_button.setCheckable(True)
        self.download_lock_button.setStyleSheet(checkable_button_style)

        self.minimized_button = QPushButton("_", self)
        self.minimized_button.setFixedSize(40, 40)
        self.minimized_button.setStyleSheet(normal_button_style)

        self.option_button = QPushButton("Option (F10)", self)
        self.option_button.setFixedSize(80, 40)
        self.option_button.setStyleSheet(normal_button_style)

        self.quit_button = QPushButton("X", self)
        self.quit_button.setFixedSize(40, 40)
        self.quit_button.setStyleSheet(normal_button_style)
                
        self.result_log_box = QTextEdit(self)
        self.result_log_box.setReadOnly(True)

        self.preview_image = QLabel()
        self.title_label = QLabel("Title : ")
        self.title_text = QLabel("")
        self.duration_time_label = QLabel("Duration : ")
        self.duration_time_text = QLabel("")
        self.streamer_label = QLabel("Streamer : ")
        self.streamer_text = QLabel("")
        self.game_label = QLabel("Game : ")
        self.game_text = QLabel("")
        self.start_time_label = QLabel("Start Time : ")
        self.start_time_text = QLabel("")
        self.quality_label = QLabel("Quality : ")
        self.quality_text = QLabel("")
        
        self.progress_bar_status = QLabel("")
        self.progress_bar = QProgressBar(self)

        self.input_value_box = QLineEdit(self)
        self.input_value_box_label = QLabel(
            "Input Vod Path (url or ID Number) (ShortCut : 1)")

        self.target_folder_display = QLineEdit(self)
        self.target_folder_display.setReadOnly(True)
        self.target_folder_display_label = QLabel(
            "File Save Path")

        self.temp_folder_display = QLineEdit(self)
        self.temp_folder_display.setReadOnly(True)
        self.temp_folder_display_label = QLabel(
            "Temporary Files Path")

        self.check_button = QPushButton("Check Vod (C)", self)
        self.check_button.setStyleSheet(normal_button_style)
        
        self.start_button = QPushButton("Download Start (F2)", self)
        self.start_button.setStyleSheet(normal_button_style)

        self.stop_button = QPushButton("Download Stop (Shift + F4)", self)
        self.stop_button.setStyleSheet(normal_button_style)

        self.check_button.setFixedSize(200, 40)
        self.start_button.setFixedSize(200, 40)
        self.stop_button.setFixedSize(200, 40)

        layout = QVBoxLayout()
        
        # download lock, set minimized window, option, quit button box
        lock_option_box = QHBoxLayout()
        lock_option_box.addWidget(self.download_lock_button, alignment=Qt.AlignLeft)
        lock_option_box.addStretch(3)

        option_quit_box = QHBoxLayout()
        option_quit_box.addWidget(self.option_button)
        option_quit_box.addWidget(self.minimized_button)
        option_quit_box.addWidget(self.quit_button)

        lock_option_box.addLayout(option_quit_box)

        # detailed information box
        infomation_box = QGridLayout()
        infomation_box.addWidget(self.title_label, 0, 0)
        infomation_box.addWidget(self.duration_time_label, 1, 0)
        infomation_box.addWidget(self.streamer_label, 2, 0)
        infomation_box.addWidget(self.game_label, 3, 0)
        infomation_box.addWidget(self.start_time_label, 4, 0)
        infomation_box.addWidget(self.quality_label, 5, 0)
        
        infomation_box.addWidget(self.title_text, 0, 1, 1, 3)
        infomation_box.addWidget(self.duration_time_text, 1, 1, 1, 3)
        infomation_box.addWidget(self.streamer_text, 2, 1, 1, 3)
        infomation_box.addWidget(self.game_text, 3, 1, 1, 3)
        infomation_box.addWidget(self.start_time_text, 4, 1, 1, 3)
        infomation_box.addWidget(self.quality_text, 5, 1, 1, 3)

        # preview image + detailed information layout
        merged_infomation_box = QHBoxLayout()
        
        merged_infomation_box.addWidget(self.preview_image)
        merged_infomation_box.addStretch(1)
        
        merged_infomation_box.addLayout(infomation_box)
        merged_infomation_box.addStretch(2)

        # progress bar layout
        progress_bar_layout = QHBoxLayout()
        progress_bar_layout.addWidget(self.progress_bar_status)
        self.progress_bar_status.setAlignment(Qt.AlignCenter)
        self.progress_bar_status.setFont(QFont("", 12))

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

        # set layout
        layout.addLayout(lock_option_box)
        layout.addWidget(self.result_log_box)
        layout.addLayout(merged_infomation_box)
        layout.addLayout(progress_bar_layout)
        layout.addWidget(self.progress_bar)
        layout.addLayout(input_layout)
        layout.addLayout(folder_display_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
