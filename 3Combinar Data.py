import pandas as pd

# Rutas a los archivos Excel
archivo_existente = 'INVIERTE_2017_29febrero2024_Analisis_rev2.xlsx'
#cambiar cada mes nombre 
archivo_nuevo = 'Inversiones_April_2024.xlsx'

# Leer los datos del archivo existente y del archivo nuevo
df_existente = pd.read_excel(archivo_existente, sheet_name='Data', header=8)
df_nuevo = pd.read_excel(archivo_nuevo, sheet_name='Resultados')

# Unificar las columnas de ambos DataFrames
columnas_unificadas = df_existente.columns.tolist() + [col for col in df_nuevo.columns if col not in df_existente.columns]

# Reordenar las columnas del DataFrame nuevo para que coincidan con el DataFrame existente y añadir nuevas columnas
df_nuevo = df_nuevo.reindex(columns=columnas_unificadas)

# Concatenar ambos DataFrames
df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo Excel
df_combinado.to_excel('Archivo_Combinado.xlsx', index=False)
