# %%
# Cargue los datos de las tabla "files/input/drivers.csv" a una variable llamada
# drivers, usando pandas 
import pandas as pd
drivers = pd.read_csv("files/input/drivers.csv")


# %%
# Cargue los datos de las tabla "files/input/timesheet.csv" a una variable llamada
# timesheet, usando pandas
timesheet = pd.read_csv("files/input/timesheet.csv")

# %%
# Calcule el promedio de las columnas "hours-logged" y "miles-logged" en la 
# tabla "timesheet", agrupando los resultados por cada conductor (driverId).
avg_timesheet = timesheet.groupby("driverId")[["hours-logged", "miles-logged"]].mean().reset_index()
avg_timesheet

# %%
# Cree una tabla llamada "timesheet_with_means" basada en la tabla "timesheet", 
# agregando una columna con el promedio de "hours-logged" para cada conductor (driverId).
timesheet_with_means = timesheet.merge(avg_timesheet[["driverId", "hours-logged"]], on="driverId", suffixes=("", "_mean"))

# %%
# Cree una tabla llamada "timesheet_below" a partir de "timesheet_with_means", filtrando los registros 
# donde "hours-logged" sea menor que "mean_hours-logged".
timesheet_below = timesheet_with_means[timesheet_with_means["hours-logged"] < timesheet_with_means["hours-logged_mean"]]
timesheet_below


import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Asegurar directorios de salida
os.makedirs(os.path.join('files','output'), exist_ok=True)
os.makedirs(os.path.join('files','plots'), exist_ok=True)

# Crear un resumen agregando promedios de horas y millas por driver
summary = timesheet.groupby('driverId')[['hours-logged','miles-logged']].mean().reset_index()
if 'name' in drivers.columns:
	summary = summary.merge(drivers[['driverId','name']], on='driverId', how='left')

# Guardar summary.csv en la ruta que espera la prueba (relative to repo root when tests run)
summary_path = os.path.join('files','output','summary.csv')
summary.to_csv(summary_path, index=False)

# Preparar plot: top 10 drivers por miles-logged promedio
top10 = summary.sort_values('miles-logged', ascending=False).head(10)
plt.figure(figsize=(8,6))
plt.bar(top10['driverId'].astype(str), top10['miles-logged'])
plt.xlabel('driverId')
plt.ylabel('avg miles-logged')
plt.title('Top 10 drivers by avg miles')
plt.tight_layout()
plot_path = os.path.join('files','plots','top10_drivers.png')
plt.savefig(plot_path)
plt.close()