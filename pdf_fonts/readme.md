# Cómo Cambiar la fuente por defecto del pdf generado

Para cambiar la fuente del pdf exportado, sigue estos pasos:
1. **Añade una nueva fuente**:
    - Añade en esta carpeta dos archivos, uno con la fuente negrita y otro normal.

2. **Como cambiar la fuente**: 
    - Hay dos maneras:
    1. Cambiando el nombre de las nuevas fuentes:
        - Fuente normal -> `fuente.ttf`
        - **Fuente negrita** -> `fuente-Bold.ttf`
            
    2. Cambiando el código de `report_generator.py`:
        - Busca las líneas `add_font`
            
        2.2 **Modificando el archivo `report_generator.py`**:
        Sigue estos pasos para cambiar el código:
        
        1. **Abre el archivo** `report_generator.py`
        
        2. **Localiza las líneas** donde se añaden las fuentes, que deberían verse similares a las siguientes:
            ```python
            pdf.add_font('pdf_font', '', '../pdf_fonts/fuente.ttf')
            pdf.add_font('pdf_font', 'B', '../pdf_fonts/fuente-Bold.ttf')
            ```
            
        3. **Actualiza las rutas** a los archivos de fuente si has movido o renombrado los archivos.
        
        4. **Si deseas utilizar una fuente diferente**, cambia el nombre de las fuentes y asegúrate de que las rutas sean correctas. Por ejemplo:
            ```python
            pdf.add_font('new_font', '', '../pdf_fonts/nueva_fuente.ttf')
            pdf.add_font('new_font', 'B', '../pdf_fonts/nueva_fuente-Bold.ttf')
            ```
        
        5. **Guarda los cambios** y ejecuta tu script para generar el PDF con las nuevas configuraciones de fuente.
