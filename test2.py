import pygame

pygame.init()

# Listet alle verfügbaren Systemschriftarten
font_list = pygame.font.get_fonts()

for font_name in font_list:
    print(font_name)

pygame.quit()