import time


def forced_stop_worker(control_conn, lock, data_object, signal):
    working = True
    while working:
        if control_conn.poll(timeout=1):
            value = control_conn.recv()
            if "quit" in value:
                signal.quit = True
                with lock:
                    data_object.working = False
            if "stop" in value:
                signal.stop = True
                working = False
                control_conn.close()

        else:
            with lock:
                working = data_object.working

        time.sleep(0.3)
