import os
import sys

def elegir_archivo(carpeta="mundos"):
    """
    Lista los archivos .txt disponibles en la carpeta especificada
    y permite al usuario seleccionar uno mediante un número.
    
    Args:
        carpeta (str): Ruta de la carpeta donde buscar archivos
        
    Returns:
        str: Ruta completa del archivo seleccionado
    """
    if not os.path.exists(carpeta):
        print(f"Error: La carpeta '{carpeta}' no existe.")
        sys.exit(1)
    
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.txt')]
    
    if not archivos:
        print(f"No se encontraron archivos .txt en '{carpeta}'.")
        sys.exit(1)
    
    print("\n=== Archivos de mundo disponibles ===")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}) {archivo}")
    
    while True:
        seleccion = input(f"\nSelecciona un archivo (1-{len(archivos)}): ").strip()
        try:
            indice = int(seleccion) - 1
            if 0 <= indice < len(archivos):
                ruta = os.path.join(carpeta, archivos[indice])
                print(f"Archivo seleccionado: {ruta}")
                return ruta
            else:
                print(f"Por favor, ingresa un número entre 1 y {len(archivos)}.")
        except ValueError:
            print("Por favor, ingresa un número válido.")
