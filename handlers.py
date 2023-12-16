import json
from typing import Dict

from colorama import Fore, Style
from prettytable import PrettyTable

from settings import MINER_PATHS


def show_profit_gpu(filename: str) -> list:
    NUMBER_OF_LINES = 10
    """
       Reads data from a file and outputs it to the console.

       :param filename: file_name
       """
    with open(filename, 'r') as f:
        data = json.load(f)

        table = PrettyTable()
        table.field_names = ["Coin", "Hashrate", "Power", "Revenue", "Profit", "Revenue (24h)", "Profit (24h)"]
        table.align["Coin"] = "l"

        max_revenue = max(item.get('revenue', None) for item in data[:NUMBER_OF_LINES])
        max_profit = max(item.get('profit', None) for item in data[:NUMBER_OF_LINES])
        max_rev_24h = max(item.get('rev_24h', None) for item in data[:NUMBER_OF_LINES])
        max_profit_24h = max(item.get('profit_24h', None) for item in data[:NUMBER_OF_LINES])

        coins = []

        for item in data[:NUMBER_OF_LINES]:
            coins.append(item.get('coin', None).split(' ')[0])

            coin = (f"{Fore.YELLOW}{item.get('coin', None).split(' ')[0]}{Style.RESET_ALL}"
                    if item.get('coin', None) in MINER_PATHS
                    else item.get('coin', None).split(' ')[0])

            hashrate = item.get('hashrate', None)

            power = f"{Fore.YELLOW}{item.get('power', None)}{Style.RESET_ALL}"

            revenue = (f"{Fore.GREEN}{item.get('revenue', None)}{Style.RESET_ALL}"
                       if item.get('revenue', None) == max_revenue
                       else item.get('revenue', None))

            profit = (f"{Fore.GREEN}{item.get('profit', None)}{Style.RESET_ALL}"
                      if item.get('profit', None) == max_profit
                      else item.get('profit', None))

            rev_24h = (f"{Fore.GREEN}{item.get('rev_24h', None)}{Style.RESET_ALL}"
                       if item.get('rev_24h', None) == max_rev_24h
                       else item.get('rev_24h', None))

            profit_24h = (f"{Fore.GREEN}{item.get('profit_24h', None)}{Style.RESET_ALL}"
                          if item.get('profit_24h', None) == max_profit_24h
                          else item.get('profit_24h', None))

            table.add_row([coin, hashrate, power, revenue, profit, rev_24h, profit_24h])

        print(table)
        return coins


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
