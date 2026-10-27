import pygame
import turtle
import time

from fractals.koch import koch, koch_snowflake, minkowski
from fractals.basic import draw_binary_tree, draw_branch
from fractals.complex import levy, dragon, ice_fractal_1, ice_fractal_2

class InputField:
    def __init__(self, x, y, width, height, label, default_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = default_text
        self.active = False
        self.error = ""

    def draw(self, surface):
        font_label = pygame.font.SysFont("Arial", 18)
        label_surf = font_label.render(self.label, True, TEXT_COLOR)
        surface.blit(label_surf, (self.rect.x, self.rect.y - 25))

        color = INPUT_ACTIVE if self.active else INPUT_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, width=2, border_radius=8)

        font_text = pygame.font.SysFont("Arial", 20)
        text_surf = font_text.render(self.text, True, TEXT_COLOR)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

        if self.error:
            font_err = pygame.font.SysFont("Arial", 14)
            err_surf = font_err.render(self.error, True, ERROR_COLOR)
            surface.blit(err_surf, (self.rect.x, self.rect.y + self.rect.height + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() or event.unicode in ['.', '-']:
                self.text += event.unicode

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
INPUT_BG = (50, 50, 65)
INPUT_ACTIVE = (80, 80, 100)
ERROR_COLOR = (220, 80, 80)

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


def run_turtle(func, needs_angle=False, depth=4, size=100, angle=30):
    try:
        screen_turtle = turtle.Screen()
    except turtle.Terminator:
        turtle.TurtleScreen._RUNNING = True
        screen_turtle = turtle.Screen()

    screen_turtle.setup(width=800, height=600)
    screen_turtle.title(f"Рисование: {func.__name__}")

    turtle.reset()
    turtle.speed(0)
    turtle.pencolor("black")
    turtle.tracer(0)

    exit_flag = False

    def on_close():
        nonlocal exit_flag
        exit_flag = True
        screen_turtle.getcanvas().winfo_toplevel().destroy()

    screen_turtle.onclick(None)
    root = screen_turtle.getcanvas().winfo_toplevel()
    root.protocol("WM_DELETE_WINDOW", on_close)

    if needs_angle:
        func(depth, size, angle)
    else:
        func(depth, size)

    turtle.update()

    while not exit_flag:
        try:
            screen_turtle.update()
            time.sleep(0.01)
        except turtle.Terminator:
            break

    try:
        turtle.bye()
    except Exception:
        pass

    turtle.TurtleScreen._RUNNING = True
    pygame.event.pump()
    pygame.event.clear()


buttons = []
button_data = [
    ("Кривая Коха", koch, False),
    ("Снежинка Коха", koch_snowflake, False),
    ("Кривая Минковского", minkowski, False),
    ("Кривая Леви", levy, False),
    ("Ледяной фрактал 1", ice_fractal_1, False),
    ("Ледяной фрактал 2", ice_fractal_2, False),
    ("Дракон Хартера", dragon, False),
    ("Двоичное дерево", draw_binary_tree, True),
    ("Фрактал 'Ветка'", draw_branch, False),
]

app_state = "menu"
current_func = None
needs_angle = False
input_fields = []
btn_draw = None
btn_back = None

start_x, start_y = 50, 100
btn_w, btn_h = 350, 60
gap_x, gap_y = 50, 20

for i, (name, func, req_angle) in enumerate(button_data):
    col = i % 2
    row = i // 2
    x = start_x + col * (btn_w + gap_x)
    y = start_y + row * (btn_h + gap_y)


    def make_action(f, req):
        def action():
            global app_state, current_func, needs_angle, input_fields
            current_func = f
            needs_angle = req
            app_state = "input"
            input_fields = [
                InputField(250, 250, 400, 40, "Глубина рекурсии (целое > 0):", "4"),
                InputField(250, 350, 400, 40, "Начальный размер (> 0):", "100")
            ]
            if needs_angle:
                input_fields.append(InputField(250, 450, 400, 40, "Угол (0-90):", "30"))

        return action


    buttons.append(Button(x, y, btn_w, btn_h, name, make_action(func, req_angle)))

btn_draw = Button(300, 580, 150, 50, "Нарисовать", None)
btn_back = Button(470, 580, 150, 50, "Отмена", None)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if app_state == "menu":
            for btn in buttons:
                btn.handle_event(event)

        elif app_state == "input":
            for field in input_fields:
                field.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.rect.collidepoint(mouse_pos):
                    app_state = "menu"
                elif btn_draw.rect.collidepoint(mouse_pos):
                    is_valid = True
                    try:
                        depth = int(input_fields[0].text)
                        if depth <= 0: raise ValueError
                        input_fields[0].error = ""
                    except ValueError:
                        input_fields[0].error = "Нужно целое число > 0"
                        is_valid = False

                    try:
                        size = float(input_fields[1].text)
                        if size <= 0: raise ValueError
                        input_fields[1].error = ""
                    except ValueError:
                        input_fields[1].error = "Нужно число > 0"
                        is_valid = False

                    if needs_angle:
                        try:
                            angle = float(input_fields[2].text)
                            if not (0 < angle <= 90): raise ValueError
                            input_fields[2].error = ""
                        except ValueError:
                            input_fields[2].error = "Угол от 0 до 90"
                            is_valid = False

                    if is_valid:
                        app_state = "menu"
                        if needs_angle:
                            run_turtle(current_func, needs_angle=True, depth=depth, size=size, angle=angle)
                        else:
                            run_turtle(current_func, needs_angle=False, depth=depth, size=size)

    screen.fill(BG_COLOR)

    if app_state == "menu":
        title_font = pygame.font.SysFont("Arial", 40, bold=True)
        title_surf = title_font.render("Фрактальная мастерская", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_surf, title_rect)

        for btn in buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

    elif app_state == "input":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("Arial", 30, bold=True)
        title_surf = title_font.render(f"Параметры: {current_func.__name__}", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        for field in input_fields:
            field.draw(screen)

        btn_draw.check_hover(mouse_pos)
        btn_draw.draw(screen)
        btn_back.check_hover(mouse_pos)
        btn_back.draw(screen)

    pygame.display.flip()
    clock.tick(60)