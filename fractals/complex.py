import turtle
import math
from fractals.koch import move_to


def ice_fractal_1(order: int, size: float, center_x: float = -300, center_y: float = 0) -> None:
    """
    «Ледяной» фрактал №1.
    :param order: Глубина рекурсии (порядок фрактала).
    :param size: Длина базового отрезка.
    """
    turtle.tracer(0)
    
    if turtle.pen()["pendown"] and turtle.heading() == 0 and turtle.pos() == (0.0, 0.0):
        move_to(center_x, center_y)

    if order == 0:
        turtle.forward(size)
    else:
        ice_fractal_1(order - 1, size, center_x, center_y)

        turtle.left(90)
        ice_fractal_1(order - 1, size * 0.5, center_x, center_y)

        turtle.right(180)
        ice_fractal_1(order - 1, size * 0.5, center_x, center_y)

        turtle.left(90)

        ice_fractal_1(order - 1, size, center_x, center_y)


def ice_fractal_2(order: int, size: float, center_x: float = -300, center_y: float = 0) -> None:
    """
    «Ледяной» фрактал №2.
    :param order: Глубина рекурсии (порядок фрактала).
    :param size: Длина базового отрезка.
    """
    turtle.tracer(0)
    
    if turtle.pen()["pendown"] and turtle.heading() == 0 and turtle.pos() == (0.0, 0.0):
        move_to(center_x, center_y)

    if order == 0:
        turtle.forward(size)
    else:
        ice_fractal_2(order - 1, size, center_x, center_y)

        turtle.left(120)
        ice_fractal_2(order - 1, size * 0.5, center_x, center_y)

        turtle.right(180)
        ice_fractal_2(order - 1, size * 0.5, center_x, center_y)

        turtle.left(120)
        ice_fractal_2(order - 1, size * 0.5, center_x, center_y)

        turtle.right(180)
        ice_fractal_2(order - 1, size * 0.5, center_x, center_y)

        turtle.left(120)
        ice_fractal_2(order - 1, size, center_x, center_y)


def levy(order: int, size: float) -> None:
    """
    Кривая Леви.
    :param order: Глубина рекурсии (порядок фрактала).
    :param size: Длина базового отрезка.
    """
    turtle.tracer(0)
    if order == 0:
        turtle.forward(size)
    else:
        turtle.left(45)
        levy(order - 1, size / math.sqrt(2))
        turtle.right(90)
        levy(order - 1, size / math.sqrt(2))
        turtle.left(45)


def dragon(order: int, size: float, direction: int = 1) -> None:
    """
    Дракон Хартера-Хейтуэя.
    :param order: Глубина рекурсии (порядок фрактала).
    :param size: Длина базового отрезка.
    :param direction: Направление поворота.
    """
    turtle.tracer(0)
    if order == 0:
        turtle.forward(size)
    else:
        turtle.left(direction * 45)
        dragon(order - 1, size / math.sqrt(2), 1)
        turtle.right(direction * 90)
        dragon(order - 1, size / math.sqrt(2), -1)
        turtle.left(direction * 45)


if __name__ == "__main__":
    
    turtle.update()
    turtle.done()
