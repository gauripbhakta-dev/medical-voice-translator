"""
Wakes the MedVoice Translator Streamlit app if it has gone to sleep.

Why this exists: a plain HTTP ping (curl, UptimeRobot, etc.) hits the
static "Yes, get this app back up!" page and gets a 200 OK response —
which looks successful to the monitor — but nothing actually gets
clicked, so the app never wakes up. This script uses a real (headless)
browser to detect the wake button and click it, the same way a human
visiting the link would.

If the app is already awake, this script finds no wake button and
exits cleanly — safe to run on a schedule indefinitely.
"""

import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

APP_URL = "https://medvoice-translator.streamlit.app"
PAGE_LOAD_WAIT = 5      # seconds to let the initial page settle
BUTTON_WAIT = 10        # seconds to wait for the wake button to appear
BOOT_WAIT = 20          # seconds to let the app boot after clicking wake

# Streamlit's wake-up button text as of 2026. If Streamlit changes this
# copy, update the XPATH match below accordingly.
WAKE_BUTTON_XPATH = "//button[contains(., 'get this app back up')]"


def main() -> int:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(options=options)
    try:
        print(f"Visiting {APP_URL} ...")
        driver.get(APP_URL)
        time.sleep(PAGE_LOAD_WAIT)

        try:
            wake_button = WebDriverWait(driver, BUTTON_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WAKE_BUTTON_XPATH))
            )
            print("App was asleep. Clicking wake button ...")
            wake_button.click()
            time.sleep(BOOT_WAIT)
            print("Wake click sent. App should be booting.")
        except Exception:
            print("No wake button found — app was already awake.")

        return 0

    except Exception as exc:
        # Don't fail the whole workflow loudly over a transient network
        # blip; log it so it's visible in the Actions run, but exit 0
        # so this doesn't spam email alerts for a one-off hiccup.
        print(f"Wake check encountered an error: {exc}")
        return 0

    finally:
        driver.quit()


if __name__ == "__main__":
    sys.exit(main())
