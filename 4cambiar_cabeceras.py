import pandas as pd
import unidecode
import re

archivo_nuevo = 'Archivo_Combinado.xlsx'

df = pd.read_excel(archivo_nuevo, sheet_name='Sheet1')

# Función para limpiar los nombres de las columnas
def limpiar_nombre_columna(nombre):
    # Reemplaza espacios con guiones bajos y convierte a minúsculas
    nombre_limpio = nombre.replace(' ', '_').lower()
    # Elimina caracteres especiales
    nombre_limpio = re.sub(r'[°?/]', '', nombre_limpio)
    # Remueve tildes
    nombre_limpio = unidecode.unidecode(nombre_limpio)
    return nombre_limpio

# Aplicar la función a cada columna del DataFrame
df.columns = [limpiar_nombre_columna(col) for col in df.columns]

# Guardar el DataFrame con los nombres de columnas limpios
df.to_excel('Archivo_Combinado_Limpio.xlsx', index=False)
