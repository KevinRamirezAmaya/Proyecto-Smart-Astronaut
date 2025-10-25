import heapq
import time
from typing import Tuple, Set, List, Dict
from algoritmos.astar import empaquetar_estado, generar_estados_vecinos, reconstruir_camino

Coordenada = Tuple[int, int]
Estado = Tuple[Coordenada, Tuple[Tuple[int, int], ...], bool, int]


def busqueda_costo_uniforme(
    mapa: List[List[int]],
    posicion_inicial: Coordenada,
    posicion_nave: Coordenada,
    muestras_iniciales: Set[Coordenada]
):
    """
    Implementación del algoritmo de costo uniforme (UCS).
    Similar a A* pero sin heurística (h=0).
    """
    tiempo_inicio = time.perf_counter()

    estado_inicial = empaquetar_estado(posicion_inicial, muestras_iniciales, False, 0)
    costo_g: Dict[Estado, float] = {estado_inicial: 0.0}
    nodos_por_explorar = [(0.0, 0, estado_inicial)]
    diccionario_padres: Dict[Estado, Estado] = {}
    visitados = set()
    nodos_expandidos = 0
    contador = 0

    while nodos_por_explorar:
        costo_actual, _, estado_actual = heapq.heappop(nodos_por_explorar)

        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)
        nodos_expandidos += 1

        posicion_actual, muestras_restantes_tupla, en_nave, combustible = estado_actual
        muestras_restantes = set(muestras_restantes_tupla)

        if not muestras_restantes:
            tiempo_total = time.perf_counter() - tiempo_inicio
            camino, costos = reconstruir_camino(diccionario_padres, estado_actual, costo_g)
            costo_por_camino = list(zip(camino, costos))
            return {
                "exito": True,
                "camino con costo": costo_por_camino,
                "camino": camino,
                "costo_total": costo_g[estado_actual],
                "nodos_expandidos": nodos_expandidos,
                "profundidad": len(camino) - 1,
                "tiempo": tiempo_total,
            }

        for estado_vecino, costo_mov in generar_estados_vecinos(estado_actual, mapa, posicion_nave):
            nuevo_costo = costo_g[estado_actual] + costo_mov

            if estado_vecino not in costo_g or nuevo_costo < costo_g[estado_vecino]:
                costo_g[estado_vecino] = nuevo_costo
                diccionario_padres[estado_vecino] = estado_actual
                contador += 1
                heapq.heappush(nodos_por_explorar, (nuevo_costo, contador, estado_vecino))

    return {"exito": False, "nodos_expandidos": nodos_expandidos, "tiempo": time.perf_counter() - tiempo_inicio}
