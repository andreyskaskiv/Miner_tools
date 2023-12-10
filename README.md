# Dog

![Dog.png](Dog.png)


1. cd Miner_tools
2. `pip install -r requirements.txt`
3. Add your constants to the .env file
    ```
    MAX_LOAD=80
    MAX_TEMP=60
    BAT_PATH=G:\\Miner\\1.80a\\1_mine_karlsen.bat
    YOUR_API_KEY=6921d42,kgb8ghffa009dc4f8hjkfhje4fg505db43fgha2e
    POWER_COST=0.07
    ```

4. Set absolute path for lolMiner.exe file

    ```
    @echo off
    %~dp0lolMiner.exe --algo KARLSEN --pool de.karlsen.herominers.com:1195 --user YOUR_KARLSEN_WALLET_ADDRESS.YOUR_WORKER_NAME --cclk 1200,1680 --coff 100,100 --mclk 810,810 --pl 200,250
    pause
    ```

5. cmd
    ```pycon
    python .\DoG.py
    ```
   
