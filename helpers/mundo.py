from typing import List, Tuple, Set
import os


Pos = Tuple[int, int]
Grid = List[List[int]]


CASILLA_LIBRE = 0
CASILLA_OBSTACULO = 1
CASILLA_ROCA = 3      
CASILLA_VOLCAN = 4    
CASILLA_NAVE = 5
CASILLA_MUESTRA = 6
ASTRONAUTA = 2

def leer_mundo_desde_archivo(ruta: str) -> dict:
    """
    Lee un archivo de texto con 10 líneas y devuelve un diccionario:
      - 'mapa': Grid 10x10 (lista de listas de int)
      - 'inicio': Pos (fila,col) del astronauta
      - 'nave': Pos (fila,col) de la nave o None
      - 'muestras': set de Pos con las muestras
    """
    assert os.path.exists(ruta), f"No existe el archivo: {ruta}"
    with open(ruta, "r") as f:
        lineas = [ln.strip() for ln in f if ln.strip()]
    mapa: Grid = []
    inicio = None
    nave = None
    muestras: Set[Pos] = set()
    for fila_idx, linea in enumerate(lineas):
        partes = linea.split()
        fila = [int(x) for x in partes]
        mapa.append(fila)
        for col_idx, valor in enumerate(fila):
            if valor == ASTRONAUTA:
                inicio = (fila_idx, col_idx)
            elif valor == CASILLA_NAVE:
                nave = (fila_idx, col_idx)
            elif valor == CASILLA_MUESTRA:
                muestras.add((fila_idx, col_idx))
    return {"mapa": mapa, "inicio": inicio, "nave": nave, "muestras": muestras}

def dentro_de_limites(pos: Pos) -> bool:
    """Devuelve True si la posición está dentro del mapa 10x10."""
    fila, col = pos
    return 0 <= fila < 10 and 0 <= col < 10

def es_obstaculo(mapa: Grid, pos: Pos) -> bool:
    """True si la celda es obstáculo (valor 1)."""
    fila, col = pos
    return mapa[fila][col] == CASILLA_OBSTACULO

def costo_de_entrada_terreno(mapa: Grid, pos: Pos) -> float:
    """
    Costo para ENTRAR a esta celda si se está a pie (no usando combustible de la nave).
    Según especificación: roca = 3, volcán = 5, libre/nave/muestra = 1.
    """
    fila, col = pos
    valor = mapa[fila][col]
    if valor == CASILLA_ROCA:
        return 3.0
    if valor == CASILLA_VOLCAN:
        return 5.0
    return 1.0
