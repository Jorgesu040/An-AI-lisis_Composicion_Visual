
# Py_Fundamentos_Comp_vis

Este proyecto extrae fotogramas de un archivo de video, los analiza usando los modelos de vision y lenguaje de OpenAI y genera un informe PDF.

## Estructura del Proyecto


- **Archivo** [`Main.py`](Main.py): Script principal que orquesta la extracción de fotogramas, análisis y generación de informes.
- **Carpeta** [`py_functions/`](py_functions/): Carpeta que contiene funciones auxiliares usadas por el script principal.

- **Carpeta** [`video_input/`](video_input/): Carpeta que contiene el archivo a analizar. El programa preguntará por el nombre del archivo en esa carpeta.

- **Carpetas** [`frames/`](frames/) y [`analized_frames/`](analized_frames/): Guardan, respectivamente, los fotogramas extraídos y los fotogramas con transformaciones que son enviados como 'input' al modelo para análisis.

- **Carpeta** [`fine-tunning_files`](fine-tunning_files): Contiene los archivos encargados de guiar al modelo en el análisis de la composición visual.


## Requisitos Previos

- Python 3.x
- Biblioteca `os`
- Biblioteca `openai`
- Otras dependencias (verificar los requisitos en cada módulo si es necesario, en el `readme` de la carpeta `py_functions/`)

## Configuración

1. Instala las dependencias necesarias:
    - En una terminal de python `pip install [package]`

2. Si las dependencias no se resuelven, reinicie el kernel de python con el commando en la terminal de python `exit`
   