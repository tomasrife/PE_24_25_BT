'''
3 - GFS 13 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=3&rundef=2025081106x0x240x0x240-2025081100x243x384x249x384&id_spot=1105404&ai=1&WGCACHEABLE=21600&cachefix=39.363x2.955x12
52 - AROME 1.3 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=52&rundef=2025081112x1x51x1x51&id_spot=1105404&ai=1&WGCACHEABLE=10800&cachefix=39.363x2.955x12
107 - ALADIN 2.3 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=107&rundef=2025081112x0x72x0x72&id_spot=1105404&ai=1&WGCACHEABLE=21600&cachefix=39.363x2.955x12
64 - Zephr-hd 2.6 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=64&rundef=2025081106x0x12x0x12x2025081111-2025081106x22x36x22x36-2025081012x64x78x64x78-2025081018x82x96x82x96-2025081018x106x120x106x120-2025081018x130x144x130x144&id_spot=1105404&ai=1&WGCACHEABLE=21600&cachefix=39.363x2.955x12
21 - WRF 9 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=21&rundef=2025081106x0x78x0x78&id_spot=1105404&ai=1&WGCACHEABLE=21600&cachefix=39.363x2.955x12
43 - ICON 7 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=43&rundef=2025081112x0x78x0x78&id_spot=1105404&ai=1&WGCACHEABLE=10800&cachefix=39.363x2.955x12
45 - ICON 13 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=45&rundef=2025081112x0x180x0x180&id_spot=1105404&ai=1&WGCACHEABLE=21600&cachefix=39.363x2.955x12
59 - GDPS 15 Km: https://www.windguru.net/int/iapi.php?q=forecast&id_model=59&rundef=2025081100x0x240x0x240&id_spot=1105404&ai=1&WGCACHEABLE=43200&cachefix=39.363x2.955x12

Los datos son horarios OJO
'''

import requests
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def unix_to_utc2(unix_timestamp):
    # Convertimos el timestamp a UTC
    dt_utc = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    
    # Convertimos a la zona horaria de España, con cambio de hora automático
    dt_spain = dt_utc.astimezone(ZoneInfo("Europe/Madrid"))
    
    return dt_spain.strftime('%Y-%m-%d %H:%M:%S')

def get_rundef_for_model(data, model):
    target_model = model
    for tab in data['tabs']:
        for m in tab['id_model_arr']:
            if m['id_model'] == target_model:
                return m['rundef']


def get_link(data, model, wgcache, spot):
    rundef = get_rundef_for_model(data, model)
    return "https://www.windguru.net/int/iapi.php?q=forecast&id_model="+str(model)+"&rundef="+str(rundef)+"&id_spot="+spot+"&ai=1&WGCACHEABLE="+str(wgcache)+"&cachefix=39.363x2.955x12"



def get_prediction(model, spot):
    model_cache = {"3": "21600",  "52": "10800", "107": "21600", "64": "21600", "21": "21600", "43": "10800", "45": "21600", "59": "43200"}
    url_forecast_spot = "https://www.windguru.cz/int/iapi.php?q=forecast_spot&id_spot="+spot

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Referer": "https://www.windguru.cz/",
        "Origin": "https://www.windguru.cz",
        "Cookie": f"langc=es-; deviceid=7963f8528bc2f4f9ba8bff68cfc6eddc; session=614048078917361237a1d066ede21c64; wgcookie=2|||||||||{spot}||||0|53_0|0|||||||||"
    }

    response = requests.get(url_forecast_spot, headers=headers)

    if response.status_code == 200:
        json_string = response.text

        data = json.loads(json_string)

        wgcache = model_cache[str(model)]
        link = get_link(data, model, wgcache, spot)

        forecast = requests.get(link, headers=headers)
        if forecast.status_code == 200:
            forecast = json.loads(forecast.text)
            initstamp = forecast["fcst"]["initstamp"] + forecast["wgmodel"]["hr_start"]*3600
            wnd = forecast['fcst']['WINDSPD']

            offset = forecast["wgmodel"]["hr_step"]*3600

            wnd_pred = []

            for i in range(24):
                wnd_pred.append((unix_to_utc2(initstamp + offset*i), wnd[i]))

            return wnd_pred   
        print(f"error al obtener la predicción - {forecast.status_code}")
    print(f"error al obtener el rundef para la predicción - {response.status_code}") 
    return []