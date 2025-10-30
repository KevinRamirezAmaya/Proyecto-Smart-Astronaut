import heapq
import time
from typing import Tuple, Set, List, Dict
from algoritmos.astar import (
    heuristica,
    empaquetar_estado,
    generar_estados_vecinos as generar_vecinos,
)

Coordenada = Tuple[int, int]
Estado = Tuple[Coordenada, Tuple[Tuple[int, int], ...], bool, int, bool]
# Un estado contiene:
#   - posicion_actual: (fila, columna)
#   - muestras_restantes: conjunto ordenado de posiciones
#   - en_nave: True/False
#   - combustible: movimientos restantes de la nave
#   - nave_usada: True si ya se recogió/usó la nave


def reconstruir_camino(diccionario_padres: Dict[Estado, Estado], estado_meta: Estado) -> List[Coordenada]:
    """
    Reconstruye el camino completo desde el estado inicial hasta el estado meta
    usando el diccionario de padres (rastro inverso).
    """
    camino = []
    estado_actual = estado_meta


    while estado_actual in diccionario_padres:
        camino.append(estado_actual[0])
        estado_actual = diccionario_padres[estado_actual]

    camino.append(estado_actual[0])
    camino.reverse()
    return camino


def busqueda_avara(
    mapa: List[List[int]],
    posicion_inicial: Coordenada,
    posicion_nave: Coordenada,
    muestras_iniciales: Set[Coordenada]
):
    """
    Implementa el algoritmo de búsqueda Avara.
    Utiliza la heurística proporcionada.

    Retorna un diccionario con la información del resultado:
    - exito: True si encontró todas las muestras
    - camino: lista de coordenadas desde el inicio hasta la meta
    - costo_total: costo acumulado del camino (solo informativo aquí)
    - nodos_expandidos: cantidad de nodos que se analizaron
    - profundidad: longitud del camino
    - tiempo: duración de la ejecución
    - max_frontera: tamaño máximo alcanzado por la frontera
    """

    tiempo_inicio = time.perf_counter()


    estado_inicial = empaquetar_estado(posicion_inicial, muestras_iniciales, False, 0, False)

    
    nodos_por_explorar: List[Tuple[float, int, Estado]] = []
    contador_expansiones = 0

    heuristica_inicial = heuristica(posicion_inicial, posicion_nave, muestras_iniciales)
    heapq.heappush(nodos_por_explorar, (heuristica_inicial, contador_expansiones, estado_inicial))

    diccionario_padres: Dict[Estado, Estado] = {}
    conjunto_visitados = set()
    nodos_expandidos = 0
    costos_acumulados: Dict[Estado, float] = {estado_inicial: 0.0}
  

    while nodos_por_explorar:     

        heuristica_actual, _, estado_actual = heapq.heappop(nodos_por_explorar)

        if estado_actual in conjunto_visitados:
            continue

        conjunto_visitados.add(estado_actual)
        nodos_expandidos += 1

        posicion_actual, muestras_restantes_tupla, en_nave, combustible, nave_usada = estado_actual
        muestras_restantes = set(muestras_restantes_tupla)

        if not muestras_restantes:
            tiempo_total = time.perf_counter() - tiempo_inicio
            camino = reconstruir_camino(diccionario_padres, estado_actual)
            profundidad = len(camino) - 1

            return {
                "exito": True,
                "camino": camino,
                "costo_total": costos_acumulados[estado_actual],
                "nodos_expandidos": nodos_expandidos,
                "profundidad": profundidad,
                "tiempo": tiempo_total
            }

        for estado_vecino, costo_movimiento in generar_vecinos(estado_actual, mapa, posicion_nave):
            costo_acumulado_nuevo = costos_acumulados[estado_actual] + costo_movimiento

            # Actualizar si encontramos un camino más barato hacia ese estado
            if estado_vecino not in costos_acumulados or costo_acumulado_nuevo < costos_acumulados[estado_vecino]:
                costos_acumulados[estado_vecino] = costo_acumulado_nuevo
                diccionario_padres[estado_vecino] = estado_actual

            # Calcular heurística del vecino (solo se usa h)
            posicion_vecina, muestras_vecinas, _, _, _ = estado_vecino
            heuristica_vecina = heuristica(posicion_vecina, posicion_nave, set(muestras_vecinas))

            contador_expansiones += 1
            heapq.heappush(nodos_por_explorar, (heuristica_vecina, contador_expansiones, estado_vecino))

    tiempo_total = time.perf_counter() - tiempo_inicio
    return {
        "exito": False,
        "tiempo": tiempo_total,
        "nodos_expandidos": nodos_expandidos
    }