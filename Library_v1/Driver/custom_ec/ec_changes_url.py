import time;
import re;

class ec_changes_url(object):

    def __init__(self, url_regex, time_wait: int = None):
        self.url_regex = url_regex
        if time_wait:
            # print(f"esperando {time_wait}....")
            time.sleep(time_wait)

    def __call__(self, driver):
        # print(f"******************** call")
        status = re.search(self.url_regex, driver.current_url) != None
        # print(f"status: {status}")
        return status;