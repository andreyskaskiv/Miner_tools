import json
import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from settings import ELECTRICITY_COST, URL_hashrate_no


def initialize_driver() -> webdriver.Chrome:
    """Initializes the Chrome browser driver in headless mode."""
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def navigate_to_url(driver: webdriver.Chrome, url: str) -> None:
    """Navigates to the specified URL."""
    driver.get(url)


def click_button(driver: webdriver.Chrome, button_class: str) -> None:
    """
    Clicks a button with the specified class.

    Args:
      driver (webdriver): The browser driver object.
      button_class (str): The class of the button to click.
    """
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, button_class)))
    button.click()


def input_data(driver: webdriver.Chrome, data_xpath_kwh: str, value: str) -> None:
    """
    Inputs data into a specified element on a webpage.

    Args:
      driver (webdriver): The browser driver object.
      data_xpath_kwh (str): The XPath of the element to input data into.
      value (str): The data to input into the element.
    """
    data = driver.find_element(By.XPATH, data_xpath_kwh)
    data.clear()
    data.send_keys(value)


def fetch_data(driver: webdriver.Chrome) -> list:
    """
    Extracts data from the HTML code, including the new Hashrate value.

    Args:
      driver (webdriver): The browser driver object.

    Returns:
      list: Extracted data with Hashrate added.
    """
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'lxml')
    elements = soup.select('a.deviceLink')

    data = []
    for element in elements[:15]:
        coin = element.select_one('div.w3-col.l3.m12.s12 .deviceHeader')
        hash_rate = element.select_one('div.w3-col.l4.m12.s12 table tbody tr td:nth-of-type(1)')
        power = element.select_one('div.w3-col.l5.m12.s12 table tbody tr td')
        revenue = element.select_one('div.w3-col.l5.m12.s12 table tbody tr td:nth-of-type(2)')
        profit = element.select_one('div.w3-col.l5.m12.s12 table tbody tr td:nth-of-type(3)')
        rev_24h = element.select_one('div.w3-col.l5.m12.s12 table tbody tr:nth-of-type(3) td:nth-of-type(2)')
        profit_24h = element.select_one('div.w3-col.l5.m12.s12 table tbody tr:nth-of-type(3) td:nth-of-type(3)')

        data.append({
            'coin': coin.text if coin else None,
            'hashrate': hash_rate.text if hash_rate else None,
            'power': power.text if power else None,
            'revenue': revenue.text if revenue else None,
            'profit': profit.text if profit else None,
            'rev_24h': rev_24h.text if rev_24h else None,
            'profit_24h': profit_24h.text if profit_24h else None,
        })
    return data


def close_driver(driver: webdriver.Chrome) -> None:
    """Closes the browser driver."""
    driver.quit()


def delete_file(file_name: str) -> None:
    """    Deletes a file if it exists.    """
    if os.path.isfile(file_name):
        os.remove(file_name)


def write_to_file(filename: str, obj: list) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(obj, file, ensure_ascii=False, indent=4)


def parser_hashrate_selenium() -> None:
    URL = URL_hashrate_no
    FILE_NAME = 'get_profit_gpu.json'

    DATA_XPATH_KWH = "//input[@class='calcBoxInput' and @name='kwh']"
    CLICK_BUTTON_CALCULATOR = "inputSubmit"

    driver = initialize_driver()
    navigate_to_url(driver, URL)

    response = requests.get(URL)
    if response.status_code == 200:
        delete_file(FILE_NAME)
        input_data(driver, DATA_XPATH_KWH, ELECTRICITY_COST)
        click_button(driver, CLICK_BUTTON_CALCULATOR)
        get_profit = fetch_data(driver)
        write_to_file(FILE_NAME, get_profit)
    else:
        print(f"{response.status_code} - {response.text}")

    close_driver(driver)

#
# if __name__ == '__main__':
#     parser_hashrate_selenium()
