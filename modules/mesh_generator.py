# ==============================================================================
# 13 Link - Módulo de Generación 3D
# Core Philosophy: Linked. Not Modified.
# ==============================================================================

import torch
import trimesh
import logging
from PIL import Image
from tsr.system import TSR
from tsr.utils import resize_foreground
from core.memory_manager import manage_resources, unload_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@manage_resources
def generate_3d_model(clean_image: Image.Image, output_format: str = "stl") -> str:
    """
    Recibe una imagen sin fondo, reconstruye la geometría 3D usando TripoSR
    y exporta la malla al formato deseado.
    """
    logging.info("[Mesh Generator] Iniciando reconstrucción 3D...")
    
    # 1. Configuración de Hardware
    # Al tener memoria limitada, evitamos que PyTorch intente usar aceleración 
    # pesada que pueda colapsar el sistema.
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    logging.info(f"[Mesh Generator] Utilizando dispositivo: {device.upper()}")
    
    # 2. Carga del Modelo
    logging.info("[Mesh Generator] Cargando pesos del modelo (esto puede tomar un momento)...")
    model = TSR.from_pretrained(
        "stabilityai/TripoSR", 
        config_name="config.yaml", 
        weight_name="model.ckpt"
    )
    # Movemos el modelo a la memoria (RAM o VRAM dependiendo del dispositivo)
    model.to(device)
    
    try:
        # 3. Preprocesamiento de la imagen
        # TripoSR requiere que el objeto ocupe un porcentaje específico del lienzo
        logging.info("[Mesh Generator] Ajustando proporciones de la imagen...")
        img_resized = resize_foreground(clean_image, 0.85)
        
        # 4. Inferencia 3D (El cuello de botella de memoria)
        with torch.no_grad():
            logging.info("[Mesh Generator] Generando nube de puntos y malla...")
            scene_codes = model(img_resized, device=device)
            meshes = model.extract_mesh(scene_codes)
            mesh = meshes[0] # Tomamos la primera malla generada
        
        # 5. Procesamiento y Exportación
        output_filename = f"13link_model_output.{output_format}"
        logging.info(f"[Mesh Generator] Convirtiendo geometría a formato {output_format.upper()}...")
        
        # Extraemos los vértices y las caras (polígonos) del tensor de PyTorch
        vertices = mesh.v.cpu().numpy()
        faces = mesh.f.cpu().numpy()
        
        # Construimos el objeto Trimesh para la exportación final
        trimesh_obj = trimesh.Trimesh(vertices=vertices, faces=faces)
        trimesh_obj.export(output_filename)
        
        logging.info(f"[Mesh Generator] ¡Éxito! Archivo guardado localmente como: {output_filename}")
        
    except Exception as e:
        logging.error(f"[Mesh Generator] Error crítico durante la generación: {e}")
        raise e
        
    finally:
        # 6. Destrucción del modelo
        # Esto es vital: quitamos el modelo pesado de la memoria RAM inmediatamente
        unload_model(model)
        
    return output_filename
