
from re import L
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
        # < Window will represent the space in which the graphics will be drawn />
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Visualiser V1')
        self.set_list(list)


    def set_list(self, list):
        self.list = list
        # < Min and Max are used to calculate the  />
        self.min_val = min(list)
        self.max_val = max(list)
        # < calculate the length and width of each bar that represents an element />
        self.block_width = round((self.width - self.SIDE_PAD) / len(list))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD // 2


# <-- Draw the controls and buttons as the title bar />
def draw(draw_info, sorting_algo_name, ascending):
    
    if ascending:
        asc = 'Ascending'
    else:
        asc = 'Descending'
     # < Fill the screen with the background colour set in the drawInformation object />
    draw_info.window.fill(drawInformation.BACKGROUND_COLOUR)

    title = draw_info.BIG_FONT.render(f"{sorting_algo_name} - {asc}",1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 10))

    on_screen = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(on_screen, (draw_info.width/2 - on_screen.get_width()/2, 40))

    sort = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort", 1, draw_info.RED)
    draw_info.window.blit(sort, (draw_info.width/2 - sort.get_width()/2, 70))

    draw_list(draw_info)
    pygame.display.update()


# < Responsible for calculating the size and widh of the bars on screen and rendering them />
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


def insertion_sort(draw_info, ascending=True):
    list = draw_info.list

    for i in range(1, len(list)):
        current = list[i]
            
        while True:
            ascending_sort = i > 0 and list[i-1] > current and ascending
            descending_sort = i > 0 and list[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            list[i] = list[i-1]
            i = i-1
            list[i] = current
            draw_list(draw_info, {i:draw_info.GREEN, i - 1 :draw_info.RED}, True)
            yield True
    return list

""" def merge_sort(draw_info, ascending = True):
    list = draw_info.list
    middle = len(list) // 2
    left_side = list[:middle+1]
    right_side = list[middle+1:]
    merge_sort(left_side)
    merge_sort(right_side)
    return merge(left_side, right_side)

def merge( left, right):
    output = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:])
    output.extend(right[j:])
    return output """

def main():
# < To be called at the start of the program, responsible for the flow of the program /> 
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 0
    max_val = 100

    list = generate_starting_list(n,min_val,max_val)
    # < instantiate the drawInformation class under the name draw_info />
    draw_info = drawInformation(800,600, list) 
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name= "Bubble Sort"
    sorting_generator = None


    while run:
        clock.tick(120) #< controls the speed of the animation, higher number = faster solving />

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            #< conditionals check for key presses and call functions accordingly />
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
            #< --- SORTING ALGORITHM KEYDOWNS --- />
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            """ elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort" """
    pygame.quit()

if __name__ == "__main__":
    main()
