import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = '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'
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_with_openai(encoded_image, prompt, current_frame, total_frames):
    """
    Analiza una imagen usando los modelos de vision de OpenAI y devuelve el texto de análisis.
    Utiliza los prompts de contexto narrativo y de análisis para el 'fine-tuning' del modelo.
    """
    # Calcular el progreso de la tarea en porcentaje
    progress = (current_frame / total_frames) * 100 if total_frames > 0 else 0
        
    # Costo estimado por llamada a la API de OpenAI
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
            # Parámetros de la API
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

def generate_openai_report(responses):
    """
    Genera un informe resumen que se añade al PDF 
    """
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