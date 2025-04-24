class ec_changes_text(object):

    def __init__(self, locator, initial_text):
        self.locator = locator
        self.initial_text = str(initial_text)

    def __call__(self, driver):
        # print(f"******************** call")
        # print(f"self.initial_text: ({self.initial_text})")
        element = driver.find_element(*self.locator)   # Finding the referenced element
        text = element.text;
        if text != self.initial_text:
            return text;
        else:
            return False;