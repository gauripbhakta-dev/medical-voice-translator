#!/usr/bin/env python3
"""
Keeps medvoice-translator.streamlit.app awake.

Streamlit Community Cloud puts an app to sleep after inactivity. A plain
HTTP ping is not enough: the sleep page itself returns 200 OK, so uptime
monitors report the app as "up" while it is actually asleep. Waking it
requires clicking the "Yes, get this app back up!" button, which needs a
real browser.

This script loads the page headlessly, clicks the button if it is there,
and exits quietly if the app was already awake.

Runs from .github/workflows/keep-medvoice-awake.yml
"""

import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

APP_URL = "https://medvoice-translator.streamlit.app"
PAGE_LOAD_WAIT = 12      # seconds to let the page settle
POST_CLICK_WAIT = 45     # container restart is slow; give it room


def build_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    # Selenium 4 resolves the driver itself; no chromedriver install needed.
    return webdriver.Chrome(options=opts)


def find_wake_button(driver):
    """Streamlit has changed this button's markup before, so try a few ways."""
    selectors = [
        (By.XPATH, "//button[contains(., 'get this app back up')]"),
        (By.XPATH, "//button[contains(., 'Yes, get this app back up')]"),
        (By.XPATH, "//*[@data-testid='wakeup-button-viewer']"),
        (By.XPATH, "//button[contains(., 'back up')]"),
    ]
    for how, what in selectors:
        try:
            el = driver.find_element(how, what)
            if el.is_displayed():
                return el
        except Exception:
            continue
    return None


def main():
    driver = None
    try:
        driver = build_driver()
        print(f"Loading {APP_URL}")
        driver.get(APP_URL)
        time.sleep(PAGE_LOAD_WAIT)

        button = find_wake_button(driver)

        if button is None:
            print("No wake button found - app was already awake.")
            return 0

        print("App was asleep. Clicking wake button...")
        button.click()
        time.sleep(POST_CLICK_WAIT)

        still_asleep = find_wake_button(driver)
        if still_asleep is None:
            print("App is back up.")
            return 0

        print("Clicked, but the app has not finished restarting yet.")
        print("This is usually fine - the next scheduled run will confirm.")
        return 0

    except WebDriverException as exc:
        print(f"Browser error: {exc}")
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 1
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    sys.exit(main())
