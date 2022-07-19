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
    FONT = pygame.font.SysFont('Century Gothic', 30)
    BIG_FONT = pygame.font.SysFont('Century Gothic', 40, True)

    def __init__(self, width, height, list):
        self.width = width
        self.height = height
        #Window will represent the space in which the graphics will be drawn.
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Visualiser V1')
        self.set_list(list)


    def set_list(self, list):
        self.list = list
        #Min and Max are used to find the height of the bar.
        self.min_val = min(list)
        self.max_val = max(list)
        #calculate the length and width of each bar that represents an element
        self.block_width = round((self.width - self.SIDE_PAD) / len(list))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD // 2



def draw(draw_info): #Fill the screen with the background colour set in the drawInformatio object
    draw_info.window.fill(drawInformation.BACKGROUND_COLOUR)
    on_screen = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(on_screen, (draw_info.width/2 - on_screen.get_width()/2, 10))

    sort = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | L - Linear Sort", 1, draw_info.RED)
    draw_info.window.blit(sort, (draw_info.width/2 - sort.get_width()/2, 40))

    draw_list(draw_info)
    pygame.display.update()



def draw_list(draw_info, colour_pos={}, clear_bg = False): #
    list = draw_info.list

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width- draw_info.SIDE_PAD, draw_info.height)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOUR, clear_rect)

    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        colour = draw_info.GREYS[i % 3]

        if i in colour_pos:
            colour = colour_pos[i]

        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()
#generate a list of random elements that will be passed to the draw function.
def generate_starting_list(n, min_val, max_val):
    list = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        list.append(val)
    return list


def bubble_sort(draw_info, ascending = True):
    list = draw_info.list
    for i in range (len(list)-1):
        for j in range (len(list)-1-i):
            first = list[j]
            second = list[j +1]
            if (first > second and ascending) or (first < second and not ascending):
                list[j], list[j+1] = list[j+1], list[j]
                draw_list(draw_info, {j:draw_info.GREEN, j+1:draw_info.RED},True)
                yield True
    return list





def main():

    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    list = generate_starting_list(n,min_val,max_val)
    #instantiate the drawInformation class under the name draw_info.
    draw_info = drawInformation(800,600, list) 
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name= "Bubble Sort"
    sorting_generator = None


    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(list)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
    pygame.quit()


if __name__ == "__main__":
    main()

