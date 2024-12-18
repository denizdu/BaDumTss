from re import T
import pygame
from pygame import mixer
import os

pygame.init()

#variables para tamaño de la ventana
WIDTH = 1400
HEIGHT = 800

#variables para colores rgb
black = (0,0,0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

#propiedades ventana
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)

# frames por segundo y temporizador
fps = 60
timer = pygame.time.Clock()
beats = 8 # número inicial de pasos en pantalla?
instruments = 6 # número de instrumentos
boxes = [] # aquí irán los rectángulos para pulsar y activar sonidos
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] # inicializamos que no haya nada marcado al arrancar
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

#cargar sonidos
hi_hat = mixer.Sound(os.getcwd() + '/sounds/hihat.wav')
snare = mixer.Sound(os.getcwd() + '/sounds/snare.wav')
kick = mixer.Sound(os.getcwd() + '/sounds/kick.wav')
crash = mixer.Sound(os.getcwd() + '/sounds/crash.wav')
clap = mixer.Sound(os.getcwd() + '/sounds/clap.wav')
tom = mixer.Sound(os.getcwd() + '/sounds/tom.wav')
pygame.mixer.set_num_channels(instruments * 3) # ver documentación, no entiendo bien el problema (podría aparecer con muchos instrumentos a la vez y muchos bpm)

# funciones
def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()                
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()

def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 195], 5) # menú izquierdo
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 5]) # menú inferior
    boxes = []
    colors = [gray, white, gray]
    # textos de instrumentos
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30,30)) # dibuja el hi_hat_text en screen
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30,130))
    kick_text = label_font.render('Bass Drum', True, white)
    screen.blit(kick_text, (30,230))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30,330))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30,430))
    floor_tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (30,530))
    # pintamos líneas para separar los instrumentos
    for i in range (instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (195, (i * 100) + 100), 3)
    
    # creamos las zonas de cada beat e instrumento
    for i in range(beats):
        for j in range(instruments):
            if clicked[j][i] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color,
                [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, gold,
                [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black,
                [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i,j)))
        # marcamos de azul el punto activo
        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return boxes

# bucle principal
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    #botones menú inferior
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))

    #reproducir sonido
    if beat_changed:
        play_notes()
        beat_changed = False
    # este for controla todos los eventos que se producen durante el juego
    # (ratón, teclado, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # para la ejecución
            run = False
        # si hacemos click en un cuadro de un beat lo activa si no lo estaba
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos): # collidepoint comprueba si las coordenadas del click coinciden con alguna de las cajas
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True

    beat_length = 3600 // bpm # 60 fps * 60s

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    # envía todo a la pantalla
    pygame.display.flip()
#pygame.quit()