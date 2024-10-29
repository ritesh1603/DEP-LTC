This project has been tested on Arch Linux and Windows 11.

Setup Backend:

Optionally create new virtual environment by using `python3 -m pip venv .venv && source .venv/bin/activate`

1. Go to script.google.com and create a new script and copy content from `app-scripts/otp.gs` and deploy the script. Copy the url of deployed function.
2. Go to script.google.com and create a new script and copy content from `app-scripts/reminder.gs` and deploy the script. Copy the url of deployed function.
3. `pip install -r requirements.txt`
4. Create `env.py` file with format:
```
OTP_URL='[URL OBTAINED FOR T1]'
REMINDER_URL='[URL OBTAINED FOR T2]'
```
5. `python3 app.py`

![Screenshot 2024-10-29 234306](https://github.com/user-attachments/assets/9bb42601-adc3-4ca1-a2d8-3767b2f6c086)
6. This is the landing page




