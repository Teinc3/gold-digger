# Gold Digger
Python script to automate gold farming in Territorial.io.

This code is only for educational purposes and should not be misused in any way or form.

## How to use
1. Extract the login token from the Network tab in the browser's developer tools (F12)
![Visual instructions on how to find token](docs/network_token.png)

*Update: You don't have to remove spaces from the Token for it to work*

2. Install required Python dependencies
- asyncio (Should be included in 3.4+)
- websockets

```bash
pip install -r requirements.txt
```

3. Run makefile to build native security module

```bash
cd security
make
```

*Note: You will need the gcc compiler as well as GNU make to complete this step.

4. Run script with the extracted token

Example:
```bash
> python main.py 69a45135d14c125b1248235c25bca0
```
OR
```bash
> python main.py
Enter account token: 69a45135d14c125b1248235c25bca0
```

5. Enjoy your gold!

6. To stop the script, press `Ctrl+C`

## Testimonials
We are accepting more testimonials! Please DM **@teinc3** on Discord.
- Testimonial from DanTheMan<br>
!["this shit works i now have 1446 gold after an hour farm"](docs/Testimonial_Dan.jpg)
- Testimonial from Luxus<br>
![1169 gold and in some hours I’m safe for 6 years ezzz](docs/Testimonial_Luxus.jpg)