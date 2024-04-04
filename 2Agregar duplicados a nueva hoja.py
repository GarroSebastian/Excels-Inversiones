import pandas as pd
import datetime

# Ruta al archivo Excel
archivo_excel = f'Inversiones_{datetime.date.today().strftime("%B_%Y")}.xlsx'
# Nombre de la hoja donde están los datos
hoja_nombre = "Resultados"

# Cargar los datos desde el archivo Excel
df = pd.read_excel(archivo_excel, sheet_name=hoja_nombre, header=5)

# Definir el nuevo orden de las columnas según tu actualización
columnas_ordenadas = [
    "#", "Código único de inversión", "Con SNIP", "Código SNIP", "Duplicidad", "Nombre de la inversión",
    "Monto viable", "Función", "Programa", "Subprograma", "Situación", "Estado de la inversión",
    "Tipo de desactivacion", "Nivel de gobierno", "Sector", "Entidad", "Unidad OPMI", "Unidad UEI",
    "Unidad UF", "Responsable OPMI", "Responsable UEI", "Responsable UF", "Entidad OPI", "Responsable OPI",
    "Ejecutora", "Fecha de registro", "Año", "Último estudio", "Estado del estudio", "Nivel de viabilidad",
    "Responsable de viabilidad", "Fecha de viabilidad", "Con F15", "Con F14", "Monto F15", "Monto F16",
    "Monto F17", "Costo actualizado", "Costo actualizado Perfil", "Costo actualizado Exp. Tec.",
    "Descripción de la alternativa", "Beneficiarios", "PIA año vigente", "PIM año vigente",
    "Devengado año vigente", "Devengado acumulado", "Cerrado", "Marco", "Tipo de formato",
    "Devengado acumulado año anterior", "Saldo por financiar", "Mes/año primer devengado",
    "Mes/año último devengado", "Incluido programación PMI", "Incluido ejecución PMI", "Ganador FONIPREL",
    "Código Convenio", "Tipo de convenio", "N° de convenio", "Encargado del convenio",
    "Encargante del convenio", "Fecha de inicio de convenio", "Fecha de término de convenio",
    "Fecha de registro de convenio", "Estado del convenio", "Registro Cierre", "Departamento",
    "Provincia", "Distrito", "Centro Poblado", "Ubigeo"
]

# Agregar las columnas faltantes en el DataFrame con valores vacíos
for columna in columnas_ordenadas:
    if columna not in df.columns:
        df[columna] = pd.NA  # Puedes usar None o np.nan según tu preferencia

# Reordenar el DataFrame según el nuevo orden de columnas y agregar columnas extras al final
df = df.reindex(columns=(columnas_ordenadas + [col for col in df.columns if col not in columnas_ordenadas]))


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
