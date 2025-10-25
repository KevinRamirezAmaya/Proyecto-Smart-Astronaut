from helpers.mundo import leer_mundo_desde_archivo
from helpers.selector_archivos import elegir_archivo
import algoritmos.astar as busqueda_a_estrella
import algoritmos.avara as busqueda_avara
from algoritmos import busqueda_amplitud, busqueda_costo_uniforme, busqueda_profundidad_sin_ciclos
from helpers import visualizador

def main():
    print("=== Smart Astronaut - Selección de búsqueda ===")
    print("1) Búsqueda NO informada")
    print("2) Búsqueda INFORMADA")
    opcion = input("Elige 1 o 2: ").strip()
    
    if opcion == "1":
        print("\n=== BÚSQUEDA NO INFORMADA ===")
        print("Algoritmos no informados disponibles:")
        print("1) Amplitud (BFS)")
        print("2) Costo uniforme (UCS)")
        print("3) Profundidad evitando ciclos")
        sel = input("Elige 1, 2 o 3: ").strip()

        if sel not in ("1", "2", "3"):
            print("Opción inválida.")
            return

        ruta = elegir_archivo()
        mundo = leer_mundo_desde_archivo(ruta)
        mapa = mundo["mapa"]
        inicio = mundo["inicio"]
        nave = mundo["nave"]
        muestras = mundo["muestras"]

        print("Inicio:", inicio, "Nave:", nave, "Muestras:", muestras)

        if sel == "1":
            print("Ejecutando búsqueda por AMPLITUD (BFS)")
            resultado = busqueda_amplitud(mapa, inicio, nave, muestras)
        elif sel == "2":
            print("Ejecutando búsqueda por COSTO UNIFORME (UCS)")
            resultado = busqueda_costo_uniforme(mapa, inicio, nave, muestras)
        else:
            print("Ejecutando búsqueda por PROFUNDIDAD evitando ciclos")
            resultado = busqueda_profundidad_sin_ciclos(mapa, inicio, nave, muestras)

        if not resultado.get("exito", False):
            print("No se encontró solución.")
            return

        print("\n=== RESULTADOS ===")
        # Algunos algoritmos retornan "camino con costo" y otros solo "camino"
        costo_total = resultado.get("costo_total", resultado.get("costo", resultado.get("costo_total", 0)))
        print("Costo total (g):", costo_total)
        print("Nodos expandidos:", resultado.get("nodos_expandidos"))
        print("Profundidad (movimientos):", resultado.get("profundidad"))
        print("Tiempo (s):", resultado.get("tiempo"))
        if "camino con costo" in resultado:
            print("Trayectoria:", resultado["camino con costo"])
            camino_a_visualizar = resultado["camino"]
        else:
            print("Trayectoria:", resultado.get("camino"))
            camino_a_visualizar = resultado.get("camino")

        print("\nSe mostrará la animación en pygame (cierra la ventana para terminar).")
        visualizador.dibujar_mundo(mapa, camino_a_visualizar, inicio, nave, muestras)
    
    elif opcion == "2":
        print("\n=== BÚSQUEDA INFORMADA ===")
        print("Algoritmos informados disponibles:")
        print("1) Avara")
        print("2) A*")
        sel = input("Elige 1 o 2: ").strip()
        
        if sel not in ("1", "2"):
            print("Opción inválida.")
            return
        
        ruta = elegir_archivo()
        mundo = leer_mundo_desde_archivo(ruta)
        mapa = mundo["mapa"]
        inicio = mundo["inicio"]
        nave = mundo["nave"]
        muestras = mundo["muestras"]

        print("Inicio:", inicio, "Nave:", nave, "Muestras:", muestras)

        if sel == "1":
            print("Ejecutando búsqueda AVARA")
            resultado = busqueda_avara.busqueda_avara(mapa, inicio, nave, muestras)
        else:
            print("Ejecutando búsqueda A*")
            resultado = busqueda_a_estrella.busqueda_a_estrella(mapa, inicio, nave, muestras)


        if not resultado.get("exito", False):
            print("No se encontró solución.")
            return

        print("\n=== RESULTADOS ===")
        print("Costo total (g):", resultado["costo_total"])
        print("Nodos expandidos:", resultado["nodos_expandidos"])
        print("Profundidad (movimientos):", resultado["profundidad"])
        print("Tiempo (s):", resultado["tiempo"])
        print("\nSe mostrará la animación en pygame (cierra la ventana para terminar).")
        visualizador.dibujar_mundo(mapa, resultado["camino"], inicio, nave, muestras)
    else:
        print("Opción inválida.")
        return

if __name__ == "__main__":
    main()