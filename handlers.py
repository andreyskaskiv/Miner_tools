import json
from typing import Dict

from colorama import Fore, Style
from prettytable import PrettyTable


def show_profit_gpu(filename: str) -> None:
    """
       Reads data from a file and outputs it to the console.

       :param filename: file_name
       """
    with open(filename, 'r') as f:
        data = json.load(f)

        table = PrettyTable()
        table.field_names = ["Coin", "Power", "Revenue", "Profit", "Revenue (24h)", "Profit (24h)"]
        table.align["Coin"] = "l"

        max_revenue = max(item['revenue'] for item in data[:5])
        max_profit = max(item['profit'] for item in data[:5])
        max_rev_24h = max(item['rev_24h'] for item in data[:5])
        max_profit_24h = max(item['profit_24h'] for item in data[:5])

        for item in data[:5]:
            coin = item['coin'].split(' ')[0]
            power = f"{Fore.YELLOW}{item['power']}{Style.RESET_ALL}"
            revenue = f"{Fore.GREEN}{item['revenue']}{Style.RESET_ALL}" if item['revenue'] == max_revenue else item[
                'revenue']
            profit = f"{Fore.GREEN}{item['profit']}{Style.RESET_ALL}" if item['profit'] == max_profit else item[
                'profit']
            rev_24h = f"{Fore.GREEN}{item['rev_24h']}{Style.RESET_ALL}" if item['rev_24h'] == max_rev_24h else item[
                'rev_24h']
            profit_24h = f"{Fore.GREEN}{item['profit_24h']}{Style.RESET_ALL}" if item[
                                                                                     'profit_24h'] == max_profit_24h else \
                item['profit_24h']

            table.add_row([coin, power, revenue, profit, rev_24h, profit_24h])

        print(table)


def get_device_performance(device_name, info, temperature, utilization, power, clock_speeds, memory_clock_speeds,
                           fan_speed):
    memory = f"{round(info.free / (1024 ** 2), 2)} MB free, {round(info.used / (1024 ** 2), 2)} MB used, {info.total / (1024 ** 2)} MB total"
    utilization_str = f"{utilization.gpu}%"

    if temperature <= 35:
        temperature_str = f"{Fore.BLUE}{temperature} C{Style.RESET_ALL}"
    elif 35 < temperature <= 60:
        temperature_str = f"{Fore.YELLOW}{temperature} C{Style.RESET_ALL}"
    else:
        temperature_str = f"{Fore.RED}{temperature} C{Style.RESET_ALL}"

    fan_speed_str = f"{fan_speed}%"
    power_str = f"{Fore.CYAN}{round(power / 1000, 1)} W{Style.RESET_ALL}"

    return [f"{Fore.GREEN}{device_name}{Style.RESET_ALL}", memory,
            f"{Fore.CYAN}{clock_speeds} MHz{Style.RESET_ALL}", f"{Fore.CYAN}{memory_clock_speeds} MHz{Style.RESET_ALL}",
            utilization_str, temperature_str, fan_speed_str, power_str]


def print_json_data(json_data: Dict) -> None:
    """
    Prints the JSON data to the console.

    :param json_data: The JSON data.
    """
    print(json.dumps(json_data, indent=4))


def read_and_print_json_data_from_file(filename: str) -> None:
    """
    Reads data from a file and prints it to the console.

    :param filename: The name of the file.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        print_json_data(data)


def write_data_to_file(filename: str, data: Dict) -> None:
    """
    Writes data to a file.

    :param filename: The name of the file.
    :param data: The data to write.
    """
    with open(filename, 'w') as f:
        json.dump(data, f)
