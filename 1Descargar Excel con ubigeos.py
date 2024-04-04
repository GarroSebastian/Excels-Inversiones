from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime
import time
# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Obtener el año actual
anio_actual = datetime.datetime.now().year

# Formatear la nueva fecha con el año actual
fecha_con_anio_actual = f"01/01/{anio_actual}"
fechafin_con_anio_actual = f"31/12/{anio_actual}"
# Navigate to the web page
driver.get('https://ofi5.mef.gob.pe/inviertePub/ConsultaPublica/ConsultaAvanzada')

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'optIngr')))

# Click on the radial button
driver.find_element(By.ID,'optIngr').click()

# Click on the box that appears and write the date of the first month of the current year
driver.find_element(By.ID, 'txtIniInvierte').click()
driver.find_element(By.ID,'txtIniInvierte').clear()
driver.find_element(By.ID,'txtIniInvierte').send_keys(fecha_con_anio_actual)

# Click on the box next to the one where the date was written previously and write the date of the last month of the current year.
driver.find_element(By.ID,'txtFinInvierte').click()
driver.find_element(By.ID,'txtFinInvierte').clear()
driver.find_element(By.ID,'txtFinInvierte').send_keys(fechafin_con_anio_actual)


# Clickon the button at the bottom of the page that says "Buscar"
driver.find_element(By.ID,'butBuscar').click()

# Wait for the page to load
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'butExportar01')))

# Click on the button that says "Exportar con Ubigeos"
driver.find_element(By.ID,'butExportar01').click()

# Wait for the file to download
WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, 'divLoad')))

# Get the downloaded file name
# Define la carpeta de descargas
download_folder = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
print(download_folder)


# Lista todos los archivos en el directorio de descargas y obtén sus fechas de modificación
files_with_dates = [(filename, os.path.getmtime(os.path.join(download_folder, filename))) for filename in os.listdir(download_folder)]

# Ordena los archivos por fecha de modificación, del más reciente al más antiguo
files_sorted_by_date = sorted(files_with_dates, key=lambda x: x[1], reverse=True)

if files_sorted_by_date:
    # Elige el archivo más reciente
    most_recent_file, _ = files_sorted_by_date[0]
    file_name = most_recent_file
    print(f"El archivo más reciente es: {file_name}")

    # Completa el proceso de mover y renombrar el archivo aquí
    source_file = os.path.join(download_folder, file_name)
    destination_folder = 'C:\\Colaboraccion\\Excels Inversiones'
    destination_file = os.path.join(destination_folder, f'Inversiones_{datetime.date.today().strftime("%B_%Y")}.xlsx')
    os.replace(source_file, destination_file)
else:
    print("No se encontraron archivos en la carpeta de descargas.")

# Close the webdriver
driver.quit()