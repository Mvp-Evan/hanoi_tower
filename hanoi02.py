import pygame
import random

piles = [
    [5,4,3, 2, 1],
    [],
    []
]


COLORS = {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "BLUE": (122, 156, 198)
}

def moveDisk(source, destination):
    if len(piles[source]) and (len(piles[destination]) == 0 or piles[source][-1] < piles[destination][-1]):
        piles[destination].append(piles[source].pop())
        return True
    return False



def drawPile(pile, mode, selected, focused):
    pileSurface = pygame.Surface( (180, 400) )
    
    # Draw base
    pygame.draw.line(pileSurface, (222, 193, 255) if focused and mode == "place" else (255, 255, 255), (10, 360), (170, 360), 6)
    pygame.draw.line(pileSurface, (222, 193, 255) if focused and mode == "place" else (255, 255, 255), (90, 360), (90, 20), 6)

    # Draw discs
    for index, disc in enumerate(pile):
        y = 50 if selected and index == len(pile)-1 else 340 - index*20
        width = 30 + disc*10
        color = ()
        if focused and mode == "select" and index == len(pile)-1:
            color = (222, 193, 255)
        else:
            color = COLORS["BLUE"]
        pygame.draw.line(pileSurface, color, (90-width, y), (90+width, y), 12)
        
    return pileSurface
#init
pygame.init()
pygame.font.init()
# Configure pygame
pygame.key.set_repeat(0, 20)
window = pygame.display.set_mode( (640, 480) )
font = pygame.font.SysFont("comic sans ms",50)
# We create a surface to draw uppon
background = pygame.Surface(  window.get_size()  )
background.fill(COLORS["BLACK"])
window.blit(background, (0, 0)  )

clock = pygame.time.Clock()

stop = False
score = 50
selectedPile = -1
focusedPile = 0
mode = "select"

while not stop:
    
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        elif event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_ESCAPE:
                stop = True
            elif event.key == pygame.K_LEFT:
                focusedPile = (focusedPile - 1)%3
            elif event.key == pygame.K_RIGHT:
                focusedPile = (focusedPile + 1)%3
            elif event.key == pygame.K_RETURN:
                if selectedPile == focusedPile:
                    selectedPile = -1
                    mode = "select"
                elif mode == "place":
                    score -= 1
                    success = moveDisk(selectedPile, focusedPile)
                    if success:
                        mode = "select"
                        selectedPile = -1
                elif len(piles[focusedPile]):
                    selectedPile = focusedPile
                    mode = "place"
                if score == 0:
                    stop = True


    background.fill(COLORS["BLACK"])
    #display score
    s = str(score)
    textsurface = font.render("score:" + s,False,(255,255,255))
    
    # Check if we have won
    if len(piles[0]) == 0 and len(piles[1]) == 0:
        stop = True

    for index, pile in enumerate(piles):
        pileSurface = drawPile(pile, mode, selectedPile == index, focusedPile == index)
        background.blit(pileSurface, (20 + index*200, 20))
    background.blit(textsurface,(320,20))
    window.blit(background, (0, 0))
    pygame.display.flip()

pygame.quit()
