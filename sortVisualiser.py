import pygame
import random
import math
pygame.init()


class drawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOUR = WHITE

    GREYS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Visualiser V1')
        self.set_list(list)


    def set_list(self, list):
        self.list = list
        #Min and Max are used to find the height of the bar.
        self.min_val = min(list)
        self.max_val = max(list)
        #calculate the length and width of each bar that represents an element
        self.block_width = round(self.width - self.SIDE_PAD / len(list))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD // 2



def draw(draw_info): #Fill the screen with the background colour set in the drawInformatio object
    draw_info.window.fill(drawInformation.BACKGROUND_COLOUR)
    draw_list(draw_info)
    pygame.display.update()



def draw_list(draw_info): #
    list = draw_info.list
    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        colour = draw_info.GREYS[i % 3]
        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_height,draw_info.block_width))

#generate a list of random elements that will be passed to the draw function.
def generate_starting_list(n, min_val, max_val):
    list = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        list.append(val)
    return list

def main():

    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    list = generate_starting_list(n,min_val,max_val)
    #instantiate the drawInformation class under the name draw_info.
    draw_info = drawInformation(900,700, list) 

    while run:
        clock.tick(60)
        draw(draw_info)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


if __name__ == "__main__":
    main()
