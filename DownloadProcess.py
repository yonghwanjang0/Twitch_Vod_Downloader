from threading import Thread, Lock
from Functions import make_temp_string, infomation_text_for_log
from Worker.DownloadWorker import download_worker
from Worker.UpdateWorker import update_worker
from Worker.ForcedStopWorker import forced_stop_worker
import asyncio


class Signal:
    stop = False
    quit = False


class SharedData:
    finished_count = 0
    total_count = 0
    percent = 0
    missing_index = []
    status = ""
    log_text_list = []
    working = True


def control_function(log_queue, control_conn, args_list):
    SharedData.total_count = len(args_list[0].files)
    SharedData.status = "Initializing"

    playlist, vod_data, vod_id, temp_path, save_path = (
        args_list[0], args_list[1], args_list[4], args_list[5], args_list[6])
    save_file_name = "{}_{}_{}.ts".format(args_list[2], args_list[3], args_list[4])
    use_temp_path = temp_path + make_temp_string() + "\\"

    log_text_list = infomation_text_for_log(
        vod_data, vod_id, save_path, save_file_name, use_temp_path)
    log_queue.put(['log', log_text_list])

    shared_data_lock = Lock()
    download_loop = asyncio.get_event_loop()

    download_thread = Thread(
        target=download_worker, args=(
            playlist, use_temp_path, save_path, save_file_name,
            download_loop, shared_data_lock, SharedData, Signal, ))
    update_thread = Thread(
        target=update_worker, args=(
            log_queue, shared_data_lock, SharedData, ))
    forced_stop_thread = Thread(
        target=forced_stop_worker, args=(
            control_conn, shared_data_lock, SharedData, Signal, ))

    download_thread.daemon = True
    update_thread.daemon = True
    forced_stop_thread.daemon = True

    download_thread.start()
    update_thread.start()
    forced_stop_thread.start()

    download_thread.join()
    update_thread.join()
    forced_stop_thread.join()

    download_loop.close()
    if Signal.quit:
        log_queue.put(['program quit'])
    if not Signal.stop:
        log_queue.put(['process finished'])
