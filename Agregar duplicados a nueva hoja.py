import pandas as pd
import datetime

# Ruta al archivo Excel
archivo_excel = f'Inversiones_{datetime.date.today().strftime("%B_%Y")}.xlsx'
# Nombre de la hoja donde están los datos
hoja_nombre = "Resultados"

# Cargar los datos desde el archivo Excel
df = pd.read_excel(archivo_excel, sheet_name=hoja_nombre, header=5)

# Añadir la columna 'Año' extrayendo el año de la 'Fecha de registro'
df['Año'] = pd.to_datetime(df['Fecha de registro'], errors='coerce').dt.year

# Inicializar las nuevas columnas con 0 y asegurar el tipo de dato correcto
df['Costo actualizado Perfil'] = 0.0
df['Costo actualizado Exp. Tec.'] = 0.0

# Llenar las nuevas columnas según las condiciones dadas
df.loc[df['Con F15'] == 1, 'Costo actualizado Perfil'] = df['Monto F16'].astype(float)
df.loc[df['Con F15'] == 0, 'Costo actualizado Exp. Tec.'] = df['Monto F16'].astype(float)

# Proceder con la búsqueda y eliminación de duplicados, y guardar los resultados como antes
duplicados = df[df.duplicated(subset=["Código único de inversión"], keep=False)]
df_sin_duplicados = df.drop_duplicates(subset=["Código único de inversión"], keep=False)

if not duplicados.empty:
    try:
        # Utilizar ExcelWriter para guardar los cambios
        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='w') as writer:
            # Guardar el DataFrame sin duplicados en la hoja 'Resultados', reemplazando su contenido
            df_sin_duplicados.to_excel(writer, sheet_name=hoja_nombre, index=False)
            # Guardar duplicados en una nueva hoja 'Duplicados'
            duplicados.to_excel(writer, sheet_name='Duplicados', index=False)
        print("Las filas duplicadas se han movido a la hoja 'Duplicados'. La hoja 'Resultados' ha sido actualizada con las nuevas columnas.")
    except Exception as e:
        print(f"No se pudo actualizar el archivo Excel. Error: {e}")
else:
    print("No se encontraron filas duplicadas.")
