import requests
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

def unix_to_utc2(unix_timestamp):
    # Convertimos el timestamp a UTC
    dt_utc = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    
    # Convertimos a la zona horaria de España, con cambio de hora automático
    dt_spain = dt_utc.astimezone(ZoneInfo("Europe/Madrid"))
    return dt_spain.strftime('%Y-%m-%d %H:%M:%S')

def get_rvalues():
    # URL del clientrawextra.txt
    url = "https://cnrapita.com/meteo/clientrawextra.txt"

    # Descargar el archivo
    resp = requests.get(url)

    if resp.status_code == 200:
        parsed = resp.text.strip().split(' ')
        # Extraer las posiciones de velocidad del viento
        indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 562, 563, 564, 565]
        wind_speeds = [float(parsed[i]) for i in indices]


        #indices_horas = [459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 578, 579, 580, 581]

        
        hora_final_str = parsed[581]
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        dt_final = datetime.strptime(fecha_actual + " " + hora_final_str, "%d/%m/%Y %H:%M")
        dt_final = dt_final.replace(minute=0)
        unix_final = int(dt_final.timestamp())

        time_wind = []
        for i in range(len(wind_speeds)):
            time_wind.append((unix_to_utc2((unix_final - (len(wind_speeds)-i-1)*3600)), wind_speeds[i]))

        return time_wind
    print(f"error al obtener los datos reales (velocidad) - {resp.status_code}")
    return []

def get_winddir():
    # URL del clientrawextra.txt
    url = "https://cnrapita.com/meteo/clientrawextra.txt"

    # Descargar el archivo
    resp = requests.get(url)

    if resp.status_code == 200:
        parsed = resp.text.strip().split(' ')

        # Extraer las posiciones de dirección del viento
        indices = [536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 590, 591, 592, 593]
        dirs = [float(parsed[i]) for i in indices]

        #indices_horas = [459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 578, 579, 580, 581]

        
        hora_final_str = parsed[581]
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        dt_final = datetime.strptime(fecha_actual + " " + hora_final_str, "%d/%m/%Y %H:%M")
        dt_final = dt_final.replace(minute=0)
        unix_final = int(dt_final.timestamp())

        time_dir = []
        for i in range(len(dirs)):
            time_dir.append((unix_to_utc2((unix_final - (len(dirs)-i-1)*3600)), dirs[i]))

        return time_dir
    print(f"error al obtener los datos reales (dirección) - {resp.status_code}")
    return []


def get_temp():
    # URL del clientrawextra.txt
    url = "https://cnrapita.com/meteo/clientrawextra.txt"

    # Descargar el archivo
    resp = requests.get(url)

    if resp.status_code == 200:
        parsed = resp.text.strip().split(' ')

        # Extraer las posiciones de dirección del viento
        indices = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 566, 567, 568, 569]
        temps = [float(parsed[i]) for i in indices]

        #indices_temp = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 566, 567, 568, 569]
        #indices_horas = [459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 578, 579, 580, 581]

        
        hora_final_str = parsed[581]
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        dt_final = datetime.strptime(fecha_actual + " " + hora_final_str, "%d/%m/%Y %H:%M")
        dt_final = dt_final.replace(minute=0)
        unix_final = int(dt_final.timestamp())

        time_temp = []
        for i in range(len(temps)):
            time_temp.append((unix_to_utc2((unix_final - (len(temps)-i-1)*3600)), temps[i]))

        return time_temp
    print(f"error al obtener los datos reales (dirección) - {resp.status_code}")
    return []