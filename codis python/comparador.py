import sqlite3

model_to_name = {"3": "gfs",  "52": "arome", "107": "aladin", "64": "zephr", "21": "wrf", "43": "icon7", "45": "icon13", "59": "gdps"}

def compare_model(model):
    conn = sqlite3.connect('data_meteo.db')
    cur = conn.cursor()

    col = model_to_name[str(model)]
    cur.execute(f"SELECT {col}, real FROM meteo WHERE real IS NOT NULL AND {col} IS NOT NULL")
    resp = cur.fetchall()

    conn.close()

    if not resp:  # por si no hay datos
        return None

    diffs = [float(r[0]) - float(r[1]) for r in resp]

    dif = sum(diffs) / len(diffs)   # promedio
    abs_dif = sum(abs(d) for d in diffs) / len(diffs)

    return dif, abs_dif


models = [3, 52, 107, 64, 21, 43, 45, 59]
for model in models:
    d = compare_model(model)
    if d != None:
        print(f"El modelo {model_to_name[str(model)].upper()} se va de {round(d[0],2)} nudos de media, el error absoluto medio es de {round(d[1],2)} nudos")
    else:
        print(f"No hay datos del modelo {model_to_name[str(model)].upper()}")