import pygame
import sys
import turtle

from fractals.koch import koch, koch_snowflake, minkowski
from fractals.basic import draw_binary_tree
from fractals.complex import levy, dragon, ice_fractal_1, ice_fractal_2

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Фрактальная мастерская")
clock = pygame.time.Clock()


BG_COLOR = (30, 30, 40)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 160, 210)
BORDER_COLOR = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, width=2, border_radius=12)

        font = pygame.font.SysFont("Arial", 20, bold=True)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.action()


def run_turtle(func, *args, **kwargs):
    """Запускает функцию рисования, ждет закрытия окна и возвращает управление в Pygame."""
    import time

    try:
        screen_turtle = turtle.Screen()
    except turtle.Terminator:
        turtle.TurtleScreen._RUNNING = True
        screen_turtle = turtle.Screen()

    screen_turtle.setup(width=800, height=600)
    screen_turtle.title(f"Рисование: {func.__name__}. Закройте окно для возврата.")

    turtle.reset()
    turtle.speed(0)
    turtle.pencolor("black")
    turtle.pensize(1)

    exit_flag = False

    def on_close():
        nonlocal exit_flag
        exit_flag = True
        screen_turtle.getcanvas().winfo_toplevel().destroy()

    screen_turtle.onclick(None)
    root = screen_turtle.getcanvas().winfo_toplevel()
    root.protocol("WM_DELETE_WINDOW", on_close)

    func(*args, **kwargs)

    while not exit_flag:
        if screen_turtle.getcanvas().winfo_exists():
            screen_turtle.update()
        time.sleep(0.01)

    try:
        turtle.bye()
    except turtle.Terminator:
        pass

    pygame.event.pump()
    pygame.event.clear()

buttons = []
button_data = [
    ("Кривая Коха", lambda: run_turtle(koch, 4, 300)),
    ("Снежинка Коха", lambda: run_turtle(koch_snowflake, 4, 300)),
    ("Кривая Минковского", lambda: run_turtle(minkowski, 4, 300)),
    ("Кривая Леви", lambda: run_turtle(levy, 10, 100)),
    ("Ледяной фрактал 1", lambda: run_turtle(ice_fractal_1, 5, 20)),
    ("Ледяной фрактал 2", lambda: run_turtle(ice_fractal_2, 5, 20)),
    ("Дракон Хартера", lambda: run_turtle(dragon, 10, 100)),
    ("Двоичное дерево", lambda: run_turtle(lambda: (turtle.left(90), draw_binary_tree(7, 100, 30)))),
]

start_x, start_y = 50, 100
btn_w, btn_h = 350, 60
gap_x, gap_y = 50, 20

for i, (name, action) in enumerate(button_data):
    col = i % 2
    row = i // 2
    x = start_x + col * (btn_w + gap_x)
    y = start_y + row * (btn_h + gap_y)
    buttons.append(Button(x, y, btn_w, btn_h, name, action))

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for btn in buttons:
            btn.handle_event(event)

    screen.fill(BG_COLOR)

    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    title_surf = title_font.render("Фрактальная мастерская", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_surf, title_rect)

    for btn in buttons:
        btn.check_hover(mouse_pos)
        btn.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()