import logging
import math
import os
import sys

CANVAS_W = 100.0
CANVAS_H = 100.0


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | %(levelname)-7s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )


def parse_float_or_none(raw):
    if raw is None:
        return None
    s = raw.strip().replace(",", ".")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def classify_triangle(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "не треугольник"
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"
    if a == b == c:
        return "равносторонний"
    if a == b or a == c or b == c:
        return "равнобедренный"
    return "разносторонний"


def calculate_vertices(a, b, c):
    """
    Координаты вершин без масштабирования: 1 единица длины = 1 px.
    Фигура просто центрируется в поле 100x100.
    """
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

    # Сдвиг, чтобы центр фигуры совпал с центром поля.
    offset_x = (CANVAS_W - width) / 2 - min_x
    offset_y = (CANVAS_H - height) / 2 - min_y

    def to_screen(p):
        sx = p[0] + offset_x
        # Y инвертируем: в экранной системе ось Y направлена вниз.
        sy = CANVAS_H - (p[1] + offset_y)
        return int(round(sx)), int(round(sy))

    return [to_screen(A), to_screen(B), to_screen(C)]


def process_triangle(raw_a, raw_b, raw_c):
    a = parse_float_or_none(raw_a)
    b = parse_float_or_none(raw_b)
    c = parse_float_or_none(raw_c)

    if a is None or b is None or c is None:
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    ttype = classify_triangle(a, b, c)
    if ttype == "не треугольник":
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    return ttype, calculate_vertices(a, b, c)


def main():
    setup_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    try:
        raw_a = input("Сторона A: ")
        raw_b = input("Сторона B: ")
        raw_c = input("Сторона C: ")

        logging.info("Запрос: A=%r, B=%r, C=%r", raw_a, raw_b, raw_c)

        ttype, vertices = process_triangle(raw_a, raw_b, raw_c)

        logging.info("Результат: тип=%s, вершины=%s", ttype, vertices)

        print(f"Тип треугольника: {ttype!r}")
        print(f"Координаты вершин: {vertices}")

    except Exception:
        logging.error("Что-то пошло не так...")
        logging.exception("Заход в блок обработки исключения:")
        print("Ошибка: см. лог")


if __name__ == "__main__":
    main()