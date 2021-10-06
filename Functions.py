import os
import time
import shutil
import pickle
import random
from datetime import datetime
from pathlib import Path
import pytz
import tzlocal
import m3u8


option_pkl = "option_values.pkl"


# create playlist object
def make_playlist_object(path):
    playlist = m3u8.load(path)

    return playlist


# extract key
def extract_key(playlist_path):
    split = playlist_path.split("/")
    key = split[3]

    return key


# convert duration time to time string
def convert_second_to_string(total_second:int):
    string = "{0}:{1}:{2}"
    hour, reminder = divmod(total_second, 3600)
    minute, second = divmod(reminder, 60)
    time_string = string.format(str(hour).zfill(2), 
    str(minute).zfill(2), str(second).zfill(2))

    return time_string


# UTC to localtime string
def convert_utc_to_local_time(utc:str):
    # utc string (e.g : '2021-04-12T05:08:12Z')
    local_timezone = tzlocal.get_localzone()
    utc_time = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    local_time_string = local_time.strftime('%Y-%m-%d %H:%M:%S')

    return local_time_string


def load_option_values():
    with open(option_pkl, mode='rb') as r:
        values_dict = pickle.load(r)
    
    return values_dict


def save_option_values(values_dict):
    with open(option_pkl, mode='wb') as f:
        pickle.dump(values_dict, f)


def free_space_calculator(hdd_disk_path):
    p = hdd_disk_path.split("\\")[0]
    total, used, free = shutil.disk_usage(p)

    return free


def make_default_path_string(key):
    if key == "temp path":
        value = str(os.path.join(Path.home(), "Downloads\\Temp\\"))
    else:
        value = str(os.path.join(Path.home(), "Downloads\\"))

    return value


def handle_download_result(result, lock, SharedData):
    missed_list = []
    with lock:
        count, total_count, percent = (
            SharedData.finished_count, SharedData.total_count, 
            SharedData.percent)

    for unit in result:
        if unit[0] is True:
            count += 1
            percent = check_percent(
                count, total_count, percent, lock, SharedData)
        else:
            missed_list.append(unit[1])

    with lock:
        SharedData.finished_count = count
        if missed_list:
            SharedData.missing_index.extend(missed_list)


def find_percent_change(count:int, total_count:int, percent:int):
    current_percent = int((count / total_count) * 100)

    if percent != current_percent:
        return True
    else:
        return False


def check_percent(*args):
    count, total_count, percent, lock, data_object = (
        args[0], args[1], args[2], args[3], args[4]
    )
    percent_increase = find_percent_change(
        count, total_count, percent)
    if percent_increase:
        percent = int((count / total_count) * 100)
        with lock:
            data_object.percent = percent

    return percent


def get_start_time(key):
    start_time = int(key.split("_")[-1])

    return start_time


def get_broadcast_date_string(key):
    start_time = get_start_time(key)
    time_string = time.strftime("%Y%m%d", 
    time.localtime(start_time))

    return time_string


def get_streamer_id(key):
    id_split_list = key.split("_")[1:-2]
    streamer_id = recombine_streamer_id(id_split_list)

    return streamer_id


def recombine_streamer_id(id_string_list):
    streamer_id = ""
    for arg in id_string_list:
        streamer_id += arg + "_"
    streamer_id = streamer_id[:-1]

    return streamer_id


def make_folder(folder_path):
    folder_check = os.path.isdir(folder_path)
    if folder_check is False:
        os.makedirs(folder_path)


def make_temp_string():
    char = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
    index_pool = range(len(char))
    
    length = 32
    output = "".join([char[random.choice(index_pool)] for index in range(length)])

    return output


# for start download information log
def infomation_text_for_log(*args):
    vod_data, vod_id, save_path, file_name, temp_path = (
        args[0], args[1], args[2], args[3], args[4]
    )
    text_list = []
    text_list.append("")
    text_list.append("Video Infomation")
    text_list.append("---------------------------")
    text_list.append("Url : https://www.twitch.tv/videos/{}".
    format(vod_id))
    text_list.append("Quality : {}@{}fps (Source)".format(
        str(vod_data['resolutions']['chunked']), 
        str(round(vod_data['fps']['chunked']))))
    text_list.append("Duration : {}".format(
        convert_second_to_string(vod_data['length'])))
    text_list.append("---------------------------")

    text_list.append("")

    text_list.append("Save Infomation")
    text_list.append("---------------------------")
    text_list.append("Save File : {}{}".format(save_path, file_name))
    text_list.append("Temporary Download Folder : {}".format(temp_path))
    text_list.append("---------------------------")
    text_list.append("")

    return text_list
