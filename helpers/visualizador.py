import pygame
import time
from typing import List, Tuple, Set

# Colores RGB
BLANCO = (255,255,255)
NEGRO = (0,0,0)
GRIS = (200,200,200)
VERDE = (34,139,34)    # muestras
AZUL = (30,144,255)    # nave
NARANJA = (255,165,0)  # astronauta
MARRON = (139,69,19)   # roca
ROJO = (178,34,34)     # volcán
AMARILLO = (255,255,0) # camino

TAM_CELDA = 50
MARGEN = 2

def dibujar_mundo(mapa: List[List[int]], camino: List[Tuple[int,int]],
                  posicion_inicio: Tuple[int,int], posicion_nave: Tuple[int,int],
                  muestras: Set[Tuple[int,int]]):
    """
    Dibuja el mapa y anima el camino encontrado.
    Presiona el botón para iniciar la animación del camino.
    Cierra la ventana para terminar.
    """
    pygame.init()
    ancho = TAM_CELDA*10 + MARGEN*(10+1)
    alto  = TAM_CELDA*10 + MARGEN*(10+1) + 80 
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Smart Astronaut - Trayectoria")
    
    fuente = pygame.font.Font(None, 36)
    boton_rect = pygame.Rect(ancho//2 - 100, alto - 70, 200, 50)
    boton_color = (0, 200, 0)
    boton_hover_color = (0, 255, 0)
    boton_texto = "Mostrar Camino"
    
    def dibujar_celda(fila, col, color):
        x = col*(TAM_CELDA+MARGEN)+MARGEN
        y = fila*(TAM_CELDA+MARGEN)+MARGEN
        pygame.draw.rect(pantalla, color, (x,y,TAM_CELDA,TAM_CELDA))
    
    def dibujar_boton(mouse_pos):
        color = boton_hover_color if boton_rect.collidepoint(mouse_pos) else boton_color
        pygame.draw.rect(pantalla, color, boton_rect, border_radius=10)
        pygame.draw.rect(pantalla, NEGRO, boton_rect, 3, border_radius=10)
        
        texto_surface = fuente.render(boton_texto, True, NEGRO)
        texto_rect = texto_surface.get_rect(center=boton_rect.center)
        pantalla.blit(texto_surface, texto_rect)

    reloj = pygame.time.Clock()
    ejecutando = True
    paso = 0
    mostrar_camino = False  
    
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    mostrar_camino = True  

        pantalla.fill(NEGRO)


        for r in range(10):
            for c in range(10):
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


        if mostrar_camino:
            for i, (r,c) in enumerate(camino[:paso+1]):
                x = c*(TAM_CELDA+MARGEN)+MARGEN
                y = r*(TAM_CELDA+MARGEN)+MARGEN
                pygame.draw.rect(pantalla, AMARILLO, (x,y,TAM_CELDA,TAM_CELDA))


        sr, sc = posicion_inicio
        dibujar_celda(sr, sc, NARANJA)
        if posicion_nave:
            dibujar_celda(posicion_nave[0], posicion_nave[1], AZUL)
        for s in muestras:
            dibujar_celda(s[0], s[1], VERDE)
        

        dibujar_boton(mouse_pos)

        pygame.display.flip()


        if mostrar_camino and paso < len(camino)-1:
            paso += 1
            time.sleep(0.08)
        
        reloj.tick(30)

    pygame.quit()
