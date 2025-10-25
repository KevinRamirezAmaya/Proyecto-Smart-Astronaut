import time
from collections import deque
from typing import Tuple, Set, List, Dict
from algoritmos.astar import empaquetar_estado, generar_estados_vecinos

Coordenada = Tuple[int, int]
Estado = Tuple[Coordenada, Tuple[Tuple[int, int], ...], bool, int]


def reconstruir_camino(diccionario_padres: Dict[Estado, Estado], estado_meta: Estado) -> List[Coordenada]:
    """
    Reconstruye el camino desde el estado inicial hasta el estado meta.
    """
    camino = []
    estado_actual = estado_meta

    while estado_actual in diccionario_padres:
        camino.append(estado_actual[0])
        estado_actual = diccionario_padres[estado_actual]

    camino.append(estado_actual[0])
    camino.reverse()
    return camino


def busqueda_amplitud(
    mapa: List[List[int]],
    posicion_inicial: Coordenada,
    posicion_nave: Coordenada,
    muestras_iniciales: Set[Coordenada]
):
    """
    Implementación de búsqueda no informada por amplitud (BFS).

    Retorna un diccionario con los siguientes campos:
      - exito: True si encontró todas las muestras
      - camino: lista de coordenadas desde el inicio hasta la meta
      - costo_total: costo acumulado real del camino (suma de costos de movimientos)
      - nodos_expandidos: cantidad de nodos extraídos/analizados
      - profundidad: número de movimientos en el camino
      - tiempo: duración de la ejecución en segundos
      - max_frontera: tamaño máximo alcanzado por la frontera (colade espera)
    """
    tiempo_inicio = time.perf_counter()

    estado_inicial = empaquetar_estado(posicion_inicial, muestras_iniciales, False, 0)

    frontera = deque([estado_inicial])
    en_frontera = {estado_inicial}
    diccionario_padres: Dict[Estado, Estado] = {}
    costos_acumulados: Dict[Estado, float] = {estado_inicial: 0.0}
    visitados = set()

    nodos_expandidos = 0
    max_frontera = 1

    while frontera:
        if len(frontera) > max_frontera:
            max_frontera = len(frontera)

        estado_actual = frontera.popleft()
        en_frontera.discard(estado_actual)

        if estado_actual in visitados:
            continue

        visitados.add(estado_actual)
        nodos_expandidos += 1

        posicion_actual, muestras_restantes_tupla, en_nave, combustible = estado_actual
        muestras_restantes = set(muestras_restantes_tupla)

        if not muestras_restantes:
            tiempo_total = time.perf_counter() - tiempo_inicio
            camino = reconstruir_camino(diccionario_padres, estado_actual)
            profundidad = len(camino) - 1

            return {
                "exito": True,
                "camino": camino,
                "costo_total": costos_acumulados.get(estado_actual, 0.0),
                "nodos_expandidos": nodos_expandidos,
                "profundidad": profundidad,
                "tiempo": tiempo_total,
                "max_frontera": max_frontera
            }

        for estado_vecino, costo_movimiento in generar_estados_vecinos(estado_actual, mapa, posicion_nave):
            nuevo_costo = costos_acumulados[estado_actual] + costo_movimiento

            # Si no lo hemos visto antes o encontramos un costo menor, actualizamos
            if estado_vecino not in costos_acumulados or nuevo_costo < costos_acumulados[estado_vecino]:
                costos_acumulados[estado_vecino] = nuevo_costo
                diccionario_padres[estado_vecino] = estado_actual

            # En BFS preferimos la primera aparición para garantizar menor profundidad.
            # Encolamos si no está visitado ni ya en la frontera.
            if estado_vecino not in visitados and estado_vecino not in en_frontera:
                frontera.append(estado_vecino)
                en_frontera.add(estado_vecino)

    tiempo_total = time.perf_counter() - tiempo_inicio
    return {"exito": False, "tiempo": tiempo_total, "nodos_expandidos": nodos_expandidos}
