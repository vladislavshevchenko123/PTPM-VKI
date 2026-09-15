import math
import logging

CANVAS_W = 100.0
CANVAS_H = 100.0
MARGIN = 5.0

logger = logging.getLogger(__name__)


def parse_positive_float(raw, field_name):
    s = raw.strip().replace(",", ".")
    if not s:
        raise ValueError(f"{field_name}: пустая строка")
    try:
        v = float(s)
    except ValueError:
        raise ValueError(f"{field_name}: не является числом")
    if v <= 0:
        raise ValueError(f"{field_name}: должно быть положительным")
    return v


def classify_triangle(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Треугольник с такими сторонами не существует")

    if a == b == c:
        side_type = "равносторонний"
    elif a == b or a == c or b == c:
        side_type = "равнобедренный"
    else:
        side_type = "разносторонний"

    s1, s2, s3 = sorted((a, b, c))
    if s3 ** 2 == s1 ** 2 + s2 ** 2:
        angle_type = "прямоугольный"
    elif s3 ** 2 < s1 ** 2 + s2 ** 2:
        angle_type = "остроугольный"
    else:
        angle_type = "тупоугольный"

    return side_type, angle_type


def calculate_vertices(a, b, c):
    A = (0.0, 0.0)
    B = (c, 0.0)

    x = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    y = math.sqrt(b ** 2 - x ** 2)
    C = (x, y)

    xs = [A[0], B[0], C[0]]
    ys = [A[1], B[1], C[1]]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    scale = min(
        (CANVAS_W - 2 * MARGIN) / width,
        (CANVAS_H - 2 * MARGIN) / height,
    )

    offset_x = (CANVAS_W - width * scale) / 2
    offset_y = (CANVAS_H - height * scale) / 2

    def to_screen(p):
        sx = offset_x + (p[0] - min_x) * scale
        sy = CANVAS_H - (offset_y + (p[1] - min_y) * scale)
        return round(sx, 2), round(sy, 2)

    return {"A": to_screen(A), "B": to_screen(B), "C": to_screen(C)}


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        a = parse_positive_float(input("Сторона A: "), "A")
        b = parse_positive_float(input("Сторона B: "), "B")
        c = parse_positive_float(input("Сторона C: "), "C")

        side_type, angle_type = classify_triangle(a, b, c)
        vertices = calculate_vertices(a, b, c)

        logger.info("Вид по сторонам: %s", side_type)
        logger.info("Вид по углам: %s", angle_type)
        logger.info("Вершины: %s", vertices)

        print(f"Вид по сторонам: {side_type}")
        print(f"Вид по углам: {angle_type}")
        for name, p in vertices.items():
            print(f"  {name}: {p}")

    except ValueError as exc:
        logger.error("Ошибка: %s", exc)
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()