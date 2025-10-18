import pygame
from typing import List, Tuple, Set, Optional

# Colores RGB (mismos que en visualizador.py)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
VERDE = (34, 139, 34)     # muestras
AZUL = (30, 144, 255)     # nave
NARANJA = (255, 165, 0)   # astronauta
MARRON = (139, 69, 19)    # roca
ROJO = (178, 34, 34)      # volcán

TAM_CELDA = 50
MARGEN = 2


Grid = List[List[int]]
Pos = Tuple[int, int]


def ver_mapa(
    mapa: Grid,
    posicion_inicio: Optional[Pos] = None,
    posicion_nave: Optional[Pos] = None,
    muestras: Optional[Set[Pos]] = None,
    titulo: str = "Smart Astronaut - Visor de Mapas",
    tam_celda: int = TAM_CELDA,
):
    """
    Muestra un mapa estático (sin animación) usando pygame.

    Args:
        mapa: Matriz de enteros (normalmente 10x10) con los valores de las casillas.
        posicion_inicio: (fila, col) del astronauta (se pinta en naranja) si se desea.
        posicion_nave: (fila, col) de la nave (se pinta en azul) si se desea.
        muestras: Conjunto de posiciones (fila, col) de las muestras (se pintan en verde) si se desea.
        titulo: Título de la ventana.
        tam_celda: Tamaño del lado de cada celda en píxeles.

    Controles:
        - Cierra la ventana o presiona ESC/Q para salir.
    """
    if muestras is None:
        muestras = set()

    filas = len(mapa)
    cols = len(mapa[0]) if filas > 0 else 0

    pygame.init()
    ancho = tam_celda * cols + MARGEN * (cols + 1)
    alto = tam_celda * filas + MARGEN * (filas + 1)
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(titulo)

    def dibujar_celda(fila: int, col: int, color):
        x = col * (tam_celda + MARGEN) + MARGEN
        y = fila * (tam_celda + MARGEN) + MARGEN
        pygame.draw.rect(pantalla, color, (x, y, tam_celda, tam_celda))

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_q):
                    ejecutando = False

        pantalla.fill(NEGRO)

        # Pintar fondo según el valor de cada casilla
        for r in range(filas):
            for c in range(cols):
                val = mapa[r][c]
                color = BLANCO
                if val == 1:
                    color = GRIS
                elif val == 3:
                    color = MARRON
                elif val == 4:
                    color = ROJO
                elif val == 5:
                    color = AZUL
                elif val == 6:
                    color = VERDE
                dibujar_celda(r, c, color)

        # Overlays de elementos lógicos si se proporcionan
        if posicion_nave:
            dibujar_celda(posicion_nave[0], posicion_nave[1], AZUL)

        for s in muestras:
            dibujar_celda(s[0], s[1], VERDE)

        if posicion_inicio:
            dibujar_celda(posicion_inicio[0], posicion_inicio[1], NARANJA)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


def ver_mapa_desde_archivo(ruta: str, tam_celda: int = TAM_CELDA):
    """
    Carga un mundo desde un archivo .txt y lo muestra de forma estática.
    """
    from helpers.mundo import leer_mundo_desde_archivo  # import local para evitar dependencias duras

    datos = leer_mundo_desde_archivo(ruta)
    ver_mapa(
        datos["mapa"],
        posicion_inicio=datos.get("inicio"),
        posicion_nave=datos.get("nave"),
        muestras=datos.get("muestras", set()),
        tam_celda=tam_celda,
    )


if __name__ == "__main__":
    # Pequeño runner opcional para previsualizar rápidamente un archivo de la carpeta 'mundos'.
    try:
        from helpers.selector_archivos import elegir_archivo
        ruta = elegir_archivo("mundos")
        ver_mapa_desde_archivo(ruta)
    except Exception as e:
        print(f"No se pudo abrir el visor de mapas: {e}")
