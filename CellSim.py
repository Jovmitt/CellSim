
import pygame
import random
import time
import keyboard

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 825, 825
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CellSim')

#temporary stuff:
cell_radius = 10
cell_width = 1

divide_timer = 0

num_cells = 5
new_cell = num_cells
cells = []
cells_pos_x = []
cells_pos_y = []

virus_enabled = True
num_viruses = 0
infection_rate = 4
viruses_timer_value = 2500
viruses = []
viruses_timer = []
viruses_pos_x = []
viruses_pos_y = []

#cells stuff
def cells_start():
    for i in range(num_cells):
        cells.append(i)
        cells_pos_x.append(random.randint(0, SCREEN_WIDTH))
        cells_pos_y.append(random.randint(0, SCREEN_HEIGHT))

def cells_update():
    global num_cells
    if cells[i] != -1:
        cells_pos_x[i] += random.randint(-1, 1)
        cells_pos_y[i] += random.randint(-1, 1)
        if cells_pos_x[i] >= SCREEN_WIDTH: cells_pos_x[i] = SCREEN_WIDTH
        if cells_pos_x[i] <= 0: cells_pos_x[i] = 0
        if cells_pos_y[i] >= SCREEN_HEIGHT: cells_pos_y[i] = SCREEN_WIDTH
        if cells_pos_y[i] <= 0: cells_pos_y[i] = 0


def cells_draw():
    if cells[i] != -1:
        pygame.draw.circle(screen, (0, 0, 0), (cells_pos_y[i], cells_pos_x[i]), cell_radius + cell_width * 2)
        pygame.draw.circle(screen, (0, 0, 255), (cells_pos_y[i], cells_pos_x[i]), cell_radius)
        pygame.draw.circle(screen, (0, 255, 0), (cells_pos_y[i], cells_pos_x[i]), cell_radius / 10)
        pygame.draw.circle(screen, (255, 0, 0), (cells_pos_y[i], cells_pos_x[i]), cell_radius, cell_width)

        #pygame.draw.rect(screen, (255, 255, 255), (cells_pos_y[i] - cell_radius, cells_pos_x[i] - cell_radius, cell_radius, cell_radius))


def cells_divide():
    global divide_timer
    global num_cells
    if divide_timer < 250: divide_timer += 1
    else:
        for i in range(len(cells)):
            if cells[i] != -1:
                cells.append(1)
                cells_pos_x.append(cells_pos_x[i] + random.randint(-10, 10))
                cells_pos_y.append(cells_pos_y[i] + random.randint(-10, 10))
                num_cells += 1
        divide_timer = 0



#virus stuff
def virus_start():
    if virus_enabled == True:
        for i in range(num_viruses):
            viruses.append(i)
            viruses_timer.append(i)
            viruses_pos_x.append(random.randint(0, SCREEN_WIDTH))
            viruses_pos_y.append(random.randint(0, SCREEN_HEIGHT))
            viruses_timer[i] = viruses_timer_value

def virus_draw():
    if virus_enabled == True:
        if viruses[i] != -1:
            pygame.draw.circle(screen, (0, 0, 0), (viruses_pos_y[i], viruses_pos_x[i]), 10)
            pygame.draw.circle(screen, (255, 0, 0), (viruses_pos_y[i], viruses_pos_x[i]), 1)

def virus_update():
    if virus_enabled == True:
        global viruses_timer
        global num_viruses
        global num_cells
        if viruses[i] != -1:
            viruses_timer[i] -= 1
            viruses_pos_x[i] += random.randint(-5, 5)
            viruses_pos_y[i] += random.randint(-5, 5)
            if viruses_pos_x[i] >= SCREEN_WIDTH: viruses_pos_x[i] = SCREEN_WIDTH
            if viruses_pos_x[i] <= 0: viruses_pos_x[i] = 0
            if viruses_pos_y[i] >= SCREEN_HEIGHT: viruses_pos_y[i] = SCREEN_HEIGHT
            if viruses_pos_y[i] <= 0: viruses_pos_y[i] = 0
            if viruses_timer[i] <= 0: viruses[i] = -1

def virus_infect():
    global num_viruses
    global num_cells
    for j in range(len(cells)):
        if cells[j] != -1:
            dx = viruses_pos_x[i] - cells_pos_x[j]
            dy = viruses_pos_y[i] - cells_pos_y[j]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance <= cell_radius:
                viruses[i] = -1
                pygame.draw.circle(screen, (0, 0, 0), (viruses_pos_y[i], viruses_pos_x[i]), 10)
                for k in range(random.randint(1, infection_rate)):
                    viruses.append(1)
                    viruses_timer.append(viruses_timer_value)
                    viruses_pos_x.append(cells_pos_x[j])
                    viruses_pos_y.append(cells_pos_y[j])
                    num_viruses += 1
                print("Infection occurred - Num cells:", num_cells - 1, "Num viruses:", num_viruses)
                cells[j] = -1
                num_cells -= 1

kill_timer = 0
already_pressed = 0
def kill_cells(kill_percentage):
    global kill_timer
    global already_pressed
    global num_cells
    if kill_timer < 50:
        kill_timer += 1
    else: already_pressed = 0
    while keyboard.is_pressed('k'):
        if already_pressed == 0:
            already_pressed = 1
            kill_timer = 0
            for i in range(len(cells)):
                if cells[i] != -1:
                    if random.randint(0, 100) <= kill_percentage:
                        pygame.draw.circle(screen, (0, 0, 0), (cells_pos_y[i], cells_pos_x[i]), cell_radius + cell_width * 2)
                        cells[i] = -1
                        num_cells -= 1



paused = False
def pause():
    global paused
    while keyboard.is_pressed('p'): paused = True
    while paused:
        if keyboard.is_pressed('p'): paused = False
        while keyboard.is_pressed('p'): paused = False

def summon_virus():
    global paused
    global num_viruses
    global i
    if not paused:
        while keyboard.is_pressed('v'): paused = True
    if paused:
        num_viruses += 1
        i = len(viruses) + 1
        viruses.append(i)
        viruses_timer.append(i)
        viruses_pos_x.append(random.randint(0, SCREEN_WIDTH))
        viruses_pos_y.append(random.randint(0, SCREEN_HEIGHT))
        viruses_timer[i-1] = viruses_timer_value
        paused = False


clock = pygame.time.Clock()
FPS = 60
running = True
cells_start()
virus_start()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)

    for i in range(len(cells)):
        cells_draw()
        cells_update()

    cells_divide()

    for i in range(len(viruses)):
        virus_draw()
        virus_update()
        virus_infect()

    kill_cells(50)

    summon_virus()

    pause()

    print(num_cells)

    pygame.display.flip()

    time.sleep(.01)

pygame.quit()
