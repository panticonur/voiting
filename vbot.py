import argparse
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def run_iteration(driver, page_name: str, item_name: str) -> None:
    driver.get(page_name)
    wait = WebDriverWait(driver, 20)

    radio_locators = [
        (By.CSS_SELECTOR, f"input[type='radio'][name='{item_name}']"),
        (By.CSS_SELECTOR, f"input[type='radio'][value='{item_name}']"),
        (By.CSS_SELECTOR, f"input[type='radio'][id='{item_name}']"),
        (By.XPATH, f"//label[normalize-space()='{item_name}']//input[@type='radio']"),
        (By.XPATH, f"//label[normalize-space()='{item_name}']/preceding::input[@type='radio'][1]"),
        (By.XPATH, f"//label[normalize-space()='{item_name}']/following::input[@type='radio'][1]"),
        (By.XPATH, f"//input[@type='radio' and @aria-label='{item_name}']"),
    ]

    radio = None
    for by, selector in radio_locators:
        try:
            radio = wait.until(EC.presence_of_element_located((by, selector)))
            if radio:
                break
        except Exception:
            continue

    if radio is None:
        raise RuntimeError(f"Radio button '{item_name}' not found on {page_name}")

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
    try:
        radio.click()
    except Exception:
        driver.execute_script("arguments[0].click();", radio)

    time.sleep(args.interval * 15)

    button = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[normalize-space()='Abstimmen']"
        " | //input[(@type='button' or @type='submit') and @value='Abstimmen']"
        " | //*[@role='button' and normalize-space()='Abstimmen']"
        " | //a[normalize-space()='Abstimmen']",
    )))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    try:
        button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", button)

    time.sleep(args.interval * 10)
    driver.quit()

def main() -> None:
    parser = argparse.ArgumentParser(description="Periodically vote on a web page.")
    parser.add_argument("--interval", type=float, required=True, help="Interval between iterations, in minutes")
    parser.add_argument("--page_name", required=True, help="URL of the page to open")
    parser.add_argument("--item_name", required=True, help="Name/value/id/label of the radio button to select")
    args = parser.parse_args()

    try:
        while True:
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--start-maximized")
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ChromeOptions")
                driver = webdriver.Chrome(options=options)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Chrome")

                run_iteration(driver, args.page_name, args.item_name)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Vote submitted.")
            except WebDriverException as e:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] WebDriver error: {e}")
            except Exception as e:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iteration failed: {e}")

            time.sleep(args.interval * 60)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
