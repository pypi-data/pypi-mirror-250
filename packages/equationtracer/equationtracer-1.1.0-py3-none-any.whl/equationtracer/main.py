import pygame
import pyperclip
from numpy import *


def main():
    n = input("Enter Degree of Equation [Default - 25]: ")
    n = 25 if n == '' else int(n)

    t = input("Enter Parameter Name [Default - \"t\"]: ")
    t = 't' if t == '' else t
    assert t.isalpha()

    s = input("Enter Size of Rendered Drawing (on the Coordinate Grid) [Default - 10]: ")
    s = (10 if s == '' else int(s)) / 500

    x = input("Enter x-coord of Center of Rendered Drawing (on the Coordinate Grid) [Default - 0]: ")
    x = 0 if x == '' else int(x)

    y = input("Enter y-coord of Center of Rendered Drawing (on the Coordinate Grid) [Default - 0]: ")
    y = 0 if y == '' else int(y)

    screen = pygame.display.set_mode((500, 500))
    pygame.init()
    drawing = False
    points = []

    while True:
        term = False
        if drawing:
            points.append(list(pygame.mouse.get_pos()))

        for i in range(len(points) - 1):
            pygame.draw.line(screen, (255, 255, 255), points[i], points[i + 1], 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                term = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    term = True
                    break

        if term:
            pygame.quit()
            break

        pygame.display.update()

    for m in range(len(points) - 1, -1, -1):
        points[m] = (points[m][0] - 250, 250 - points[m][1])
        points.append(points[m])

    xt = yt = ""
    M = len(points)
    for k in range(-n, n + 1):
        cx = cy = 0
        for m in range(M):
            cx += cos(2 * pi * k * m / M) * points[m][0] + sin(2 * pi * k * m / M) * points[m][1]
            cy += cos(2 * pi * k * m / M) * points[m][1] - sin(2 * pi * k * m / M) * points[m][0]

        if k != -n:
            xt += " + "
            yt += " + "

        xt += f"{cx / M} cos({k * pi}{t}) - {cy / M} sin({k * pi}{t})"
        yt += f"{cx / M} sin({k * pi}{t}) + {cy / M} cos({k * pi}{t})"

    eq = f"({x} + {s}({xt}), {y} + {s}({yt}))".replace(" + -", " - ").replace(" - -", " + ")
    print(eq + "\n\nEquation Generated!\n")

    copyeq = input("Copy to Clipboard? (Y/n): ")
    if copyeq in ["", "Y", "y"]:
        pyperclip.copy(eq)
