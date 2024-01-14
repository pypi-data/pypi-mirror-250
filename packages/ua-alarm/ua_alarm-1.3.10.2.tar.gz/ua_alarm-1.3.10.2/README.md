# UA_ALARM 🚨
> **Elegant, modern and asynchronous UkraineAlarm API framework in Python**

## About

### UK

**Імплементує [api.ukrainealarm.com](https://api.ukrainealarm.com/swagger/index.html), який повертає інформацію про
повітряні тривоги в Україні.**

**Потребує API-ключ. Подавайте запит на отримання через форму на [api.ukrainealarm.com](https://api.ukrainealarm.com/).**

>**Приклад роботи функції alert_loop українською мовою, за дефолтом українська**
>
>![image](https://github.com/user-sspmynxdvb/ua_alarm/assets/132933165/dabcd9ab-e5cd-41fa-afb2-4854d48acbe8)

### EN

**Implements [api.ukrainealarm.com](https://api.ukrainealarm.com/swagger/index.html) API that returns info about Ukraine
air raid alarms.**

**Request API key via form on [api.ukrainealarm.com](https://api.ukrainealarm.com/).**

>**An example of the alert_loop function in English, Ukrainian by default**
>
>![image](https://github.com/user-sspmynxdvb/ua_alarm/assets/132933165/48c8cc1a-17f3-481f-b5e3-f0e97b833145)

> **About text was copied from [github.com/PaulAnnekov/ukrainealarm](https://github.com/PaulAnnekov/ukrainealarm)**

## Installing

### pip

``` bash
pip install ua_alarm
```

### poetry

``` bash
poetry add ua_alarm
```

### Example

```python
from ua_alarm import Client as UkraineAlertApiClient
import os
from asyncio import run

# Clear the console screen
os.system('cls' if os.name == 'nt' else 'clear')

api_token = "YOUR_API_KEY"
client = UkraineAlertApiClient(api_token)

# Run the main function
if __name__ == '__main__':
    try:
        run(client.get_alerts())
    except KeyboardInterrupt:
        exit()
```