import os
import cv2

def extract_frames(video_path, save_folder, interval_seconds):
    """
    Extrae fotogramas de un video cada 'interval_seconds' segundos y los guarda en 'save_folder'.
    """
    # Asegurar que el directorio existe
    os.makedirs(save_folder, exist_ok=True)
    
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"No se pudo abrir el video: {video_path}")
        
    frame_count = 0
    extracted_frames = []
    
    # Obtener FPS del video
    fps = int(round(video.get(cv2.CAP_PROP_FPS)))
    
    # Calcular intervalo de fotogramas en base al FPS
    frame_interval = int(fps * interval_seconds)
    
    print(f"FPS del video: {fps}")
    print(f"Intervalo de fotogramas: {frame_interval} (1 fotograma cada {interval_seconds} segundos)")
    
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
    """
    Aplica la regla de los tercios a una imagen y guarda el resultado.
    """
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