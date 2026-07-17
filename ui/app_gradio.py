# ==============================================================================
# 13 Link - Interfaz Principal (Gradio)
# ==============================================================================

import gradio as gr
import sys
import os

# Ajuste para que Python encuentre los módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.image_cleaner import process_image
from modules.mesh_generator import generate_3d_model

def procesar_interfaz(imagen):
    """
    Paso 1: Recibe la imagen original y elimina el fondo.
    """
    if imagen is None:
        return None
    return process_image(imagen)

def generar_3d_interfaz(imagen_limpia):
    """
    Paso 2: Toma la imagen limpia y genera el archivo STL.
    """
    if imagen_limpia is None:
        raise gr.Error("Por favor, elimina el fondo de una imagen primero.")
    
    # Llama a la función del generador, que devuelve la ruta del archivo local
    ruta_archivo = generate_3d_model(imagen_limpia, output_format="stl")
    return ruta_archivo

# Definimos la estructura de la interfaz
with gr.Blocks(title="13 Link - Generador 3D", theme=gr.themes.Base()) as app:
    
    # Encabezado
    gr.Markdown("# 13 Link | Estudio de Creación 3D")
    gr.Markdown("Transforma imágenes 2D en modelos 3D listos para descargar (STL). Todo el procesamiento es 100% local.")
    
    with gr.Row():
        # Columna 1: Entrada y Limpieza
        with gr.Column():
            gr.Markdown("### Paso 1: Preparar la Imagen")
            imagen_entrada = gr.Image(label="Imagen Original", type="pil", interactive=True)
            boton_limpiar = gr.Button("Eliminar Fondo", variant="secondary")
            
        # Columna 2: Generación 3D
        with gr.Column():
            gr.Markdown("### Paso 2: Generar Malla 3D")
            imagen_salida = gr.Image(label="Imagen Procesada", type="pil", interactive=False)
            boton_generar = gr.Button("Generar Archivo STL", variant="primary")
            
        # Columna 3: Resultado Visual
        with gr.Column():
            gr.Markdown("### Resultado")
            # gr.Model3D permite previsualizar e incluye un ícono de descarga
            modelo_salida = gr.Model3D(
                label="Modelo 3D Final", 
                clear_color=[0.0, 0.0, 0.0, 0.0]
            )
            
    # Conexiones de los botones
    boton_limpiar.click(
        fn=procesar_interfaz,
        inputs=imagen_entrada,
        outputs=imagen_salida
    )
    
    boton_generar.click(
        fn=generar_3d_interfaz,
        inputs=imagen_salida,
        outputs=modelo_salida
    )

# Lanzar la aplicación
if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, debug=True)
