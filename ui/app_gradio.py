# ==============================================================================
# 13 Link - Interfaz Principal (Gradio)
# ==============================================================================

import gradio as gr
import sys
import os

# Ajuste para que Python encuentre los módulos internos si se ejecuta desde la carpeta ui/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.image_cleaner import process_image

def procesar_interfaz(imagen):
    """
    Función puente entre la UI de Gradio y nuestro core lógico.
    """
    if imagen is None:
        return None
    
    # Llamamos a nuestra función envuelta en el gestor de memoria
    imagen_limpia = process_image(imagen)
    return imagen_limpia

# Definimos el tema visual y la estructura de la interfaz
with gr.Blocks(title="13 Link - Generador 3D", theme=gr.themes.Base()) as app:
    
    # Encabezado
    gr.Markdown("# 13 Link | Estudio de Creación 3D")
    gr.Markdown("Sube una imagen para remover el fondo automáticamente. Este es el primer paso antes de generar la malla 3D.")
    
    with gr.Row():
        # Columna Izquierda: Entrada
        with gr.Column():
            imagen_entrada = gr.Image(label="Imagen Original", type="pil", interactive=True)
            boton_limpiar = gr.Button("Eliminar Fondo", variant="primary")
            
        # Columna Derecha: Salida
        with gr.Column():
            imagen_salida = gr.Image(label="Imagen Procesada (Lista para 3D)", type="pil", interactive=False)
            
    # Conectamos el botón con la función
    boton_limpiar.click(
        fn=procesar_interfaz,
        inputs=imagen_entrada,
        outputs=imagen_salida
    )

# Bloque de ejecución principal
if __name__ == "__main__":
    # Lanzamos el servidor local
    # debug=True ayuda a ver errores en la consola
    app.launch(server_name="127.0.0.1", server_port=7860, debug=True)
