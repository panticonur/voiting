import argparse
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def run_iteration(driver, page_name: str, item_name: str) -> None:
    driver.get(page_name)
    wait = WebDriverWait(driver, 20)

    button = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[normalize-space()='Direkt zur Abstimmung']"
        " | //input[(@type='button' or @type='submit') and @value='Direkt zur Abstimmung']"
        " | //*[@role='button' and normalize-space()='Direkt zur Abstimmung']"
        " | //a[normalize-space()='Direkt zur Abstimmung']",
    )))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    try:
        button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", button)
    
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
    time.sleep(2)

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

    result_xpath = (
        f"//*[contains(normalize-space(.), \"{item_name}\")"
        f" and contains(., 'Stimmen)')"
        f" and not(.//*[contains(normalize-space(.), \"{item_name}\") and contains(., 'Stimmen)')])]"
    )
    try:
        result_element = wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        match = re.search(r"\((\d+)\s+Stimmen\)", result_element.text)
        if match:
            votes = int(match.group(1))
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Votes {votes}")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Could not read vote count: {e}")

    time.sleep(10)
    driver.quit()

def main() -> None:
    page_name = "https://tafel-oesterreich.at/voting-2026/"
    item_name = "Integrationstreffen 50+ (Neki)"
    
    parser = argparse.ArgumentParser(description="Periodically vote on a web page.")
    parser.add_argument("--interval", type=float, required=True, help="Interval between iterations, in minutes")
    parser.add_argument("--move_window", type=float, required=True, help="Move Chrome left or right")
    args = parser.parse_args()
    
    try:
        while True:
            try:
                options = webdriver.ChromeOptions()
                # options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
                # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Open Chrome")
                driver.set_window_position(args.move_window, 0)

                run_iteration(driver, page_name, item_name)
                # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Vote submitted.")
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
