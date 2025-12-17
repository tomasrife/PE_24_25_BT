import meteo_to_db
import time


spot = "1105404" # SA RÀPITA
models = [3, 52, 107, 64, 21, 43, 45, 59]

meteo_to_db.create_table("meteo_sarapita")
for model in models:
    meteo_to_db.add_prediction(model, spot, "meteo_sarapita")
meteo_to_db.add_real("meteo_sarapita")
meteo_to_db.add_dir("meteo_sarapita")
meteo_to_db.add_temp("meteo_sarapita")


spot = "1217069" # DOSRIUS
meteo_to_db.create_table("meteo_dosrius")
for model in models:
    meteo_to_db.add_prediction(model, spot, "meteo_dosrius")
#meteo_to_db.add_real("meteo_dosrius")
#meteo_to_db.add_dir("meteo_dosrius")
