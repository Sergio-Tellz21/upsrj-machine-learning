import os
import shutil
import pandas as pd
import numpy as np

# Ruta de la carpeta Descargas
def obtener_carpeta_descargas():
    ruta_config = os.path.expanduser("~/.config/user-dirs.dirs")

    if os.path.exists(ruta_config):
        with open(ruta_config, "r") as f:
            for linea in f:
                if linea.startswith("XDG_DOWNLOAD_DIR"):
                    ruta = linea.split("=")[1].strip().strip('"')
                    return os.path.expandvars(ruta)

    # Fallback si no existe el archivo
    return os.path.expanduser("~/Downloads")


RUTA_DESCARGAS = os.path.expanduser("~/Downloads")
os.makedirs(RUTA_DESCARGAS, exist_ok=True)



# Diccionario de carpetas y extensiones
EXTENSIONES = {
    "PDFs": [".pdf"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Musica": [".mp3", ".wav"],
    "Documentos": [".docx", ".txt", ".xlsx", ".pptx"],
    "Programas": [".exe", ".msi"],
    "Comprimidos": [".zip", ".rar"]
}

def obtener_extension(archivo):
    return os.path.splitext(archivo)[1].lower()

def organizar_archivos():
    archivos = []

    # Recolectar información de los archivos
    for archivo in os.listdir(RUTA_DESCARGAS):
        ruta = os.path.join(RUTA_DESCARGAS, archivo)
        if os.path.isfile(ruta):
            archivos.append({
                "nombre": archivo,
                "extension": obtener_extension(archivo),
                "ruta": ruta
            })

    # Crear DataFrame con pandas
    df = pd.DataFrame(archivos)

    if df.empty:
        print("No hay archivos para organizar")
        return

    # Usar numpy para manejar extensiones únicas
    extensiones_unicas = np.unique(df["extension"])

    for ext in extensiones_unicas:
        for carpeta, extensiones in EXTENSIONES.items():
            if ext in extensiones:
                ruta_carpeta = os.path.join(RUTA_DESCARGAS, carpeta)
                os.makedirs(ruta_carpeta, exist_ok=True)

                # Filtrar archivos con pandas
                archivos_filtrados = df[df["extension"] == ext]

                for _, fila in archivos_filtrados.iterrows():
                    destino = os.path.join(ruta_carpeta, fila["nombre"])
                    shutil.move(fila["ruta"], destino)

if __name__ == "__main__":
    organizar_archivos()
    print("✅ Organización completada usando pandas y numpy")
