# Dog

![Dog.png](Dog.png)


1. cd Miner_tools
2. `pip install -r requirements.txt`
3. Fill out the calculator and copy the link to a file `parser_hashrate_selenium.py`

   ```pycon
   def parser_hashrate_selenium() -> None:
       URL = "https://hashrate.no/GPUcalculator?3080=1&1080ti=1"
      ....
   ```

4. Add your constants to the .env file
    ```
    MAX_LOAD=80
    MAX_TEMP=60
    BAT_PATH=G:\\Miner\\1.80a\\1_mine_karlsen.bat
    YOUR_API_KEY=6921d42,kgb8ghffa009dc4f8hjkfhje4fg505db43fgha2e
    POWER_COST=0.07
    ```

5. Set absolute path for lolMiner.exe file

    ```
    @echo off
    %~dp0lolMiner.exe --algo KARLSEN --pool de.karlsen.herominers.com:1195 --user YOUR_KARLSEN_WALLET_ADDRESS.YOUR_WORKER_NAME --cclk 1200,1680 --coff 100,100 --mclk 810,810 --pl 200,250
    pause
    ```

6. cmd
    ```pycon
    python .\DoG.py
    ```
   
