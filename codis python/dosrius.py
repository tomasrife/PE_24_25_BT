import requests
import sqlite3
from datetime import datetime

def es_fecha_mayor(fecha_dada: str) -> bool:
    
    #true si la fecha donada es major a l'actual

    fecha_dada = fecha_dada.split(' ')
    ymd_dada = fecha_dada[0].split('-')
    h_dada = int((fecha_dada[1])[0:2])

    fecha_actual = str(datetime.now())
    fecha_actual = fecha_actual.split(' ')
    ymd_act = fecha_actual[0].split('-')
    h_act = int((fecha_actual[1])[0:2])
    
    if ymd_dada[0] != ymd_act[0]: return int(ymd_dada[0]) > int(ymd_act[0])
    if ymd_dada[1] != ymd_act[1]: return int(ymd_dada[1]) > int(ymd_act[1])
    if ymd_dada[2] != ymd_act[2]: return int(ymd_dada[2]) > int(ymd_act[2])
    return h_dada >= h_act

def kmh_to_knot(velocitat):
    return round(velocitat*0.539957)

# Conectar (crea el archivo si no existe)
conn = sqlite3.connect('data_meteo.db')

# Crear cursor para ejecutar comandos SQL
cur = conn.cursor()
cur.execute('select time from meteo_dosrius where real is NULL or dir is NULL or temp is NULL')
times = cur.fetchall()
times = times[0:50]
for t in times:
    date = t[0]

    if not es_fecha_mayor(date):
        date_splitejat = date.split(' ')
        date_sense_hora = date_splitejat[0]
        
        url = 'https://www.meteo.cat/observacions/xema/dades?codi=UQ&dia=' + date_sense_hora + 'T00:00Z'
        
        resp = requests.get(url)
        if resp.status_code == 200:
            html = resp.text
            #trobar velocitats
            posv = html.find("'velocitatVent'") + 18
            posfv = html.find(']', posv)
            string_velocitats = html[posv : posfv]
            #trobar dir's
            posd = html.find('direccioVent') + 16
            posfd = html.find(']', posd)
            string_direccions = html[posd : posfd]
            #trobar temp's
            post = html.find('\'temperatura\':')
            post = html.find('[', post)
            posft = html.find(']', post)
            string_temperatures = html[post : posft]
            #formatejem
            string_velocitats = string_velocitats.replace(",", "")
            string_direccions = string_direccions.replace(",", "")
            string_temperatures = string_temperatures.replace(",", "")
            string_temperatures = string_temperatures.replace("[", "")
            #obtenim lists
            velocitats = string_velocitats.split(' ')
            direccions = string_direccions.split(' ')
            temperatures = string_temperatures.split(' ')

            index = (int(date_splitejat[1][0 : 2]))*2

            #print(f"{date}: {len(velocitats)} -> {index} valor vel: {float(velocitats[index])}, valor dir: {direccions[index]}, valor temp: {temperatures[index]}\n")
            cur.execute("UPDATE meteo_dosrius SET real = ?, dir = ?, temp = ? WHERE time = ?", (kmh_to_knot(float(velocitats[index])), direccions[index], float(temperatures[index]), date))
        
        else: print("No s'ha pogut accedir a l'url\n")

conn.commit()
conn.close()