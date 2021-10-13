from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QKeySequence, QShortcut

from multiprocessing import Process, Pipe, Manager
import urllib.request
import os

from Constants import message_box_size, dialog_box_size, disk_buffer_size
from Functions import convert_second_to_string, \
    convert_utc_to_local_time, load_option_values, save_option_values, \
        extract_key, make_playlist_object, free_space_calculator, \
            make_default_path_string, get_broadcast_date_string, \
                get_streamer_id
from GetVodInfo import GetVodInfo
from DownloadProcess import control_function
from InputValueAnalysis import InputValueAnalysis
from UserInterface import CentralWidget
from Option import OptionDialog
from SizeCalculator import SizeCalculator
from StyleSheet import main_window_style, message_box_style


class InterfaceControl(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Twitch Vod Downloader v1.0'
        self.position = (50, 100, 800, 800)
        self.cWidget = CentralWidget()
        self.setCentralWidget(self.cWidget)
        self.setStyleSheet(main_window_style)

        self.input_value_analyzer = InputValueAnalysis()
        self.vod_info_obtainer = GetVodInfo()
        self.size_calculator = SizeCalculator()

        self.manager = Manager()
        self.log_queue = self.manager.Queue()
        self.sub_conn, self.main_conn = Pipe()

        self.update_check_timer = QTimer()
        self.option_values = load_option_values()

        self.temp_folder_path = None
        self.target_folder_path = None
        self.set_default_path()

        self.controller = None
        self.ready_to_start = False
        self.work_status = False

        self.analysis_result = None
        self.playlist_object = None

        self.vod_data = None
        self.vod_id = None
        self.key = None
        self.broadcast_date = None
        self.streamer = None
        self.size_data = []

        self.offset = None

        self.msgbox = QMessageBox()
        self.quit_box = QMessageBox()
        self.quit_timer = None
        self.close_signal = False

        # Function Setting
        self.download_lock_button = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.download_lock_button.activated.connect(self.click_download_button)
        self.cWidget.download_lock_button.clicked.connect(self.change_download_lock)

        self.option_dialog = QShortcut(QKeySequence('F10'), self)
        self.option_dialog.activated.connect(self.change_option)
        self.cWidget.option_button.clicked.connect(self.change_option)

        self.cWidget.minimized_button.clicked.connect(self.showMinimized)
        self.cWidget.quit_button.clicked.connect(self.close_app)

        self.check_vod = QShortcut(QKeySequence('C'), self)
        self.check_vod.activated.connect(self.check_video)
        self.cWidget.check_button.clicked.connect(self.check_video)

        self.download_start = QShortcut(QKeySequence('F2'), self)
        self.download_start.activated.connect(self.start)
        self.cWidget.start_button.clicked.connect(self.start)

        self.download_stop = QShortcut(QKeySequence('Shift+F4'), self)
        self.download_stop.activated.connect(self.stop)
        self.cWidget.stop_button.clicked.connect(self.stop)

        self.go_input_box = QShortcut(QKeySequence('1'), self)
        self.go_input_box.activated.connect(self.go_to_input_box)

        self.set_function_activation("wait")
        self.cWidget.progress_bar_status.setText("Waiting")
        
        # App Window setting
        self.setWindowTitle(self.title)
        self.setGeometry(
            self.position[0], self.position[1], self.position[2], self.position[3])
        
        # set frameless option
        self.setWindowFlags(Qt.FramelessWindowHint)

    # check vod url
    def check_video(self):
        if not self.work_status:
            self.set_function_activation("wait")
            self.clear_display_info()
            input_value = self.get_input_value()
            self.analyze_input_value(input_value)
            self.select_popup()

    def get_input_value(self):
        return self.cWidget.input_value_box.text()

    def analyze_input_value(self, input_value:str):
        self.analysis_result = self.input_value_analyzer.run(input_value)

    # after check vod -> select popup window by situation
    def select_popup(self):
        option = self.analysis_result[-1]
        if option == "not valid":
            self.error_message("Error",
                               'The entered value is not valid. Please re-enter.')
        elif option == "subscribers only":
            self.error_message("Error",
                               'This Video is for only subscriber.')
        elif option == "not exists":
            self.error_message("Error",
                               'No video information. This video has been deleted or not available.')
        else:
            self.display_vod_info(self.analysis_result[0])
            log_text = ("Find Video Infomation. (path : https://www.twitch.tv/videos/{})"
            .format(self.analysis_result[0]))
            self.log_update(log_text, self.cWidget.result_log_box)
            log_text = """Ready to start download."""
            self.log_update(log_text, self.cWidget.result_log_box)
            self.set_function_activation("ready")
            self.cWidget.progress_bar_status.setText("Ready")
            self.ready_to_start = True

    def set_style_to_message_box(self, box, box_size:tuple):
        box_pos = [self.pos().x() + (self.width() // 2) - (box_size[0] // 2), 
        self.pos().y() + (self.height() // 2) - (box_size[1] // 2)]
        box.setGeometry(box_pos[0], box_pos[1],
                           box_size[0], box_size[1])
        box.setStyleSheet(message_box_style)

    def error_message(self, title, message):
        self.set_style_to_message_box(self.msgbox, message_box_size)

        return self.msgbox.critical(self.msgbox, title, message)

    def get_vod_info(self, video_id:str):
        self.vod_data = None
        self.vod_info_obtainer.__init__()
        self.vod_info_obtainer.video_id = video_id
        load_failed = self.vod_info_obtainer.get_json()
        if load_failed:
            self.get_vod_info(video_id)
        self.vod_info_obtainer.get_data()
        if self.vod_info_obtainer.data:
            self.vod_data = self.vod_info_obtainer.data

    def set_vod_info(self):
        if self.vod_data:
            self.cWidget.title_text.setText(self.vod_data['title'])

            duration_time_string = convert_second_to_string(
                self.vod_data['length'])
            self.cWidget.duration_time_text.setText(duration_time_string)

            streamer_id_name = "{} ({})".format(self.vod_data['name'], self.vod_data['id'])
            self.cWidget.streamer_text.setText(streamer_id_name)

            self.cWidget.game_text.setText(self.vod_data['game'])

            start_time_string = convert_utc_to_local_time(
                self.vod_data['start_time'])
            self.cWidget.start_time_text.setText(start_time_string)

            fps = round(self.vod_data['fps']['chunked'])
            resolutions = self.vod_data['resolutions']['chunked']
            quality_text = "{} {} fps".format(str(resolutions), str(fps))
            self.cWidget.quality_text.setText(quality_text)
            
            image_url = self.vod_data['preview_image_path']
            self.set_preview_image(image_url)
    
    def set_preview_image(self, url):
        image = QPixmap()
        image_data = urllib.request.urlopen(url).read()
        image.loadFromData(image_data)
        self.cWidget.preview_image.setPixmap(image)

    def display_vod_info(self, video_id:str):
        self.get_vod_info(video_id)
        self.set_vod_info()

    # clear a display vod information
    def clear_display_info(self):
        self.cWidget.result_log_box.clear()

        self.cWidget.title_text.setText("")
        self.cWidget.duration_time_text.setText("")
        self.cWidget.streamer_text.setText("")
        self.cWidget.game_text.setText("")
        self.cWidget.start_time_text.setText("")
        self.cWidget.quality_text.setText("")

        image = QPixmap()
        self.cWidget.preview_image.setPixmap(image)
        self.cWidget.progress_bar.reset()
        self.cWidget.progress_bar_status.setText("")

    def check_enough_disk_size(self):
        predict_size = self.size_calculator.run(self.playlist_object)
        possible_minimum_size = predict_size + disk_buffer_size

        temp_disk_free_size = free_space_calculator(self.temp_folder_path)
        target_disk_free_size = free_space_calculator(self.target_folder_path)

        if temp_disk_free_size > possible_minimum_size and \
            target_disk_free_size > possible_minimum_size:
            possible_download = True
        else:
            self.size_data = [
                predict_size, target_disk_free_size, temp_disk_free_size]
            possible_download = False

        return possible_download

    def get_Insufficient_space_string(self):
        # estimated, save free space, temp free space
        convert_size = []
        for size in self.size_data:
            convert = self.size_calculator.convert_size_units(size)
            convert_size.append(convert)

        string = (
            "(estimated file size : {} {}.\nsave file disk free space : {} {}, "
            "temp files disk free space : {} {}.)"
        .format(
            str(convert_size[0][0]), convert_size[0][1],
            str(convert_size[1][0]), convert_size[1][1],
            str(convert_size[2][0]), convert_size[2][1])
        )

        return string

    def check_file_exists(self):
        save_file_path = "{}{}_{}_{}.ts".format(
            self.target_folder_path, self.broadcast_date, 
            self.streamer, self.vod_id)
        file_exists = os.path.exists(save_file_path)

        return file_exists
    
    # start download
    def start(self):
        if not self.work_status and self.ready_to_start:
            playlist_path = self.analysis_result[1]
            self.playlist_object = make_playlist_object(playlist_path)
            
            self.set_download_info()
            file_exists = self.check_file_exists()
            if file_exists:
                self.error_message("Error",
                'The video file is already in the folder.')
                return

            possible_download = self.check_enough_disk_size()
            if possible_download:
                self.start_control_process()
            else:
                space_string = self.get_Insufficient_space_string()
                string = ('There is not enough disk space to download.\n{}'
                .format(space_string))
                self.error_message("Error", string)

    # start download process
    def start_control_process(self):
        self.set_function_activation("download")
        self.work_status = True

        self.cWidget.progress_bar_status.setText("Initializing")
        self.log_update("Download has been started.", 
        self.cWidget.result_log_box)
        self.log_update("Initializing for download...", 
        self.cWidget.result_log_box)

        args_list = [self.playlist_object, self.vod_data, 
        self.broadcast_date, self.streamer, self.vod_id, 
        self.temp_folder_path, self.target_folder_path]

        self.controller = Process(target=control_function, args=(
            self.log_queue, self.sub_conn, args_list,))
        self.controller.daemon = True
        self.controller.start()

        self.update_check_timer.setInterval(100)
        self.update_check_timer.timeout.connect(
            self.check_update)
        self.update_check_timer.start()

    def set_download_info(self):
        self.key = extract_key(self.analysis_result[1])
        self.broadcast_date = get_broadcast_date_string(self.key)
        self.streamer = get_streamer_id(self.key)
        self.vod_id = self.analysis_result[0]

    def click_download_button(self):
        self.cWidget.download_lock_button.click()

    def change_download_lock(self):
        if self.work_status:
            if self.cWidget.download_lock_button.isChecked():
                self.cWidget.stop_button.setEnabled(False)
                self.download_stop.setEnabled(False)
            else:
                self.cWidget.stop_button.setEnabled(True)
                self.download_stop.setEnabled(True)

    # stop download
    def stop(self):
        if self.work_status and not self.cWidget.download_lock_button.isChecked():
            self.main_conn.send("stop")

    # option dialog
    def change_option(self):
        path_data = [self.temp_folder_path, self.target_folder_path]
        dialog = OptionDialog(path_data)
        dialog.setWindowTitle("Option")

        calibration_value = (5, 80)
        
        pos_x = (self.pos().x() + (self.width() // 2) - 
        (dialog_box_size[0] // 2) - calibration_value[0])
        pos_y = (self.pos().y() + (self.height() // 2) - 
        (dialog_box_size[1] // 2) - calibration_value[1])
        dialog_pos = [pos_x, pos_y]

        dialog.setGeometry(dialog_pos[0], dialog_pos[1],
                           dialog_box_size[0], dialog_box_size[1])

        ok = dialog.exec_()
        if ok:
            return_paths = dialog.get_values()
            self.change_folder_path(return_paths)

    def change_folder_path(self, paths):
        self.temp_folder_path, self.target_folder_path = (paths[0], paths[1])
        self.change_display_path()
        
        self.option_values['temp path'] = paths[0]
        self.option_values['save path'] = paths[1]
        save_option_values(self.option_values)

    @staticmethod
    def log_update(msg, textbox):
        textbox.append(msg)

    def check_update(self):
        if self.log_queue.qsize():
            result = self.log_queue.get()
            if result[0] == "program quit":
                self.close_signal = True
            else:
                if result[0] != "process finished":
                    # integer, string, string
                    if result[0] == "status":
                        self.cWidget.progress_bar_status.setText(result[1])
                        self.cWidget.progress_bar.setValue(0)
                    elif result[0] == "percent":
                        self.cWidget.progress_bar.setValue(result[1])
                    # send log text
                    else:
                        if type(result[1]) == str:
                            self.log_update(result[1], self.cWidget.result_log_box)
                        # list type
                        else:
                            for line in result[1]:
                                self.log_update(line, self.cWidget.result_log_box)
                        
                    if result[1] == 'Download Canceled.':
                        self.finished_work("Canceled")
                    if result[1] == "Download Failed.":
                        self.finished_work("Error")
                else:
                    self.finished_work()

    # set default path (saved values or default values)
    def set_default_path(self):
        self.temp_folder_path = self.option_values['temp path']
        self.target_folder_path = self.option_values['save path']

        if self.option_values['temp path'] == '':
            self.option_values['temp path'] = make_default_path_string('temp path')
            self.temp_folder_path = self.option_values['temp path']

        if self.option_values['save path'] == '':
            self.option_values['save path'] = make_default_path_string('save path')
            self.target_folder_path = self.option_values['save path']

        self.change_display_path()
        save_option_values(self.option_values)

    # change path display string
    def change_display_path(self):
        self.cWidget.temp_folder_display.setText(self.temp_folder_path)
        self.cWidget.target_folder_display.setText(self.target_folder_path)

    # input box shortcut (1)
    def go_to_input_box(self):
        self.cWidget.input_value_box.setFocus()

    # select active function by status
    def set_function_activation(self, status:str):
        # [check, start, stop, option]
        if status == "wait":
            enable_list = [True, False, False, True]
            self.cWidget.input_value_box.setEnabled(True)
        elif status == "ready":
            enable_list = [True, True, False, True]
        # status == "download":
        else:
            enable_list = [False, False, True, False]
            if self.cWidget.download_lock_button.isChecked():
                enable_list[2] = False
            self.cWidget.input_value_box.setEnabled(False)

        self.set_button_activation(enable_list)
        self.set_menu_activation(enable_list)

    def set_button_activation(self, enable_list):
        self.cWidget.check_button.setEnabled(enable_list[0])
        self.cWidget.start_button.setEnabled(enable_list[1])
        self.cWidget.stop_button.setEnabled(enable_list[2])
        self.cWidget.option_button.setEnabled(enable_list[3])

    def set_menu_activation(self, enable_list):
        self.check_vod.setEnabled(enable_list[0])
        self.download_start.setEnabled(enable_list[1])
        self.download_stop.setEnabled(enable_list[2])
        self.option_dialog.setEnabled(enable_list[3])

    # mouse event override (for window move by drag.)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton :
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        try:
            if self.offset is not None and event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)
        except:
            pass

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    # after finished work
    def finished_work(self, finish_type="Done"):
        self.controller.join()
        self.controller.terminate()
        self.update_check_timer.stop()

        if finish_type == "Done":
            self.cWidget.progress_bar_status.setText("Done")
            self.log_update("Download Finished.", 
            self.cWidget.result_log_box)

        self.log_update("==============================",
                        self.cWidget.result_log_box)

        self.controller = None
        self.ready_to_start = False
        self.work_status = False

        self.analysis_result = None
        self.playlist_object = None

        self.vod_data = None
        self.vod_id = None
        self.key = None
        self.broadcast_date = None
        self.streamer = None

        while not self.log_queue.empty():
            self.log_queue.get()

        self.set_function_activation("wait")

    def ask_want_close(self):
        self.set_style_to_message_box(self.quit_box, message_box_size)
        reply = self.quit_box.question(
            self.quit_box, 'Message', "Are you sure to quit?", 
        self.quit_box.Yes | self.quit_box.No, self.quit_box.No)

        return reply
    
    # closeEvent method (alt + F4) override
    def closeEvent(self, event):
        event.ignore()
        self.close_app()

    def close_app(self):
        reply = self.ask_want_close()
        if reply == self.quit_box.Yes:
            self.prepare_to_quit()

    def prepare_to_quit(self):
        if self.work_status:
            self.main_conn.send("stop-quit")
        else:
            self.close_signal = True

        # wait for download tasks to be cleaned up
        if self.quit_timer is None:
            self.quit_timer = QTimer()
            self.quit_timer.setInterval(100)
            self.quit_timer.timeout.connect(
                self.check_process_closed)
            self.quit_timer.start()

    def check_process_closed(self):
        if self.close_signal is True:
            self.program_quit()
            self.quit_timer.stop()

    def program_quit(self):
        QCoreApplication.exit(0)
