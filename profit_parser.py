import json
import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()
YOUR_API_KEY = os.getenv('YOUR_API_KEY')
POWER_COST = os.getenv('POWER_COST')


def get_data_from_api(api_key: str, power_cost: float) -> requests.Response:
    """
    Fetches data from the API.

    :param api_key: The API key.
    :param power_cost: The cost of electricity.
    :return: The API response.
    """
    url = f"https://api.hashrate.no/v1/gpuEstimates?apiKey={api_key}&powerCost={power_cost}"
    response = requests.get(url)
    return response


def check_response_status(response: requests.Response) -> bool:
    """
    Checks the status of the API response.

    :param response: The API response.
    :return: True if the response status is 200, otherwise False.
    """
    if response.status_code == 200:
        return True
    else:
        return False


def parse_response_to_json(response: requests.Response) -> Dict:
    """
    Converts the API response to JSON.

    :param response: The API response.
    :return: The JSON data.
    """
    data = response.text
    parse_json = json.loads(data)
    return parse_json


def write_data_to_file(filename: str, data: Dict) -> None:
    """
    Writes data to a file.

    :param filename: The name of the file.
    :param data: The data to write.
    """
    with open(filename, 'w') as f:
        json.dump(data, f)


def profit_parser_from_hashrate(your_api_key, power_cost) -> None:
    response = get_data_from_api(your_api_key, power_cost)

    if check_response_status(response):

        json_data = parse_response_to_json(response)
        data_3080 = json_data.get('3080')
        data_1080ti = json_data.get('1080ti')

        write_data_to_file('data_3080.json', data_3080)
        write_data_to_file('data_1080ti.json', data_1080ti)

        # print("Data for 3080:")
        # read_and_print_json_data_from_file('data_3080.json')
        #
        # print("Data for 1080ti:")
        # read_and_print_json_data_from_file('data_1080ti.json')

    else:
        print("An error occurred while executing the request")


if __name__ == "__main__":
    profit_parser_from_hashrate(YOUR_API_KEY, POWER_COST)
