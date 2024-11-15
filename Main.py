"""
Este script extrae fotogramas de un archivo de video, los analiza usando la API de OpenAI y genera un informe PDF.
"""

import os

# Importar funciones de otros archivos
from py_functions.video_processing import extract_frames, apply_rule_of_thirds
from py_functions.visual_api import analyze_with_openai, generate_openai_report
from py_functions.report_generator import generate_pdf, generate_txt
from py_functions.frame_api_encoder import encode_image

# Obtener parámetros del usuario
video_path = os.path.join('video_input', input('Introduce el nombre del archivo de video (por ejemplo, video.mp4): '))
output_frame_folder = 'frames/'
# Obtener los prompts de análisis y contexto narrativo
prompt_analisis_file = "" # Ruta al archivo del prompt de análisis
prompt_contexto_narrativo = "" # Guardar el prompt de contexto narrativo (opcional)

prompt_analisis = "" # Prompt global (este combina los distintos prompts que guian al modelo)
responses = [] # Almacenar el análisis de cada fotograma

# Leer el prompt de análisis
prompt_analisis_file = os.path.join('fine-tunning_files', input('Introduce la ruta al archivo del prompt de análisis (obligatorio): '))

# Leer el prompt de contexto narrativo si se proporciona
prompt_contexto_narrativo_file = os.path.join('fine-tunning_files', input('Introduce la ruta al archivo del prompt de contexto narrativo (opcional, presiona Enter para omitir): '))

if prompt_contexto_narrativo_file != "fine-tunning_files\\":
    with open(prompt_contexto_narrativo_file, "r", encoding="utf-8") as file:
        prompt_contexto_narrativo = file.read()
else:
    print("Para mejorar la calidad de los análisis, se recomienda proporcionar un prompt de contexto narrativo.")


# Leer los prompts de los archivos
with open(prompt_analisis_file, "r", encoding="utf-8") as file:
    prompt_analisis = file.read()
    
def main():
    """
    Función principal para orquestar la extracción de fotogramas, análisis y generación de informes.
    """
    # Preguntar al usuario por la frecuencia con la que se extraerán los fotogramas
    frame_interval = int(input('Introduce el intervalo de captura de fotogramas en segundos: '))
    extracted_frames = extract_frames(video_path, output_frame_folder, frame_interval)

    # Contar el número de llamadas a la API que se realizarán
    num_api_calls = len(extracted_frames)
    print(f"Total de llamadas a la API que se realizarán: {num_api_calls}")

    # Pedir confirmación al usuario
    proceed = input(f"¿Deseas continuar con el envío de solicitudes a la API (Coste estimado: ${num_api_calls * 0.01:.2f})? (sí/no): ")

    if proceed.lower() not in ['sí', 'si', 's']:
        print("Operación cancelada por el usuario.")
        return  # Salir de la función main
    else:
        print(f"Procesando fotogramas...")

    # Procesar cada fotograma
    for frame_file, timestamp in extracted_frames:
        frame_path = os.path.join(output_frame_folder, frame_file)
        # Aplicar la regla de los tercios al fotograma para facilitar el análisis
        analyzed_frame_path = apply_rule_of_thirds(frame_path)
        # Codificar la imagen en base64 para enviarla a la API
        encoded_image = encode_image(analyzed_frame_path)
        # Incluye el fotograma actual y la respuesta anterior en el prompt
        previous_response = responses[-1]['analysis'] if responses else ""
        prompt = f""""{prompt_analisis}
                      {prompt_contexto_narrativo}
                      ## Frame actual y respuesta anterior
                      Frame actual: {frame_file}
                      Respuesta anterior: {previous_response}"""
        
        # Analizar la imagen con los modelos multimodales de OpenAI
        response_text = analyze_with_openai(encoded_image, prompt, len(responses) + 1, num_api_calls)
        # Guardar el resultado del análisis
        responses.append({'frame': frame_file, 'timestamp': timestamp, 'analysis': response_text})

        # Crea un informe en formato markdown
        generate_txt(response_text, frame_file)

    # Generar un informe resumen utilizando la API de OpenAI
    report = generate_openai_report(responses)

    # Generar un informe PDF con los análisis y las imágenes
    generate_pdf(responses, output_frame_folder, report, output_filename="analysis_report.pdf")

if __name__ == "__main__":
    main()
