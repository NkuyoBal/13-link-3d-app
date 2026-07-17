# ==============================================================================
# 13 Link - Módulo de Limpieza de Imagen
# ==============================================================================

from PIL import Image
from rembg import remove, new_session
from core.memory_manager import manage_resources, unload_model
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@manage_resources
def process_image(input_image: Image.Image) -> Image.Image:
    """
    Recibe una imagen (PIL.Image), elimina el fondo usando un modelo de IA 
    ultraligero y retorna la imagen limpia lista para el procesamiento 3D.
    """
    logging.info("[Image Cleaner] Iniciando extracción de fondo...")
    
    # Inicializamos la sesión con 'u2netp'. 
    # Es una versión comprimida del modelo U2Net, perfecta para sistemas limitados.
    session = new_session("u2netp")
    
    try:
        # Ejecutar la eliminación de fondo
        output_image = remove(input_image, session=session)
        logging.info("[Image Cleaner] Extracción completada con éxito.")
        
    except Exception as e:
        logging.error(f"[Image Cleaner] Error durante el procesamiento: {e}")
        raise e
        
    finally:
        # Garantizamos que el modelo se descargue de la memoria, incluso si hay un error
        unload_model(session)
        
    return output_image

# Bloque de prueba local
if __name__ == "__main__":
    # Si ejecutas este script directamente, intentará limpiar una imagen de prueba
    try:
        img_prueba = Image.open("prueba.jpg") # Asegúrate de tener una imagen llamada así
        img_limpia = process_image(img_prueba)
        img_limpia.save("prueba_limpia.png")
        print("Imagen guardada como prueba_limpia.png")
    except FileNotFoundError:
        print("Para probar localmente, coloca una imagen llamada 'prueba.jpg' en esta carpeta.")
