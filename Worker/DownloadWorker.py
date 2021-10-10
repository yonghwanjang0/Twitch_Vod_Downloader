import copy
import os
import shutil
from FilesDownloader import FilesDownloader
from FilesMerger import FilesMerger
from Functions import handle_download_result, make_folder


def download_procedure(*args):
    size, down_list, downloader, download_loop, lock, SharedData, Signal = (
        args[0], args[1], args[2], args[3], args[4], args[5], args[6])

    stop = False
    quit = False
    bundle_list = []
    left_count = len(down_list)

    for index in down_list:
        if Signal.stop:
            stop = True
            if Signal.quit:
                quit = True
            break

        bundle_list.append(index)
        left_count -= 1

        if len(bundle_list) == size or left_count == 0:
            download_result = download_loop.run_until_complete(
                downloader.bundle_of_downloads(bundle_list))
            handle_download_result(download_result, lock, SharedData)
            bundle_list = []

    return stop, quit


def download_worker(*args):
    (playlist, temp_path, save_path, save_file_name, 
    download_loop, lock, SharedData, Signal) = (
        args[0], args[1], args[2], args[3], 
        args[4], args[5], args[6], args[7])

    # make object
    downloader = FilesDownloader()
    merger = FilesMerger()

    # make temporary files folder
    make_folder(temp_path)

    # input values to object
    downloader.playlist = playlist
    downloader.save_folder_path = temp_path
    merger.temp_folder_path = temp_path
    merger.target_folder_path = save_path

    # make files index list
    index_list = list(range(len(playlist.files)))
    
    bundle_size = 6
    retry_count = 2

    # set download status
    with lock:
        SharedData.status = "Downloading"
        SharedData.log_text_list.append('Start download stream files.')

    # start download loop
    stop, quit = download_procedure(
        bundle_size, index_list, downloader, 
        download_loop, lock, SharedData, Signal)

    # retry for failed download
    while retry_count > 0 and not stop:
        with lock:
            missed_count = len(SharedData.missing_index)
            if missed_count > 0:
                missed_list = copy.deepcopy(SharedData.missing_index)
                SharedData.missing_index = []
                stop, quit = download_procedure(
                    bundle_size, missed_list, downloader, 
                    download_loop, lock, SharedData, Signal)
                retry_count -= 1
            else:
                retry_count = 0

    # download finished
    if not stop:
        with lock:
            if not SharedData.missing_index:
                download_success = True
                SharedData.status = "Merging"
                SharedData.log_text_list.append(
                    'Download finished, Start files merge.')
            else:
                download_success = False
            
        if download_success:
            index_range = [index_list[0], index_list[-1]]
            stop, quit = merger.merge_files(
                index_range, save_file_name, lock, SharedData, Signal)
        else:
            with lock:
                SharedData.status = "Error"
                SharedData.log_text_list.append('Download Failed.')
            shutil.rmtree(temp_path)

        if not stop and download_success:
            with lock:
                SharedData.status = "Done"
                SharedData.log_text_list.append('Merge finished.')
            os.rmdir(temp_path)

    # user forced stop
    if stop:
        if not quit:
            with lock:
                SharedData.status = "Canceled"
                SharedData.log_text_list.append('Download Canceled.')

        shutil.rmtree(temp_path)
        absolute_save_path = save_path + save_file_name
        if os.path.exists(absolute_save_path):
            os.remove(absolute_save_path)
