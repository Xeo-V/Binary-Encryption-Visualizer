import pygame
from cryptography.fernet import Fernet

pygame.init()
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
BIT_COLOR = (95, 221, 229)
NEW_BIT_COLOR = (255, 0, 0)
FONT_SIZE = 20
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Binary Data Visualization')
font = pygame.font.SysFont('Courier', FONT_SIZE)
char_width, char_height = font.size('0')

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bytes_to_binary(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

def draw_binary_data(surface, binary_data, start_x, start_y, bit_color, new_bit_color, font, page, lines_per_page, char_width):
    x, y = start_x, start_y
    start_index = page * lines_per_page * BITS_PER_LINE
    end_index = start_index + lines_per_page * BITS_PER_LINE
    binary_data = binary_data[start_index:end_index]

    for i, bit in enumerate(binary_data):
        color = new_bit_color if i == 0 else bit_color
        bit_surface = font.render(bit, True, color)
        surface.blit(bit_surface, (x, y))
        x += char_width
        if x >= WIDTH // 2 - char_width and start_x == 10:
            x = 10
            y += char_height
        elif x >= WIDTH and start_x == WIDTH // 2 + 10:
            x = WIDTH // 2 + 10
            y += char_height
        if y >= start_y + lines_per_page * char_height:
            break

def create_button(surface, x, y, width, height, text, font):
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    surface.blit(text_surface, (x + 10, y + 10))

key = Fernet.generate_key()
cipher = Fernet(key)
with open('D:/github projects/encryptionVisualization/fileToBeEncrypted.txt', 'r') as file:
    file_content = file.read()

original_binary = text_to_binary(file_content)
encrypted_content = cipher.encrypt(file_content.encode())
encrypted_binary = bytes_to_binary(encrypted_content)

running = True
clock = pygame.time.Clock()
page = 0
lines_per_page = (HEIGHT - BUTTON_HEIGHT - 10) // char_height
BITS_PER_LINE = (WIDTH // 2) // char_width
total_pages = max(len(original_binary), len(encrypted_binary)) // (lines_per_page * BITS_PER_LINE) + 1
button_font = pygame.font.SysFont('Arial', 24)
up_button_rect = pygame.Rect(10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
down_button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if up_button_rect.collidepoint(event.pos) and page > 0:
                page -= 1
            elif down_button_rect.collidepoint(event.pos) and page < total_pages - 1:
                page += 1

    window.fill(BACKGROUND_COLOR)
    draw_binary_data(window, original_binary, 10, 10, BIT_COLOR, NEW_BIT_COLOR, font, page, lines_per_page, char_width)
    draw_binary_data(window, encrypted_binary, WIDTH // 2 + 10, 10, BIT_COLOR, NEW_BIT_COLOR, font, page, lines_per_page, char_width)
    create_button(window, 10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Up', button_font)
    create_button(window, WIDTH - BUTTON_WIDTH - 10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Down', button_font)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
