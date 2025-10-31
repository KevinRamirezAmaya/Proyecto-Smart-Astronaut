import time
from typing import Tuple, Set, List, Dict
from algoritmos.astar import empaquetar_estado, generar_estados_vecinos

Coordenada = Tuple[int, int]
# Estado ahora incluye el flag `nave_usada` (bool) como quinto elemento
Estado = Tuple[Coordenada, Tuple[Tuple[int, int], ...], bool, int, bool]


def reconstruir_camino(diccionario_padres: Dict[Estado, Estado], estado_meta: Estado) -> List[Coordenada]:
    camino = []
    estado_actual = estado_meta
    while estado_actual in diccionario_padres:
        camino.append(estado_actual[0])
        estado_actual = diccionario_padres[estado_actual]
    camino.append(estado_actual[0])
    camino.reverse()
    return camino


def busqueda_profundidad_sin_ciclos(
    mapa: List[List[int]],
    posicion_inicial: Coordenada,
    posicion_nave: Coordenada,
    muestras_iniciales: Set[Coordenada],
    profundidad_maxima: int = 10000
):
    """
    Búsqueda en profundidad que evita ciclos (no reingresa en nodos del camino actual).
    Devuelve la primera solución encontrada.
    """
    tiempo_inicio = time.perf_counter()

    estado_inicial = empaquetar_estado(posicion_inicial, muestras_iniciales, False, 0, False)

    pila = [(estado_inicial, {estado_inicial})]  # (estado, conjunto_de_estados_en_camino)
    diccionario_padres: Dict[Estado, Estado] = {}
    nodos_expandidos = 0

    while pila:
        estado_actual, camino_actual = pila.pop()
        nodos_expandidos += 1

        posicion_actual, muestras_restantes_tupla, en_nave, combustible, nave_usada = estado_actual
        muestras_restantes = set(muestras_restantes_tupla)

        if not muestras_restantes:
            tiempo_total = time.perf_counter() - tiempo_inicio
            camino = reconstruir_camino(diccionario_padres, estado_actual)
            return {
                "exito": True,
                "camino": camino,
                "costo_total": 0.0,  # No calculamos sumatoria real en esta versión
                "nodos_expandidos": nodos_expandidos,
                "profundidad": len(camino) - 1,
                "tiempo": tiempo_total,
            }

        # Evitar expandir si profundidad excede límite
        if len(camino_actual) > profundidad_maxima:
            continue

        for estado_vecino, costo_mov in generar_estados_vecinos(estado_actual, mapa, posicion_nave):
            if estado_vecino in camino_actual:
                continue  # evita ciclos en el camino actual

            # Guardar padre y empujar con nuevo conjunto de estados en camino
            diccionario_padres[estado_vecino] = estado_actual
            nuevo_camino_actual = set(camino_actual)
            nuevo_camino_actual.add(estado_vecino)
            pila.append((estado_vecino, nuevo_camino_actual))

    return {"exito": False, "nodos_expandidos": nodos_expandidos, "tiempo": time.perf_counter() - tiempo_inicio}
