
import turtle
from math import sqrt


# --------------------------------------------------
# 1. КРИВАЯ КОХА
# --------------------------------------------------

def koch(order: int, size: float) -> None:
    """Рекурсивно рисует одну кривую Коха."""
    if order < 0:
        raise ValueError("Глубина не может быть отрицательной")

    if size <= 0:
        raise ValueError("Длина должна быть положительной")

    if order == 0:
        turtle.forward(size)
    else:
        part = size / 3

        koch(order - 1, part)
        turtle.left(60)

        koch(order - 1, part)
        turtle.right(120)

        koch(order - 1, part)
        turtle.left(60)

        koch(order - 1, part)


# --------------------------------------------------
# 2. СНЕЖИНКА КОХА
# --------------------------------------------------

def koch_snowflake(order: int, size: float) -> None:
    """Рисует снежинку из трёх кривых Коха."""
    if order < 0:
        raise ValueError("Глубина не может быть отрицательной")

    if size <= 0:
        raise ValueError("Длина должна быть положительной")

    for _ in range(3):
        koch(order, size)
        turtle.right(120)


# --------------------------------------------------
# 3. КРИВАЯ МИНКОВСКОГО
# --------------------------------------------------

def minkowski(order: int, size: float) -> None:
    """Рекурсивно рисует кривую Минковского."""
    if order < 0:
        raise ValueError("Глубина не может быть отрицательной")

    if size <= 0:
        raise ValueError("Длина должна быть положительной")

    if order == 0:
        turtle.forward(size)
    else:
        part = size / 4

        minkowski(order - 1, part)
        turtle.left(90)

        minkowski(order - 1, part)
        turtle.right(90)

        minkowski(order - 1, part)
        turtle.right(90)

        minkowski(order - 1, part)
        minkowski(order - 1, part)

        turtle.left(90)

        minkowski(order - 1, part)
        turtle.left(90)

        minkowski(order - 1, part)
        turtle.right(90)

        minkowski(order - 1, part)


# --------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# --------------------------------------------------

def move_to(x: float, y: float) -> None:
    """Перемещает черепашку без рисования."""
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.pendown()


def draw_label(x: float, y: float, text: str) -> None:
    """Пишет подпись в указанной точке."""
    turtle.penup()
    turtle.goto(x, y)
    turtle.write(
        text,
        align="center",
        font=("Arial", 14, "bold")
    )


# --------------------------------------------------
# РИСОВАНИЕ ФРАКТАЛОВ В НУЖНЫХ МЕСТАХ
# --------------------------------------------------

def draw_koch(
    order: int,
    size: float,
    x: float = -540,
    y: float = 170
) -> None:
    """Рисует кривую Коха с заданной глубиной и длиной."""
    move_to(x, y)
    koch(order, size)
    turtle.penup()


def draw_koch_snowflake(
    order: int,
    size: float,
    center_x: float = 250,
    center_y: float = 90
) -> None:
    """Рисует снежинку Коха с центром в заданной точке."""

    start_x = center_x - size / 2
    start_y = center_y + sqrt(3) * size / 6

    move_to(start_x, start_y)
    koch_snowflake(order, size)
    turtle.penup()


def draw_minkowski(
    order: int,
    size: float,
    x: float = -420,
    y: float = -230
) -> None:
    """Рисует кривую Минковского в заданной точке."""
    move_to(x, y)
    minkowski(order, size)
    turtle.penup()


# --------------------------------------------------
# ЗАПУСК ПРОГРАММЫ
# --------------------------------------------------

def main() -> None:
    try:
        order = int(input("Глубина рекурсии (рекомендуется 0–4): "))
        size = float(input("Длина стороны (например, 240): "))

        if order < 0:
            raise ValueError("Глубина не может быть отрицательной")

        if size <= 0 or size > 300:
            raise ValueError(
                "Длина должна быть больше 0 и не больше 300"
            )

    except ValueError as error:
        print("Ошибка ввода:", error)
        return

    screen = turtle.Screen()
    screen.setup(width=1200, height=800)
    screen.title("Фракталы: Кох и Минковский")
    screen.bgcolor("white")
    screen.tracer(0, 0)

    turtle.speed(0)
    turtle.pensize(2)
    turtle.hideturtle()

    # Кривая Коха
    turtle.pencolor("royalblue")
    draw_koch(order, size)
    draw_label(-420, 290, "Кривая Коха")

    # Снежинка Коха
    turtle.pencolor("darkgreen")
    draw_koch_snowflake(order, size)
    draw_label(250, 285, "Снежинка Коха")

    # Кривая Минковского
    turtle.pencolor("darkorange")
    draw_minkowski(order, size)
    draw_label(-300, -110, "Кривая Минковского")




if __name__ == "__main__":
    turtle.done()

