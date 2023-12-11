import time

import psutil
from colorama import Fore, Style
from dotenv import load_dotenv
from ping3 import ping
from pynvml import *
from tqdm import tqdm

from handlers import print_device_info
from profit_parser import profit_parser_from_hashrate

load_dotenv()
nvmlInit()
deviceCount = nvmlDeviceGetCount()

MAX_LOAD = int(os.getenv('MAX_LOAD'))
MAX_TEMP = int(os.getenv('MAX_TEMP'))
BAT_PATH = os.getenv('BAT_PATH')
YOUR_API_KEY = os.getenv('YOUR_API_KEY')
POWER_COST = os.getenv('POWER_COST')


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


def update_profit_parser(your_api_key, power_cost):
    while True:
        profit_parser_from_hashrate(your_api_key, power_cost)
        time.sleep(12 * 60 * 60)  # Обновлять каждые 12 часов


def main():
    """
    Main function to check each available GPU.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        for i in range(deviceCount):
            device_name, info, temperature, utilization, power, clock_speeds, memory_clock_speeds, fan_speed = get_device_info(
                i)

            if utilization.gpu < MAX_LOAD and not is_miner_running():
                run_miner()

            if temperature > MAX_TEMP and is_miner_running():
                stop_miner()

            print_device_info(device_name, info, temperature, utilization, power, clock_speeds, memory_clock_speeds,
                              fan_speed)

        time.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=update_profit_parser, args=(YOUR_API_KEY, POWER_COST)).start()
    threading.Thread(target=main).start()
