import time
import os

def wait_condition(fn: callable, attempts: int = 10):
    waitingTime = 1
    while True:
        responseStatus = fn();
        if responseStatus: break;
        time.sleep(waitingTime);
        attempts = attempts - 1
        if attempts <= 0: raise ValueError("As tentativas foram esgotadas")

def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds