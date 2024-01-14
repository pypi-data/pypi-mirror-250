from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class AutoWeb():
    """
    A class to automate web operations.
    """

    def __init__(self):
        """
        Initialize AutoWeb with the necessary drivers and services.
        """
        self.driver_classes = {
            "Firefox": webdriver.Firefox,
            "Chrome": webdriver.Chrome,
        }
        self.driver_services = {
            "Firefox": FirefoxService,
            "Chrome": ChromeService,
        }
        self.driver_managers = {
            "Firefox": GeckoDriverManager,
            "Chrome": ChromeDriverManager,
        }
        self.browser = None

    def open_browser(self, name: str, url: str) -> None:
        """
        Opens the browser using selenium library. Supports chrome and firefox. Handles webdrivers installation.
        
        :param name: Name of the browser to open.
        :param url: The url on which the browser should open.
        """
        try:
            if name in self.driver_classes:
                driver_class = self.driver_classes[name]
                driver_service = self.driver_services[name]
                driver_manager = self.driver_managers[name]
                service = driver_service(executable_path=driver_manager().install())
                self.browser = driver_class(service=service)
                self.browser.get(url)
            else:
                print(f"Browser '{name}' not supported")
        except Exception as e:
            print(e)

    def close_browser(self) -> None:
        """
        Closes the browser instance.
        """
        if self.browser:
            self.browser.quit()
            self.browser = None

    def navigate(self, action: str) -> None:
        """
        Navigate to forward or back from a page. Also can refresh a page.

        :param action: The action to take.
        """
        if self.browser:
            if action.lower() == "back":
                self.browser.back()
            elif action.lower() == "forward":
                self.browser.forward()
            elif action.lower() == "refresh":
                self.browser.refresh()

    def click_element(self, element) -> None:
        """
        Click on element provided.
        """
        if self.browser and element:
            element.click()

    def enter_text(self, element, text: str) -> None:
        """
        Type text in element.

        :param element: Element to type into should be an input field.
        :param text: Text to type.
        """
        if self.browser and element:
            element.clear()
            element.send_keys(text)

    def wait_for_element(self, locator: str, locator_strategy: str = "NAME", timeout: int = 30):
        """
        Wait for an element to be present.

        :param locator: The locator of the element.
        :param locator_strategy: The strategy to locate the element. Defaults to 'NAME'.
        :param timeout: The maximum time to wait for the element. Defaults to 30.
        :return: The element if found.
        """
        locator_strategy = locator_strategy.upper()
        if self.browser:
            if hasattr(By, locator_strategy):
                strategy = getattr(By, locator_strategy)
                element = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_element_located((strategy, locator))
                )
                return element
            else:
                raise ValueError(f"Invalid locator strategy: {locator_strategy}")

    def page_screen_shot(self, path: str = "screenshot.png") -> None:
        """
        Take a screenshot of the current page.

        :param path: The path to save the screenshot to. Defaults to 'screenshot.png'.
        """
        if path.endswith(".png") or path.endswith(".jpeg"):
            self.browser.get_screenshot_as_file(path)
        else:
            raise Exception("No file type provided in path")


