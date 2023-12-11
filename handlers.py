import json
import os
from typing import Any, Dict

from colorama import Fore, Style


def read_and_print_data_from_file(filename: str) -> None:
    """
    Reads data from a file and prints it to the console.

    :param filename: The name of the file.
    """
    with open(filename, 'r') as f:
        data = json.load(f)

        prev_revenueUSD24 = None

        # print(f"{Fore.BLUE}{data['device']['name']}: {Style.RESET_ALL}")

        print(f" Profit: {data['profit']['coin']},"
              f" RevenueUSD: {round(data['profit']['revenueUSD'], 2)}$,"
              f" ProfitUSD: {round(data['profit']['profitUSD'], 2)}$")

        revenueUSD24 = round(data['profit24']['revenueUSD24'], 2)
        if prev_revenueUSD24 is None or revenueUSD24 != prev_revenueUSD24:
            print(f"{Fore.CYAN} Profit24: {data['profit24']['coin']},"
                  f" RevenueUSD24: {revenueUSD24}$,"
                  f" ProfitUSD24: {round(data['profit24']['profitUSD24'], 2)}${Style.RESET_ALL}")
            prev_revenueUSD24 = revenueUSD24

        print(f" Revenue: {data['revenue']['coin']},"
              f" RevenueUSD: {round(data['revenue']['revenueUSD'], 2)}$,"
              f" ProfitUSD: {round(data['revenue']['profitUSD'], 2)}$")

        revenueUSD24 = round(data['revenue24']['revenueUSD24'], 2)
        if prev_revenueUSD24 is None or revenueUSD24 != prev_revenueUSD24:
            print(f" Revenue24: {data['revenue24']['coin']},"
                  f" RevenueUSD24: {revenueUSD24}$,"
                  f" ProfitUSD24: {round(data['revenue24']['profitUSD24'], 2)}$")
            prev_revenueUSD24 = revenueUSD24


def print_device_info(device_name: str, info: Any, temperature: int, utilization: Any,
                      power: int, clock_speeds: int, memory_clock_speeds: int, fan_speed: int):
    """
    Print device information.
    """

    print(f"\n{'- ' * 30}\n {Fore.GREEN}{device_name}:{Style.RESET_ALL}")

    print(
        f"  Memory: {round(info.free / (1024 ** 2), 2)} MB free,"
        f" {round(info.used / (1024 ** 2), 2)} MB used,"
        f" {info.total / (1024 ** 2)} MB total")

    print(f"  Clock Speeds: {Fore.CYAN}{clock_speeds} MHz{Style.RESET_ALL}")
    print(f"  Memory Clock Speeds: {Fore.CYAN}{memory_clock_speeds} MHz{Style.RESET_ALL}")
    print(f"  Utilization: {utilization.gpu}% \n")

    if temperature <= 35:
        print(f" Temperature: {Fore.BLUE}{temperature} C{Style.RESET_ALL}")
    elif 35 < temperature <= 60:
        print(f" Temperature: {Fore.YELLOW}{temperature} C{Style.RESET_ALL}")
    else:
        print(f" Temperature: {Fore.RED}{temperature} C{Style.RESET_ALL}")

    print(f" Fan Speed: {fan_speed}%")
    print(f" Power usage: {Fore.CYAN}{round(power / 1000, 1)} W{Style.RESET_ALL} \n")

    file_name = 'data_3080.json' if device_name == "GeForce RTX 3080" else 'data_1080ti.json'

    if os.path.isfile(file_name):
        read_and_print_data_from_file(file_name)
    else:
        print("Connect to hashrate.no ...")


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
