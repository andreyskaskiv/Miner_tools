import time

import psutil
from colorama import Fore, Style
from dotenv import load_dotenv
from ping3 import ping
from prettytable import PrettyTable
from pynvml import *
from tqdm import tqdm

from handlers import get_device_performance, show_profit_gpu
from parser_hashrate_selenium import parser_hashrate_selenium
from settings import MAX_LOAD, MAX_TEMP, MINER_PATHS

load_dotenv()
nvmlInit()
deviceCount = nvmlDeviceGetCount()


def internet_connected(host: str = '8.8.8.8') -> bool:
    """
    Check internet connection by pinging Google DNS.
    """
    if ping(host) is not None:
        print(f"{Fore.GREEN}Internet OK{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}No Internet{Style.RESET_ALL}")
        return False


def get_device_info(i: int):
    """
    Get device information.
    """
    handle = nvmlDeviceGetHandleByIndex(i)
    device_name = nvmlDeviceGetName(handle)
    info = nvmlDeviceGetMemoryInfo(handle)
    temperature = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
    utilization = nvmlDeviceGetUtilizationRates(handle)
    power = nvmlDeviceGetPowerUsage(handle)
    clock_speeds = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
    memory_clock_speeds = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)
    fan_speed = nvmlDeviceGetFanSpeed(handle)
    return device_name, info, temperature, utilization, power, clock_speeds, memory_clock_speeds, fan_speed


def is_miner_running():
    """
    Checks if the miner is currently running.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'lolMiner.exe':
            return True
    return False


def countdown(t=5):
    """
    Creates a countdown from t to 0с.

    Args:
        t (int): The start of the countdown. Default is 5с.
    """
    for _ in tqdm(range(t, 0, -1), bar_format='Miner will start in {remaining} seconds... '):
        time.sleep(1)


def run_miner(coin):
    """
    Starts the miner if there is an internet connection.
    """
    miner_name = None
    if internet_connected():
        try:
            for path in MINER_PATHS:
                miner_bat = MINER_PATHS[path].split("\\")[-1]
                miner_name = miner_bat.split('.')[0]
                if miner_name == coin:
                    os.startfile(MINER_PATHS[path])
                    print(f"Starting miner...{MINER_PATHS[path]}")
                    countdown(20)
                    break
        except Exception as e:
            print(e)
    return miner_name


def stop_miner():
    """
    Stops the miner if it is currently running.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'lolMiner.exe':
            proc.kill()


def update_profit_parser():
    while True:
        parser_hashrate_selenium()
        time.sleep(1 * 30 * 60)


def find_miner_coin(coins: list, miner_paths: dict):
    for coin in coins:
        if coin in miner_paths:
            return coin
            break
    return None


def main():
    """
    Main function to check each available GPU.
    """
    bat_miner_name = None
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        file_name = 'get_profit_gpu.json'
        coins = show_profit_gpu(file_name) if os.path.isfile(file_name) else None

        if coins is None:
            print("Connect to hashrate.no ...")

        table = PrettyTable()
        table.field_names = ["Num", "Device", "Mem, MB, used", "CCLK", "MCLK", "Util-on",
                             "Temp", "Fan", "Power"]
        table.align["Device"] = "l"

        for i in range(deviceCount):
            device_name, info, temperature, utilization, power, clock_speeds, memory_clock_speeds, fan_speed = get_device_info(
                i)

            if temperature > MAX_TEMP and is_miner_running():
                stop_miner()
                print("Stopping miner due to high temperature...")
                countdown(300)

            if (utilization.gpu < MAX_LOAD
                    and not is_miner_running()
                    and coins is not None):

                profit_coin = find_miner_coin(coins, MINER_PATHS)
                print(f"Profit Coin: {Fore.CYAN}{profit_coin}{Style.RESET_ALL}")

                bat_miner_name = run_miner(profit_coin)

            if coins is not None:
                profit_coin = find_miner_coin(coins, MINER_PATHS)

                if bat_miner_name != profit_coin:
                    stop_miner()

            device_data = get_device_performance(device_name, info, temperature, utilization, power, clock_speeds,
                                                 memory_clock_speeds, fan_speed)

            device_data.insert(0, i + 1)
            table.add_row(device_data)
        print(table)

        time.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=update_profit_parser).start()
    threading.Thread(target=main).start()