class AutoWebAdvanced(AutoWeb):
    """
    A class to automate advanced web operations.
    """

    def __init__(self):
        """
        Initialize AutoWebAdvanced.
        """
        super().__init__()

    def hover_over_element(self, element) -> None:
        """
        Hover over an element.

        :param element: The element to hover over.
        """
        actions = ActionChains(self.browser)
        actions.move_to_element(element)
        actions.perform()

    def drag_and_drop(self, source_element, target_element) -> None:
        """
        Drag an element and drop it on another element.

        :param source_element: The element to drag.
        :param target_element: The element to drop on.
        """
        actions = ActionChains(self.browser)
        actions.drag_and_drop(source_element, target_element)
        actions.perform()

    def right_click(self, element) -> None:
        """
        Right click on an element.

        :param element: The element to right click on.
        """
        actions = ActionChains(self.browser)
        actions.context_click(element)
        actions.perform()

    def double_click(self, element) -> None:
        """
        Double click on an element.

        :param element: The element to double click on.
        """
        actions = ActionChains(self.browser)
        actions.double_click(element)
        actions.perform()

    def click_and_hold(self, element) -> None:
        """
        Click and hold on an element.

        :param element: The element to click and hold on.
        """
        actions = ActionChains(self.browser)
        actions.click_and_hold(element)
        actions.perform()

    def release_click(self) -> None:
        """
        Release a click.
        """
        actions = ActionChains(self.browser)
        actions.release()
        actions.perform()

    def select_option_from_dropdown(self, element, option_text) -> None:
        """
        Select an option from a dropdown.

        :param element: The dropdown element.
        :param option_text: The text of the option to select.
        """
        select = Select(element)
        select.select_by_visible_text(option_text)

    def deselect_option_from_dropdown(self, element, option_text) -> None:
        """
        Deselect an option from a dropdown.

        :param element: The dropdown element.
        :param option_text: The text of the option to deselect.
        """
        select = Select(element)
        select.deselect_by_visible_text(option_text)

    def switch_to_frame(self, frame_reference) -> None:
        """
        Switch to a frame.

        :param frame_reference: The reference to the frame to switch to.
        """
        self.browser.switch_to.frame(frame_reference)

    def switch_to_default_content(self) -> None:
        """
        Switch to the default content.
        """
        self.browser.switch_to.default_content()

    def switch_to_alert(self) -> None:
        """
        Switch to an alert.
        """
        return self.browser.switch_to.alert
    
    def handle_alert(self, action="accept"):
        """
        Handle an alert.

        :param action: The action to take on the alert. Defaults to 'accept'.
        """
        alert = self.browser.switch_to.alert
        if action.lower() == "accept":
            alert.accept()
        else:
            alert.dismiss()

    def switch_to_window(self, window_name) -> None:
        """
        Switch to a window.

        :param window_name: The name of the window to switch to.
        """
        self.browser.switch_to.window(window_name)

    def switch_to_new_window(self) -> None:
        """
        Switch to a new window.
        """
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def switch_to_previous_window(self) -> None:
        """
        Switch to the previous window.
        """
        self.browser.switch_to.window(self.browser.window_handles[-2])

    def execute_javascript(self, script, *args) -> None:
        """
        Execute JavaScript.

        :param script: The JavaScript to execute.
        :param args: The arguments to the script.
        """
        return self.browser.execute_script(script, *args)

    def execute_async_javascript(self, script, *args) -> None:
        """
        Execute asynchronous JavaScript.

        :param script: The JavaScript to execute.
        :param args: The arguments to the script.
        """
        return self.browser.execute_async_script(script, *args)

    def scroll_into_view(self, element) -> None:
        """
        Scroll an element into view.

        :param element: The element to scroll into view.
        """
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_top(self) -> None:
        """
        Scroll to the top of the page.
        """
        self.browser.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self) -> None:
        """
        Scroll to the bottom of the page.
        """
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_by(self, x, y) -> None:
        """
        Scroll by a certain amount.

        :param x: The amount to scroll horizontally.
        :param y: The amount to scroll vertically.
        """
        self.browser.execute_script(f"window.scrollBy({x}, {y});")

    def get_cookies(self) -> None:
        """
        Get the cookies.
        """
        return self.browser.get_cookies()

    def add_cookie(self, cookie_dict) -> None:
        """
        Add a cookie.

        :param cookie_dict: The cookie to add.
        """
        self.browser.add_cookie(cookie_dict)

    def delete_cookie(self, name) -> None:
        """
        Delete a cookie.

        :param name: The name of the cookie to delete.
        """
        self.browser.delete_cookie(name)

    def delete_all_cookies(self) -> None:
        """
        Delete all cookies.
        """
        self.browser.delete_all_cookies()

    def refresh_page(self) -> None:
        """
        Refresh the page.
        """
        self.browser.refresh()

    def close_current_tab(self) -> None:
        """
        Close the current tab.
        """
        self.browser.close()

    def maximize_window(self) -> None:
        """
        Maximize the window.
        """
        self.browser.maximize_window()

    def minimize_window(self) -> None:
        """
        Minimize the window.
        """
        self.browser.minimize_window()

    def fullscreen_window(self) -> None:
        """
        Make the window fullscreen.
        """
        self.browser.fullscreen_window()

    def set_window_size(self, width, height) -> None:
        """
        Set the size of the window.

        :param width: The width to set.
        :param height: The height to set.
        """
        self.browser.set_window_size(width, height)

    def get_window_size(self) -> None:
        """
        Get the size of the window.
        """
        return self.browser.get_window_size()

    def set_window_position(self, x, y) -> None:
        """
        Set the position of the window.

        :param x: The x-coordinate to set.
        :param y: The y-coordinate to set.
        """
        self.browser.set_window_position(x, y)

    def get_window_position(self) -> None:
        """
        Get the position of the window.
        """
        return self.browser.get_window_position()

    def get_current_url(self) -> None:
        """
        Get the current URL.
        """
        return self.browser.current_url

    def get_title(self) -> None:
        """
        Get the title of the page.
        """
        return self.browser.title

    def get_current_window_handle(self) -> None:
        """
        Get the handle of the current window.
        """
        return self.browser.current_window_handle

    def get_window_handles(self) -> None:
        """
        Get the handles of all windows.
        """
        return self.browser.window_handles

    def implicitly_wait(self, seconds) -> None:
        """
        Set the implicit wait time.

        :param seconds: The number of seconds to wait.
        """
        self.browser.implicitly_wait(seconds)

    def set_page_load_timeout(self, seconds) -> None:
        """
        Set the page load timeout.

        :param seconds: The number of seconds to wait for the page to load.
        """
        self.browser.set_page_load_timeout(seconds)

    def set_script_timeout(self, seconds) -> None:
        """
        Set the script timeout.

        :param seconds: The number of seconds to wait for a script to execute.
        """
        self.browser.set_script_timeout(seconds)

    def check_checkbox(self, element) -> None:
        """
        Check a checkbox if it's not already checked.

        :param element: The checkbox element.
        """
        if not element.is_selected():
            element.click()

    def uncheck_checkbox(self, element) -> None:
        """
        Uncheck a checkbox if it's already checked.

        :param element: The checkbox element.
        """
        if element.is_selected():
            element.click()

    def select_radio_button(self, element) -> None:
        """
        Select a radio button if it's not already selected.

        :param element: The radio button element.
        """
        if not element.is_selected():
            element.click()

    def send_hot_keys(self, element, key: str) -> None:
        """
        Send hotkeys to an element.

        :param element: The element to send hotkeys to.
        :param key: The hotkey to send.
        """
        key = key.upper()
        if hasattr(Keys, key):
            hotkey = getattr(Keys, key)
            element.send_keys(hotkey)
        else:
            raise Exception(f"Key '{key}' not supported")

    def get_page_source(self, path: str = "source_code.txt") -> None:
        """
        Get the source code of the current page and save it to a file.

        :param path: The path to save the source code to. Defaults to 'source_code.txt'.
        """
        html = self.browser.page_source
        with open(path, "w") as f:
            f.write(html)
            f.close()
            