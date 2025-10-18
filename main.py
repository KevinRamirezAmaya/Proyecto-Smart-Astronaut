from helpers.mundo import leer_mundo_desde_archivo
from helpers.selector_archivos import elegir_archivo
import algoritmos.astar as busqueda_a_estrella
import algoritmos.avara as busqueda_avara
from helpers import visualizador

def main():
    print("=== Smart Astronaut - Selección de búsqueda ===")
    print("1) Búsqueda NO informada")
    print("2) Búsqueda INFORMADA")
    opcion = input("Elige 1 o 2: ").strip()
    
    if opcion == "1":
        print("\n=== BÚSQUEDA NO INFORMADA ===")
        print("A John le falta camellar(John camella).")
        return
    
    elif opcion == "2":
        print("\n=== BÚSQUEDA INFORMADA ===")
        print("Algoritmos informados disponibles:")
        print("1) Avara")
        print("2) A*")
        sel = input("Elige 1 o 2: ").strip()
        
        if sel not in ("1", "2"):
            print("Opción inválida.")
            return
        
        # Seleccionar archivo de mundo
        ruta = elegir_archivo()
        mundo = leer_mundo_desde_archivo(ruta)
        mapa = mundo["mapa"]
        inicio = mundo["inicio"]
        nave = mundo["nave"]
        muestras = mundo["muestras"]

        print("Inicio:", inicio, "Nave:", nave, "Muestras:", muestras)

        # Ejecutar el algoritmo seleccionado
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
        print("Trayectoria:", resultado["camino con costo"])
        print("\nSe mostrará la animación en pygame (cierra la ventana para terminar).")
        visualizador.dibujar_mundo(mapa, resultado["camino"], inicio, nave, muestras)
    else:
        print("Opción inválida.")
        return

if __name__ == "__main__":
    main()