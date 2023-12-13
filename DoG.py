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

load_dotenv()
nvmlInit()
deviceCount = nvmlDeviceGetCount()

MAX_LOAD = int(os.getenv('MAX_LOAD'))
MAX_TEMP = int(os.getenv('MAX_TEMP'))
BAT_PATH = os.getenv('BAT_PATH')


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


def run_miner():
    """
    Starts the miner if there is an internet connection.
    """
    if internet_connected():
        try:
            os.startfile(BAT_PATH)
            print("Starting miner...")
            countdown(5)
        except Exception as e:
            print(e)


def stop_miner():
    """
    Stops the miner if it is currently running.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'lolMiner.exe':
            proc.kill()
            print("Stopping miner due to high temperature...")
            countdown(300)


def update_profit_parser():
    while True:
        parser_hashrate_selenium()
        time.sleep(1 * 60 * 60)  # update every 1 hour


def main():
    """
    Main function to check each available GPU.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        table = PrettyTable()
        table.field_names = ["Num", "Device", "Mem, MB, used", "CCLK", "MCLK", "Util-on",
                             "Temp", "Fan", "Power"]
        table.align["Device"] = "l"

        for i in range(deviceCount):
            device_name, info, temperature, utilization, power, clock_speeds, memory_clock_speeds, fan_speed = get_device_info(
                i)

            if utilization.gpu < MAX_LOAD and not is_miner_running():
                run_miner()

            if temperature > MAX_TEMP and is_miner_running():
                stop_miner()

            device_data = get_device_performance(device_name, info, temperature, utilization, power, clock_speeds,
                                                 memory_clock_speeds, fan_speed)

            device_data.insert(0, i + 1)

            table.add_row(device_data)

        print(table)

        file_name = 'get_profit_gpu.json'
        if os.path.isfile(file_name):
            show_profit_gpu(file_name)
        else:
            print("Connect to hashrate.no ...")

        time.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=update_profit_parser).start()
    threading.Thread(target=main).start()
