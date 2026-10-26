import turtle

# --------------------------------------------------
# 1. РЕКУРСИВНАЯ ФУНКЦИЯ ДЛЯ ДВОИЧНОГО ДЕРЕВА
# --------------------------------------------------

def draw_binary_tree(depth: int, size: float, angle: float) -> None:
    if depth == 0:
        turtle.forward(size)
        turtle.backward(size)
        return
    else:
        turtle.color('green')
        turtle.forward(size)
        turtle.right(angle)
        draw_binary_tree(depth - 1, size*0.65, angle)
        turtle.left(angle*2)
        draw_binary_tree(depth - 1, size*0.65, angle)
        turtle.color('brown')
        turtle.right(angle)
        turtle.backward(size)
        return

turtle.reset()
turtle.left(90)
draw_binary_tree(4, 100, 30)
turtle.done()



def draw_branch(n: int, size: float) -> None:
    pass