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
![Screenshot 2024-10-29 235048](https://github.com/user-attachments/assets/9c43d6d5-5226-44df-975f-70d18de174fa)
![Screenshot 2024-10-29 235029](https://github.com/user-attachments/assets/06335e38-cb76-4334-9d2c-ecae151dde3c)
![Screenshot 2024-10-29 235016](https://github.com/user-attachments/assets/13211ac2-84ff-4094-984d-12beb6e92864)
![Screenshot 2024-10-29 234944](https://github.com/user-attachments/assets/8bba4207-b912-4f73-8ada-dea08ddeea3d)
![Screenshot 2024-10-29 234923](https://github.com/user-attachments/assets/0360a0c4-e275-40bf-8714-18430bc72129)
![Screenshot 2024-10-08 182152](https://github.com/user-attachments/assets/d2af4962-1563-4315-8d77-4964c311cb7e)
![Screenshot 2024-10-08 182142](https://github.com/user-attachments/assets/74716356-7a55-4942-acab-2e029b7800cb)





