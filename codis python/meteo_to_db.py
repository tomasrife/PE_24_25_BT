import datos_predic
import datos_reales
import sqlite3

'''
3 - GFS 13 Km
52 - AROME 1.3 Km
107 - ALADIN 2.3 Km
64 - Zephr-hd 2.6 Km
21 - WRF 9 Km
43 - ICON 7 Km
45 - ICON 13 Km
59 - GDPS 15 Km
'''
model_to_name = {"3": "gfs",  "52": "arome", "107": "aladin", "64": "zephr", "21": "wrf", "43": "icon7", "45": "icon13", "59": "gdps"}





def add_prediction(model, spot, taula):
    # Conectar (crea el archivo si no existe)
    conn = sqlite3.connect('data_meteo.db')

    # Crear cursor para ejecutar comandos SQL
    cur = conn.cursor()

    pred = datos_predic.get_prediction(model, spot)
    for p in pred:
        cur.execute(f"SELECT * FROM {taula} WHERE time = ?", (p[0],))
        if cur.fetchone() == None:
            cur.execute(f"INSERT INTO {taula} (time) VALUES (?)", (p[0],))
        cur.execute(f"UPDATE {taula} SET {model_to_name[str(model)]} = ? WHERE time = ?", (p[1], p[0]))

    conn.commit()
    conn.close()






def add_real(taula):
    # Conectar (crea el archivo si no existe)
    conn = sqlite3.connect('data_meteo.db')

    # Crear cursor para ejecutar comandos SQL
    cur = conn.cursor()

    real = datos_reales.get_rvalues()
    for p in real:
        cur.execute(f"SELECT * FROM {taula} WHERE time = ?", (p[0],))
        if cur.fetchone() != None:
            cur.execute(f"UPDATE {taula} SET real = ? WHERE time = ?", (p[1], p[0]))
    conn.commit()
    conn.close()



def add_dir(taula):
    # Conectar (crea el archivo si no existe)
    conn = sqlite3.connect('data_meteo.db')

    # Crear cursor para ejecutar comandos SQL
    cur = conn.cursor()

    real = datos_reales.get_winddir()
    for p in real:
        cur.execute(f"SELECT * FROM {taula} WHERE time = ?", (p[0],))
        if cur.fetchone() != None:
            cur.execute(f"UPDATE {taula} SET dir = ? WHERE time = ?", (p[1], p[0]))
    conn.commit()
    conn.close()


def add_temp(taula):
    # Conectar (crea el archivo si no existe)
    conn = sqlite3.connect('data_meteo.db')

    # Crear cursor para ejecutar comandos SQL
    cur = conn.cursor()

    real = datos_reales.get_temp()
    for p in real:
        cur.execute(f"SELECT * FROM {taula} WHERE time = ?", (p[0],))
        if cur.fetchone() != None:
            cur.execute(f"UPDATE {taula} SET temp = ? WHERE time = ?", (p[1], p[0]))
    conn.commit()
    conn.close()




def create_table(taula):
    # Conectar (crea el archivo si no existe)
    conn = sqlite3.connect('data_meteo.db')

    # Crear cursor para ejecutar comandos SQL
    cur = conn.cursor()

    # Crear tabla de ejemplo
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {taula} (
                time TEXT,
                real REAL,
                gfs REAL,
                arome REAL,
                aladin REAL,
                zephr REAL,
                wrf REAL,
                icon7 REAL,
                icon13 REAL,
                gdps REAL,
                dir INT,
                temp REAL
    )
    ''')

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()