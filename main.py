import pygame
import random

# Dimensiones de la ventana y del grid
WINDOW_SIZE = (450, 450)
GRID_SIZE = 25

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BEIGE = (220, 200, 187)
BG = (141, 123, 104)

# Clase para representar cada casilla del grid
class Casilla:
    def __init__(self, isBomb, x, y):
        self.isBomb = isBomb
        self.x = x
        self.y = y
        self.revealed = False
        self.isFlag = False

class Text:
    def __init__(self, surface, rect):
        self.surface = surface
        self.rect = rect

notMe = []
casillasReveladas = []

# clase para controlar el comportamiento del juego
class Behavior:
    # comportamiento cuando se hace click derecho
    def click(casilla, primer_click):
        global score, banderas, terminarJuego
        # el primer click nunca será una bomba
        if primer_click:
            casilla.isBomb = False       
        # si es bomba el juego termina, pieder puntaje para que sea imposible obtener victoria
        if casilla.isBomb: 
            terminarJuego = True
            casilla.revealed = True
            score -= 1
            for casilla in grid:
                casilla.revealed = True
            return
        # si la casilla no es bomba, la muestra
        if not casilla.isBomb and not casilla.revealed:
            casilla.revealed = True
            bombas_adyacentes = Behavior.contar_bombas_adyacentes(casilla)
            # si hay casillas sin bombas alrededor se expandirá lo que mas puedas hasta encontrar bombas
            if bombas_adyacentes == 0:
                Behavior.expandir_casillas_sin_bombas_adyacentes(casilla)
        if casilla.isFlag:
            banderas+=1
        Behavior.casillas_revelada(casilla)
    
    #expandir todo el terreno posible si no hay bombas adyacentes
    def expandir_casillas_sin_bombas_adyacentes(casilla):
        if casilla not in notMe:  
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        notMe.append(casilla)
                        continue
                    x = casilla.x + i
                    y = casilla.y + j
                    if 0 <= x < WINDOW_SIZE[0] // GRID_SIZE and 0 <= y < WINDOW_SIZE[1] // GRID_SIZE:
                        adyacente = grid[x * (WINDOW_SIZE[0] // GRID_SIZE) + y]
                        if not adyacente.isFlag:
                            adyacente.revealed = True
                            bombas_adyacentes = Behavior.contar_bombas_adyacentes(adyacente)
                            Behavior.mostrar_texto_numero_de_bombas_adyacentes(adyacente, bombas_adyacentes)
                            Behavior.casillas_revelada(adyacente)
                            if bombas_adyacentes == 0:
                                Behavior.expandir_casillas_sin_bombas_adyacentes(adyacente)
                    
    # Función para contar las bombas adyacentes
    def contar_bombas_adyacentes(casilla):
        bombas_adyacentes = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = casilla.x + i
                y = casilla.y + j
                if 0 <= x < WINDOW_SIZE[0] // GRID_SIZE and 0 <= y < WINDOW_SIZE[1] // GRID_SIZE:
                    adyacente = grid[x * (WINDOW_SIZE[0] // GRID_SIZE) + y]
                    if adyacente.isBomb:
                        bombas_adyacentes += 1

        # asignae el numero de bombas adyacente a la casilla seleccionada
        Behavior.mostrar_texto_numero_de_bombas_adyacentes(casilla, bombas_adyacentes)
        return bombas_adyacentes

    # cuando las todas las banderas estan sobre las casillas bombas y estan descubiertas el resto de casillas se gana
    def victoria():
        global victoria, terminarJuego
        if casillas_al_descubierto + score == len(grid):
            victoria = True
            terminarJuego = True

    # cuando una casilla se muestra, auumenta la variable de casillas al descubierto
    def casillas_revelada(casilla):
        global casillas_al_descubierto
        if casilla not in casillasReveladas:
            casillas_al_descubierto += 1
        casillasReveladas.append(casilla)

    # muestra el texto de numero de bombas adyacente en la casilla basado en una casilla y numero a poner
    def mostrar_texto_numero_de_bombas_adyacentes(casilla, bombas_adyacentes):
        if bombas_adyacentes != 0:
            COLORS = BLACK
            if bombas_adyacentes == 1: 
                COLORS = BLUE
            if bombas_adyacentes == 2:
                COLORS = GRAY
            if bombas_adyacentes == 3:
                COLORS = GREEN
            if bombas_adyacentes == 4:
                COLORS = ORANGE
            if bombas_adyacentes >= 5:
                COLORS = RED
            text_surface = font.render(str(bombas_adyacentes), True, COLORS)
            text_rect = text_surface.get_rect(center=(casilla.x * GRID_SIZE + GRID_SIZE // 2, casilla.y * GRID_SIZE + GRID_SIZE // 2))
            texts.append(Text(text_surface, text_rect))

    # si se gana o se pierde el juego termina
    def terminar_juego(victoria=False):
        # en caso de ganar
        if victoria:
            textVictoria = fontBigger.render("Victoria!",True,GREEN)
            textVictoriaRect = textVictoria.get_rect()
            textVictoriaRect.center = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2)
            window.blit(textVictoria, textVictoriaRect)
        # en caso de perder
        if not victoria:
            textDerrota = fontBigger.render("Derrota!",True,RED)
            textDerrotaRect = textDerrota.get_rect()
            textDerrotaRect.center = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2)
            window.blit(textDerrota, textDerrotaRect)


# Inicializar pygame
pygame.init()

# Crear la ventana
window = pygame.display.set_mode((WINDOW_SIZE[0],WINDOW_SIZE[1]))
pygame.display.set_caption("Buscaminas")
font = pygame.font.SysFont(None, 22)
fontBigger = pygame.font.SysFont(None, 100)

# Crear variables para controlar estados del juego
grid = []
texts = []
banderas = 0
score = 0
casillas_al_descubierto = 0
victoria = False
terminarJuego = False

# se crea aleatoriamente las bombas en cada casilla
for row in range(WINDOW_SIZE[0] // GRID_SIZE):
    for col in range(WINDOW_SIZE[1] // GRID_SIZE):
        #posibilidades de generar una bomba 1/7
        is_bomb = random.choice([True, False, False, False, False, False, False])  # Determinar si hay una bomba
        if is_bomb: banderas+=1
        casilla = Casilla(is_bomb, row, col)
        grid.append(casilla)

numBombasInMap = banderas
primerClick = True

# Bucle principal del juego
running = True
while running:
    window.fill(BG) # color fondo
    for event in pygame.event.get():
        # cerrar ventana
        if event.type == pygame.QUIT: 
            running = False
        # click del mouse
        elif event.type == pygame.MOUSEBUTTONUP and not terminarJuego:  # Evento de clic del mouse
            pos = pygame.mouse.get_pos()
            # se obtiene la casilla clickeada haciendo conversiones
            clicked_row = (pos[0] // GRID_SIZE)
            clicked_col = (pos[1] // GRID_SIZE)
            casilla = grid[clicked_row * (WINDOW_SIZE[0] // GRID_SIZE) + clicked_col]
            # click izquierdo
            if event.button == 1:
                Behavior.click(casilla, primerClick)
                primerClick = False
            # click derecho para poner banderas
            if event.button == 3:
                if not casilla.revealed:
                    if not casilla.isFlag:
                        banderas -= 1
                        casilla.isFlag = True
                        if casilla.isBomb:
                            score += 1
                        break
                if casilla.isFlag:
                    banderas += 1
                    casilla.isFlag = False
            # cada que se hace click se verifica si ya ganó el usuario
            Behavior.victoria()

    # Dibujar el grid (casillas)
    for casilla in grid:
        pygame.draw.rect(window, BEIGE, (casilla.x * GRID_SIZE, casilla.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        if casilla.revealed:
            pygame.draw.rect(window, WHITE, (casilla.x * GRID_SIZE+1, casilla.y * GRID_SIZE+1, GRID_SIZE-1, GRID_SIZE-1))
            if casilla.isBomb:
                pygame.draw.circle(window, BLACK, (casilla.x * GRID_SIZE + GRID_SIZE // 2, casilla.y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 4)
        else:
            if casilla.isFlag:
                pygame.draw.rect(window, RED, (casilla.x * GRID_SIZE+1, casilla.y * GRID_SIZE+1, GRID_SIZE-1, GRID_SIZE-1))
            else:
                pygame.draw.rect(window, BG, (casilla.x * GRID_SIZE+1, casilla.y * GRID_SIZE+1, GRID_SIZE-1, GRID_SIZE-1))
    pygame.draw.line(window, WHITE, (WINDOW_SIZE[0],0),(WINDOW_SIZE[0],WINDOW_SIZE[1]))

    # muestra los textos de los numeros de cada casilla
    for txt in texts:
        window.blit(txt.surface, txt.rect)

    # si gana o pierde esta parte se ejecuta
    if terminarJuego:
        if victoria:
            Behavior.terminar_juego(victoria)
        if not victoria:
            Behavior.terminar_juego()

    pygame.display.update()

# Salir del juego
pygame.quit()
