# py_functions

Este directorio contiene funciones auxiliares utilizadas por `Main.py`.

## Módulos

### `video_processing.py`

- **Dependencias**:
  - `cv2`
  - `os`
- `extract_frames(video_path, output_folder, frame_interval)`: Extrae fotogramas de un video a intervalos especificados.
- `apply_rule_of_thirds(image_path)`: Aplica la regla de los tercios a una imagen.

### `visual_api.py`

- **ESTE MODULO REQUIERE DE UNA CLAVE DE OPENAI (API key)**
- Se puede conseguir en [OpenAI API](https://openai.com/index/openai-api/)

- **Dependencias**:
  - `openai`
  - `os`
- `analyze_with_openai(encoded_image, prompt, current_frame, total_frames)`: Analiza una imagen utilizando la API de OpenAI.
- `generate_openai_report(responses)`: Genera un informe resumen basado en las respuestas obtenidas.

### `report_generator.py`

- **Dependencias**:
  - `fpdf2` 
  - `os`
- `generate_pdf(responses, output_folder, report, output_filename)`: Genera un informe PDF con los análisis y las imágenes.
- `generate_txt(response_text, frame_file)`: Crea un informe en formato de texto.

### `frame_api_encoder.py`

- **Dependencias**:
  - `base64`
- `encode_image(image_path)`: Codifica una imagen en base64 para su envío a la API.

## Uso

Estas funciones son importadas en `Main.py` y se encargan de distintas tareas como procesamiento de video, interacción con la API y generación de informes.