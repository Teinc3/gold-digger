# Gold Digger
Script to automate gold farming in Territorial.io

## How to use
1. Extract the login token from the Network tab in the browser's developer tools (F12)
![Visual instructions on how to find token](docs/network_token.png)

2. Install required python dependencies
- asyncio (Should be included in 3.4+)
- websockets

```bash
pip install -r requirements.txt
```

3. Run makefile to build native security module

```bash
cd security
makefile
```

4. Run script with the extracted token

Example:
```bash
python main.py 69a45135d14c125b1248235c25bca0
```

5. Enjoy your gold!

6. To stop the script, press `Ctrl+C`