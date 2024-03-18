import pandas as pd
import re

# Función para limpiar los nombres de las columnas
def limpiar_nombre_columna(nombre):
    # Reemplazar espacios por guiones bajos
    nombre = nombre.replace(" ", "_")
    # Reemplazar / por guiones bajos (o cualquier otro reemplazo deseado)
    nombre = nombre.replace("/", "_")
    # Eliminar otros caracteres especiales si es necesario
    nombre = re.sub(r"[^a-zA-Z0-9_]", "", nombre)
    return nombre

# Cargar los CSV
df_actual = pd.read_csv('proyectos_mef.csv')
df_nuevo = pd.read_csv('INVIERTE_2017_29febrero2024_Analisis_rev.csv')

# Aplicar la limpieza a los nombres de las columnas del DataFrame nuevo
df_nuevo.columns = [limpiar_nombre_columna(col) for col in df_nuevo.columns]

# Identificar columnas existentes y nuevas
columnas_existentes = df_actual.columns.intersection(df_nuevo.columns)
columnas_nuevas = df_nuevo.columns.difference(df_actual.columns)

print("Columnas existentes que se actualizarán:", columnas_existentes.tolist())
print("Columnas nuevas a agregar:", columnas_nuevas.tolist())

# Preparar el SQL para agregar las nuevas columnas, asumiendo VARCHAR como tipo de dato genérico
sql_agregar_columnas = ""
for columna in columnas_nuevas:
    sql_agregar_columnas += f"ALTER TABLE observatorio_v2.proyectos_mef_temp ADD COLUMN {columna} VARCHAR(255);\n"

print("SQL para agregar nuevas columnas:\n", sql_agregar_columnas)

# Generar SQL para actualizar las filas existentes
clave_unica = 'cod_unico'  # Asegúrate de que este sea el nombre correcto de tu clave única

sql_actualizaciones = []
for indice, fila in df_nuevo.iterrows():
    fila_actual = df_actual.loc[df_actual[clave_unica] == fila[clave_unica]]
    if not fila_actual.empty:  # Asegurarse de que se encontró una coincidencia
        actualizaciones = ', '.join([f"{col} = '{fila[col]}'" for col in columnas_existentes if col != clave_unica and pd.notnull(fila[col]) and fila[col] != fila_actual[col].values[0]])
        if actualizaciones:
            sql = f"UPDATE observatorio_v2.proyectos_mef_temp SET {actualizaciones} WHERE {clave_unica} = '{fila[clave_unica]}';"
            sql_actualizaciones.append(sql)

# Nombre del archivo de salida
nombre_archivo = 'actualizaciones_sql2.txt'

# Abrir el archivo en modo de escritura
with open(nombre_archivo, 'w', encoding = 'utf-8') as archivo:
    # Escribir el SQL para agregar nuevas columnas
    archivo.write("SQL para agregar nuevas columnas:\n")
    archivo.write(sql_agregar_columnas + "\n")

    # Escribir el SQL de actualización para las filas existentes
    archivo.write("SQL para actualizar las filas existentes:\n")
    for sql in sql_actualizaciones:
        archivo.write(sql + "\n")

print(f"Las instrucciones SQL se han guardado en '{nombre_archivo}'.")
