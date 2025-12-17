import sqlite3
import csv
from pathlib import Path

DB_PATH = "data_meteo.db"          # tu base de datos SQLite
TABLE = "error_sarapita"           # tabla a exportar
CSV_PATH = "error_sarapita.csv"    # salida

def export_table_to_csv(db_path: str, table: str, csv_path: str) -> None:
    db_path = str(db_path)
    csv_path = str(csv_path)

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()

        # Obtener nombres de columnas
        cur.execute(f"PRAGMA table_info({table})")
        cols = [row[1] for row in cur.fetchall()]
        if not cols:
            raise ValueError(f"No existe la tabla '{table}' o no tiene columnas.")

        # Leer datos
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        # Escribir CSV
        Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)   # cabecera
            writer.writerows(rows)  # filas

        print(f"Exportado: {len(rows)} filas -> {csv_path}")

    finally:
        conn.close()

if __name__ == "__main__":
    export_table_to_csv(DB_PATH, TABLE, CSV_PATH)
