import os
from fpdf import FPDF, XPos, YPos

pdf = FPDF()
pdf.add_page()
pdf.add_font('pdf_font', '', './pdf_fonts/fuente.ttf')
pdf.add_font('pdf_font', 'B', './pdf_fonts/fuente-Bold.ttf')

def generate_pdf(responses, output_folder, report, output_filename="analysis_report.pdf"):
    """
    Genera un informe PDF que contiene los análisis e imágenes.
    """
    pdf.set_font('pdf_font', '', 9)
    
    line_height = 10
    
    for item in responses:
        frame_path = os.path.join(output_folder, item['frame'])
        
        # Add frame filename and timestamp
        pdf.set_font('pdf_font', 'B', 12)
        pdf.cell(0, line_height, text=f"Frame: {item['frame']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, line_height, text=f"Timestamp: {item['timestamp']} seconds", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('pdf_font', '', 9)
        
        if os.path.exists(frame_path):
            pdf.image(frame_path, x=10, y=None, w=pdf.w - 20)
        else:
            pdf.cell(0, line_height, text="Image not found.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.multi_cell(0, line_height, text=item['analysis'], align='L', markdown=True)
        pdf.ln(2) # Añade un espacio en blanco entre los análisis  

    # Añadir un resumen del fragmento analizado
    pdf.add_page()
    pdf.set_font('pdf_font', 'B', 12)
    pdf.cell(0, line_height, text="Resumen del fragmento analizado", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('pdf_font', '', 9)
    pdf.multi_cell(0, line_height, text=report, align='L', markdown=True)

    # Guardar el PDF
    pdf.output('./program_output/' + output_filename)
    print(f"PDF generado en:" + os.path.abspath('./program_output/' + output_filename))

def generate_txt(response_text, frame_file):
    """
    Genera un informe en formato markdown con los análisis de los fotogramas.
    """
    with open("./program_output/analysis_report.md", "a", encoding="utf-8") as file:
        file.write(f"Frame {frame_file}: {response_text}\n\n")