import pandas as pd
import glob
from pathlib import Path
from charset_normalizer import from_path


def cargar_datos_csv(ruta_carpeta:str, pref:str = None , suf:list = None, chunk_size:int = 10000, metadata:bool = False) -> tuple:
    """
    Carga múltiples archivos CSV desde una carpeta en dataframes de pandas.
    Si los archivos son grandes, los procesa en chunks para evitar problemas de memoria.
    Args:
        ruta_carpeta (str): Ruta de la carpeta que contiene los archivos CSV.
        pref (str | None): Prefijo para los nombres de los dataframes. Si es None, se usa el nombre del archivo.
        suf (list | None): Sufijos para los nombres de los dataframes. Si es None, se usa un índice numérico.
        chunk_size (int): Tamaño del chunk para leer archivos grandes.
        metadata (bool): Si es True, imprime metadatos de cada dataframe cargado.
    Returns:
        dict: Diccionario con nombres de dataframes como claves y los dataframes como valores.
        Si metadata es True, devuelve una tupla (dataframes, metadatos) donde metadatos es otro diccionario con información adicional.
    """
    archivos_csv = glob.glob(f"{ruta_carpeta}/*.csv")
    dataframes = {}
    metadatos = {}
    
    # Ajustar sufijos
    suf = [str(sufijo) for sufijo in suf]
    
    # Si no se proporcionan sufijos, usar índices
    if suf is None:
        suf = range(len(archivos_csv))
    elif len(suf) < len(archivos_csv):
        # Completar con índices a partir del ultimo sufijo dado si hay menos sufijos que archivos
        for i in range(1,len(archivos_csv) - len(suf)+1):
            suf.append(suf[-1] + f"_{i}")
    
    for i,archivo in enumerate(archivos_csv):
        # Generar nombre del dataframe
        # Si no hay prefijo usar nombre del archivo sin extensión
        if pref is not None:
            nombre = f"{pref}_{suf[i]}"
        else:
            nombre = archivo.split('/')[-1].replace('.csv', '')
        
        try:
            # Leer todo el archivo si es pequeño
            tamaño = Path(archivo).stat().st_size / (1024 * 1024)  # MB
            # Detectar la codificación del archivo
            encoding = encoding_detect(archivo)
            
            if tamaño < 100:  # Si es menor a 100MB, cargar completo
                dataframes[nombre] = pd.read_csv(archivo, encoding=encoding)
            else:
                # Para archivos grandes, procesar por chunks
                chunks = []
                for chunk in pd.read_csv(archivo,encoding=encoding, chunksize=chunk_size):
                    chunks.append(chunk)
                dataframes[nombre] = pd.concat(chunks, ignore_index=True)
            if metadata:
                # Recopilar metadatos
                metadatos[nombre] = {
                    'rows': len(dataframes[nombre]),
                    'columns': len(dataframes[nombre].columns),
                    'columns_list': list(dataframes[nombre].columns),
                    'memory_size': dataframes[nombre].memory_usage(deep=True).sum()/(1024*1024),  # en MB
                    'file_path': archivo,
                    'encoding': encoding
                }
            
        except Exception as e:
            print(f"✗ Error en {nombre}: {e}")

    return dataframes, metadatos

def encoding_detect(file_path: str, steps: int = 10) -> str:
    """
    Detecta la codificación de un archivo de texto leyendo las primeras n líneas.
    Args:
        file_path (str): Ruta del archivo de texto.
        steps (int): Número de divisiones a realizar al archivo para su analisis estadistico.
    Returns:
        str: Codificación  detectada del archivo.
    """

    result = from_path(file_path,steps=steps,cp_isolation=['utf_8','utf_16','latin_1','cp1252','iso-8859-1','cp1250'])
    best_guess = result.best()
    return best_guess.encoding