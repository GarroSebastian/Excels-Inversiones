import pandas as pd

# Nombres de archivo
archivo_existente = 'INVIERTE_2017_29febrero2024_Analisis_rev.xlsx'
archivo_nuevo = 'Inversiones_March_2024.xlsx'
hoja_nombre = 'Resultados'

# Leer los archivos Excel considerando que las cabeceras están en la fila 6
df_existente = pd.read_excel(archivo_existente, sheet_name='Data', header=8)
df_nuevo = pd.read_excel(archivo_nuevo, sheet_name=hoja_nombre)

print(df_existente.columns)
print(df_nuevo.columns)


# Asegurarse de que ambas DataFrames tengan el mismo orden de columnas basado en los nombres de las cabeceras
# Esto es importante si planeas combinar o actualizar datos basados en estas cabeceras
df_nuevo = df_nuevo.reindex(columns=df_existente.columns)

# Combinar los datos
# Si quieres añadir nuevas filas del df_nuevo a df_existente basándose en "Código único de inversión":
df_combinado = pd.merge(df_existente, df_nuevo, on="Código único de inversión", how="outer", suffixes=('', '_nuevo'))

# O, si quieres actualizar los valores existentes en df_existente con los valores de df_nuevo:
# Nota: Esto reemplazará los valores en df_existente con cualquier valor coincidente en df_nuevo.
# df_existente.update(df_nuevo)

# Guardar el DataFrame resultante en un nuevo archivo Excel
df_combinado.to_excel('Archivo_Combinado.xlsx', index=False, header=True)
