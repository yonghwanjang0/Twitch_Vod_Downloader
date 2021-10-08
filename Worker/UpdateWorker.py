import time
from SendUpdateHandler import SendUpdateHandler


# percent change, status change, add log text
def update_worker(log_queue, lock, SharedData):
    with lock:
        working = SharedData.working
        percent = SharedData.percent
        status = SharedData.status

    # make object
    update_handler = SendUpdateHandler()

    # set queue
    update_handler.queue = log_queue

    # When it detects a change in value, it is updated in the queue.
    finish_moment = False
    while working:
        with lock:
            if SharedData.percent != percent:
                update_handler.send(['percent', SharedData.percent])
                percent = SharedData.percent

            if SharedData.status != status:
                update_handler.send(['status', SharedData.status])
                status = SharedData.status

            if SharedData.log_text_list:
                for log in SharedData.log_text_list:
                    update_handler.send(['log', log])
                SharedData.log_text_list = []

            working = SharedData.working
            
            if SharedData.status == "Done" or \
                SharedData.status == "Canceled" or \
                SharedData.status == "Error":
                finish_moment = True

            if finish_moment:
                working = False
                SharedData.working = False
        time.sleep(0.1)
