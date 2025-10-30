import heapq
import time
from typing import Tuple, Set, List, Dict
from helpers.mundo import costo_de_entrada_terreno, dentro_de_limites, es_obstaculo


Coordenada = Tuple[int, int]
Estado = Tuple[Coordenada, Tuple[Tuple[int, int], ...], bool, int, bool]
# Un estado contiene:
#   - posicion_actual: (fila, columna)
#   - muestras_restantes: conjunto ordenado de posiciones
#   - en_nave: True/False
#   - combustible: movimientos restantes de la nave
#   - nave_usada: True si ya se recogió/usó la nave

def heuristica(posicion_actual: Coordenada, posicion_nave: Coordenada, muestras_restantes: Set[Coordenada]) -> float:
    """
    Calcula la heurística h(n) según:
    h = min(
        distancia_manhattan(posicion_actual, muestra),
        distancia_manhattan(posicion_actual, nave) + 0.5 * distancia_manhattan(nave, muestra)
    )
    """
    if not muestras_restantes:
        return 0.0

    valores_heuristicos = []
    for muestra in muestras_restantes:
        distancia_directa = abs(posicion_actual[0] - muestra[0]) + abs(posicion_actual[1] - muestra[1])
        if posicion_nave:
            distancia_a_nave = abs(posicion_actual[0] - posicion_nave[0]) + abs(posicion_actual[1] - posicion_nave[1])
            distancia_nave_a_muestra = abs(posicion_nave[0] - muestra[0]) + abs(posicion_nave[1] - muestra[1])
            costo_usando_nave = distancia_a_nave + 0.5 * distancia_nave_a_muestra
            valores_heuristicos.append(min(distancia_directa, costo_usando_nave))
        else:
            valores_heuristicos.append(distancia_directa)

    return min(valores_heuristicos)


def empaquetar_estado(posicion: Coordenada, muestras: Set[Coordenada], en_nave: bool, combustible: int, nave_usada: bool) -> Estado:
    """Convierte los datos del estado en una tupla inmutable"""
    return (posicion, tuple(sorted(muestras)), en_nave, combustible, nave_usada)


def desempaquetar_estado(estado: Estado):
    posicion, muestras_tupla, en_nave, combustible, nave_usada = estado
    return posicion, set(muestras_tupla), en_nave, combustible, nave_usada


def generar_estados_vecinos(estado_actual: Estado, mapa: List[List[int]], posicion_nave: Coordenada):
    """
    Genera los estados vecinos posibles (arriba, abajo, izquierda, derecha).
    Aplica las reglas de movimiento:
      - Si está en la nave y tiene combustible: costo 0.5 por movimiento, -1 combustible
      - Si no está en la nave: costo según el tipo de terreno (1, 3, 5)
      - Al llegar a la nave por primera vez: recarga combustible a 20, en_nave=True, y la nave desaparece
      - Al llegar a una muestra: la elimina de las muestras restantes
    """
    posicion_actual, muestras_restantes, en_nave, combustible, nave_usada = desempaquetar_estado(estado_actual)
    fila, col = posicion_actual

    movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    vecinos = []

    for desplazamiento_fila, desplazamiento_columna in movimientos:
        nueva_fila, nueva_col = fila + desplazamiento_fila, col + desplazamiento_columna
        nueva_posicion = (nueva_fila, nueva_col)

        if not dentro_de_limites(nueva_posicion) or es_obstaculo(mapa, nueva_posicion):
            continue

        nueva_nave_usada = nave_usada
        
        # Determinar costo y estado de combustible
        if en_nave and combustible > 0:
            # Movimiento usando la nave
            costo_movimiento = 0.5
            nuevo_combustible = combustible - 1
            nuevo_en_nave = True
        else:
            # Movimiento a pie
            costo_movimiento = costo_de_entrada_terreno(mapa, nueva_posicion)
            nuevo_combustible = 0
            nuevo_en_nave = False

        # Si llegamos a la nave por primera vez, recargar y marcar como usada
        if mapa[nueva_fila][nueva_col] == 5 and not nave_usada:
            nuevo_en_nave = True
            nuevo_combustible = 20
            nueva_nave_usada = True

        # Si llegamos a una muestra, recogerla
        nuevas_muestras = set(muestras_restantes)
        if mapa[nueva_fila][nueva_col] == 6 and (nueva_fila, nueva_col) in nuevas_muestras:
            nuevas_muestras.remove((nueva_fila, nueva_col))

        nuevo_estado = empaquetar_estado(nueva_posicion, nuevas_muestras, nuevo_en_nave, nuevo_combustible, nueva_nave_usada)
        vecinos.append((nuevo_estado, costo_movimiento))

    return vecinos


def reconstruir_camino(diccionario_padres: Dict[Estado, Estado], estado_final: Estado, costo_g: Dict[Estado, float]):
    """Reconstruye la trayectoria completa desde el inicio hasta la meta con sus costos"""
    camino = []
    costos = []
    estado = estado_final
    
    while estado in diccionario_padres:
        camino.append(estado[0])
        costos.append(costo_g[estado])
        estado = diccionario_padres[estado]
    
    camino.append(estado[0])
    costos.append(costo_g[estado])
    
    camino.reverse()
    costos.reverse()
    
    return camino, costos


def busqueda_a_estrella(mapa: List[List[int]], posicion_inicio: Coordenada, posicion_nave: Coordenada, muestras_objetivo: Set[Coordenada]):
    """
    Implementa el algoritmo A*.
    """
    tiempo_inicio = time.perf_counter()

    estado_inicial = empaquetar_estado(posicion_inicio, muestras_objetivo, False, 0, False)
    costo_g = {estado_inicial: 0.0}
    heuristica_inicial = heuristica(posicion_inicio, posicion_nave, muestras_objetivo)
    nodos_por_explorar = [(heuristica_inicial, heuristica_inicial, 0, estado_inicial)]

    diccionario_padres = {}
    visitados = set()
    nodos_expandidos = 0

    while nodos_por_explorar:
        f_actual, h_actual, _, estado_actual = heapq.heappop(nodos_por_explorar)

        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)
        nodos_expandidos += 1

        posicion_actual, muestras_restantes, en_nave, combustible, nave_usada = desempaquetar_estado(estado_actual)

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
                "tiempo": tiempo_total
            }

        for estado_vecino, costo_mov in generar_estados_vecinos(estado_actual, mapa, posicion_nave):
            nuevo_costo_g = costo_g[estado_actual] + costo_mov

            if estado_vecino not in costo_g or nuevo_costo_g < costo_g[estado_vecino]:
                costo_g[estado_vecino] = nuevo_costo_g
                diccionario_padres[estado_vecino] = estado_actual

                posicion_vecina, muestras_vecinas, en_nave_vecina, combustible_vecino, nave_usada_vecina = desempaquetar_estado(estado_vecino)
                heuristica_vecina = heuristica(posicion_vecina, posicion_nave, muestras_vecinas)
                

                heapq.heappush(nodos_por_explorar, (nuevo_costo_g + heuristica_vecina, heuristica_vecina, nodos_expandidos, estado_vecino))

    return {"exito": False}
