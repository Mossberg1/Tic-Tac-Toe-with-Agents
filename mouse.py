import pygame

def get_mouse_pos() -> tuple[int, int]:
    current_pos = pygame.mouse.get_pos()
    
    converted_x = (current_pos[0] - 65) / 835 * 2
    converted_y = current_pos[1] / 835 * 2
    
    return (round(converted_x), round(converted_y))