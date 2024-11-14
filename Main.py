import os
import cv2
import base64
from fpdf import FPDF, XPos, YPos
from openai import OpenAI
import re

os.environ['OPENAI_API_KEY'] = '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'

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuración inicial
video_path = 'BladeRunner2049_LasVegas.mp4'
output_frame_folder = 'frames/'
responses = []
prompt_analisis = ""
prompt_contexto_narrativo = ""

# Crear un objeto PDF
pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')
pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf')


# Guarda el text del prompt (archivo Prompt_Analisis_Composicion_Visual.md) en una variable
with open("Prompt_Analisis_Composicion_Visual.md", "r", encoding="utf-8") as file:
    prompt_analisis = file.read()

# Guarda el text del prompt (archivo Prompt_Contexto_Narrativo.md) en una variable
with open("Prompt_Contexto_Narrativo.md", "r", encoding="utf-8") as file:
    prompt_contexto_narrativo = file.read()
    
def extract_frames(video_path, save_folder, interval_seconds):
    # Asegurar que el directorio existe
    os.makedirs(save_folder, exist_ok=True)
    
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"No se pudo abrir el video: {video_path}")
        
    frame_count = 0
    extracted_frames = []
    
    # Obtener FPS del video
    fps = int(round(video.get(cv2.CAP_PROP_FPS)))
    
    # Calcular intervalo de frames en base al FPS
    frame_interval = int(fps * interval_seconds)
    
    print(f"FPS del video: {fps}")
    print(f"Intervalo de frames: {frame_interval} (1 frame cada {interval_seconds} segundos)")
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_filename = f"frame_{frame_count}.jpeg"
            frame_path = os.path.join(save_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            # Calcular el tiempo en segundos
            timestamp = frame_count / fps
            extracted_frames.append((frame_filename, timestamp))
        frame_count += 1
    
    video.release()
    return extracted_frames

def apply_rule_of_thirds(image_path):
    
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Draw the rule of thirds grid
    cv2.line(image, (width // 3, 0), (width // 3, height), (0, 255, 0), 2)
    cv2.line(image, (2 * width // 3, 0), (2 * width // 3, height), (0, 255, 0), 2)
    cv2.line(image, (0, height // 3), (width, height // 3), (0, 255, 0), 2)
    cv2.line(image, (0, 2 * height // 3), (width, 2 * height // 3), (0, 255, 0), 2)

    # Save the image with the grid
    analyzed_image_path = image_path.replace("frame", "analyzed_frame")

    # Create the output folder if it doesn't exist
    os.makedirs(os.path.dirname(analyzed_image_path), exist_ok=True)

    cv2.imwrite(analyzed_image_path, image)
    return analyzed_image_path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
    return image

def analyze_with_openai(encoded_image, prompt, current_frame, total_frames):

    # Calculate progress percentage
    progress = (current_frame / total_frames) * 100 if total_frames > 0 else 0
        
    # Estimated cost per call (adjust based on your model's pricing)
    estimated_cost = 0.01  # $0.01 per image analysis
        
    print(f"Procesando frame {current_frame}/{total_frames} ({progress:.1f}%)")
    print(f"Costo estimado acumulado: ${(current_frame + 1) * estimated_cost:.2f}")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {
                "role": "system",
                "content": [
                {
                    "type": "text",
                    "text": prompt }
                ]
            },
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "Analiza esta imagen y asegurate de seguir el system prompt"
                }
                ]
            },
            {
                "role": "user",
                "content": [
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}",
                    "detail": "auto"
                    }
                }
                ]
            }
            ],
            temperature=.8,
            max_tokens=500,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=.5,
            response_format={
            "type": "text"
            }
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("Error en la llamada a la API de OpenAI:", e)
        return None
        

def generate_pdf(responses, output_folder, report, output_filename="analysis_report.pdf"):
    pdf.set_font('DejaVu', '', 9)
    
    line_height = 10
    
    for item in responses:
        frame_path = os.path.join(output_folder, item['frame'])
        
        # Add frame filename and timestamp
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(0, line_height, text=f"Frame: {item['frame']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, line_height, text=f"Timestamp: {item['timestamp']} seconds", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('DejaVu', '', 9)
        
        if os.path.exists(frame_path):
            pdf.image(frame_path, x=10, y=None, w=pdf.w - 20)
        else:
            pdf.cell(0, line_height, text="Image not found.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.multi_cell(0, line_height, text=item['analysis'], align='L', markdown=True)
        pdf.ln(2) # Add some space between frames   

    # Add the summary
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, line_height, text="Resumen del fragmento analizado", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('DejaVu', '', 9)
    pdf.multi_cell(0, line_height, text=report, align='L', markdown=True)

    pdf.output(output_filename)
    print(f"PDF generado en: ./{output_filename}")

def generate_txt(response_text, frame_file):
    with open("analysis_report.md", "a", encoding="utf-8") as file:
        file.write(f"Frame {frame_file}: {response_text}\n\n")

def generate_openai_report(responses):

    # Transformar la lista de respuestas en un solo string
    full_text = "\n".join([f"Frame {item['frame']}: {item['analysis']}" for item in responses])

    try:
        report = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {
                "role": "system",
                "content": [
                {
                    "type": "text",
                    "text": "A continuación se muestra los análisis realizados en los frames de un video, has de resumir y sacar conlusiones de los análisis realizados. Has de ser bastante breve: "
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": full_text
                }
                ]
            },
            ],
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
            "type": "text"
            }
        )
        return report.choices[0].message.content
    except Exception as e:
        print("Error en la llamada a la API de OpenAI:", e)
        return None


def main():

    frame_interval = 6
    extracted_frames = extract_frames(video_path, output_frame_folder, frame_interval)

    # Contar el número de llamadas a la API que se realizarán
    num_api_calls = len(extracted_frames)
    print(f"Total de llamadas a la API que se realizarán: {num_api_calls}")

    # Pedir confirmación al usuario
    proceed = input("¿Deseas continuar con el envío de solicitudes a la API? (sí/no): ")
    if proceed.lower() not in ['sí', 'si', 's']:
        print("Operación cancelada por el usuario.")
        return  # Salir de la función main

    for frame_file, timestamp in extracted_frames:
        frame_path = os.path.join(output_frame_folder, frame_file)
        analyzed_frame_path = apply_rule_of_thirds(frame_path)
        encoded_image = encode_image(analyzed_frame_path)
        previous_response = responses[-1]['analysis'] if responses else ""
        prompt = f""""{prompt_analisis}
                      {prompt_contexto_narrativo}
                      ## Frame actual y respuesta anterior
                      Frame actual: {frame_file}
                      Respuesta anterior: {previous_response}"""
        
        response_text = analyze_with_openai(encoded_image, prompt, len(responses) + 1, num_api_calls)
        responses.append({'frame': frame_file, 'timestamp': timestamp, 'analysis': response_text})

        # Create a txt file if it doesnt exist. If it exists append
        generate_txt(response_text, frame_file)

    report = generate_openai_report(responses)

    generate_pdf(responses, output_frame_folder, report, output_filename="analysis_report.pdf")

if __name__ == "__main__":
    main()
