import sqlite3
# Conectar (crea el archivo si no existe)
conn = sqlite3.connect('data_meteo.db')

# Crear cursor para ejecutar comandos SQL
cur = conn.cursor()

#cur.execute("DROP TABLE IF EXISTS error_sarapita")

cur.execute(f'''
CREATE TABLE IF NOT EXISTS error_sarapita (
            time TEXT,
            dgfs REAL,
            darome REAL,
            dicon7 REAL,
            dir INT,
            temp REAL
)
''')

cur.execute(f'''SELECT time, real, gfs, arome, icon7, dir, temp 
            FROM meteo_sarapita WHERE 
            real IS NOT NULL AND 
            gfs IS NOT NULL AND 
            arome IS NOT NULL AND 
            icon7 IS NOT NULL''')


rows = cur.fetchall()

for r in rows:
    time_ = r[0]
    real_ = r[1]
    gfs_ = r[2]
    arome_ = r[3]
    icon7_ = r[4]
    dir_ = r[5]
    temp_ = r[6]

    
    cur.execute('''
        INSERT INTO error_sarapita (time, dgfs, darome, dicon7, dir, temp) VALUES (?, ?, ?, ?, ?, ?)
    ''', (time_,
        round(abs(gfs_ - real_), 2),
        round(abs(arome_ - real_), 2),
        round(abs(icon7_ - real_), 2),
        dir_,
        temp_))

conn.commit()
conn.close()