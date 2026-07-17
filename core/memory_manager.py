# ==============================================================================
# 13 Link - Core Memory Manager
# Utilidades para la gestión agresiva de memoria RAM y VRAM
# ==============================================================================

import gc
import psutil
import os
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_current_ram_usage():
    """
    Calcula la memoria RAM que está consumiendo el proceso actual de la aplicación.
    Retorna el valor en Megabytes (MB).
    """
    process = psutil.Process(os.getpid())
    # rss (Resident Set Size) es la memoria física que el proceso tiene en la RAM
    mem_mb = process.memory_info().rss / (1024 * 1024)
    return mem_mb

def free_memory():
    """
    Fuerza la liberación de memoria del sistema y de PyTorch.
    Debe llamarse después de completar cada paso pesado (ej. extraer fondo, generar malla).
    """
    # 1. Liberar caché de PyTorch (si aplica, útil para CPU o GPU)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    elif torch.backends.mps.is_available():
        torch.mps.empty_cache()
    
    # 2. Forzar al recolector de basura de Python a eliminar objetos huérfanos
    collected = gc.collect()
    
    logging.info(f"[Memory Manager] Recolección de basura ejecutada. Objetos eliminados: {collected}")
    logging.info(f"[Memory Manager] Uso actual de RAM: {get_current_ram_usage():.2f} MB")

def unload_model(model_variable):
    """
    Elimina explícitamente un modelo de IA de la memoria y limpia el entorno.
    
    Uso:
        modelo = cargar_modelo()
        resultado = modelo.procesar(imagen)
        unload_model(modelo)
    """
    try:
        del model_variable
    except NameError:
        pass
    
    free_memory()

# ==============================================================================
# Decorador de Gestión de Memoria
# ==============================================================================
def manage_resources(func):
    """
    Decorador para envolver funciones pesadas. Garantiza que la memoria
    se limpie automáticamente antes y después de que la función se ejecute.
    """
    def wrapper(*args, **kwargs):
        logging.info(f"Preparando entorno para: {func.__name__}...")
        free_memory() # Limpiar antes de empezar
        
        resultado = func(*args, **kwargs)
        
        logging.info(f"Proceso {func.__name__} finalizado. Limpiando memoria...")
        free_memory() # Limpiar después de terminar
        
        return resultado
    return wrapper
