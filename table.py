from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Создаем пример DataFrame
data = {
    "Coin": ('UBQ', 'HYPRA', 'ETNT', 'ETHW', 'CAU', 'ETC', 'DOGETHER', 'PWR', 'OCTA', 'LRS', 'XPB', 'BTN', 'DUBX',
             'EGAZ', 'AVS', 'CLO', 'ELH', 'REDEV2', 'DIS', 'NYBC'),
    "Profit 1GH/day": range(11, 31),
    "Coins 1GH/day": range(21, 41),
    "Coin price": range(31, 51),
    "Volume 24h": range(41, 61)
}
df = pd.DataFrame(data)


def load_font(fnt_path, fnt_size):
    try:
        font = ImageFont.truetype(fnt_path, fnt_size)
    except IOError:
        font = ImageFont.load_default()

    return font


def calculate_text_height(fnt_path, fnt_size, pad_y):
    """
    Вычисляет высоту строки текста с учетом вертикальных отступов.

    :param fnt_path: Путь к файлу шрифта.
    :param fnt_size: Размер шрифта.
    :param pad_y: Вертикальный отступ.
    :return: Высота строки текста с учетом отступов.
    """
    # Загрузка шрифта
    font = load_font(fnt_path, fnt_size)

    # Создание временного изображения для рисования текста
    dummy_image = Image.new("RGB", (100, 100), "white")
    dummy_draw = ImageDraw.Draw(dummy_image)

    # Рисование текста для измерения на изображении
    text = "Ag_test"  # Пример текста для измерения высоты
    dummy_draw.text((0, 0), text, fill="black", font=font)
    bbox = dummy_draw.textbbox((0, 0), text=text, font=font)

    # Получение ограничивающего прямоугольника для текста
    # bbox = dummy_image.getbbox()

    # Расчет размеров текста
    if bbox:
        text_height = bbox[3] - bbox[1]
    else:
        text_height = 0

    # Расчет высоты строки с учетом вертикальных отступов
    line_height = text_height + pad_y * 2

    return line_height


def draw_rounded_corner(draw, x0, y0, x1, y1, position, radius=10, fill="lightgrey", border="black", border_width=1):
    # Расчет для внешнего скругления (бордер)
    outer_x0, outer_y0, outer_x1, outer_y1 = x0, y0, x1, y1

    # Расчет для внутреннего скругления (заливка)
    inner_x0 = x0 + border_width
    inner_y0 = y0 + border_width
    inner_x1 = x1 - border_width
    inner_y1 = y1 - border_width
    # Внешний скругленный угол (бордер)
    if position == 'top_left':
        draw.pieslice([outer_x0, outer_y0, outer_x0 + 2 * radius, outer_y0 + 2 * radius], 180, 270, fill=border)
        draw.rectangle([(x0 + radius, y0), (x1, y1)], fill=fill)  # Заполнение остальной части ячейки
        draw.rectangle([(x0, y0 + radius), (x1, y1)], fill=fill)
    elif position == 'top_right':
        draw.pieslice([outer_x1 - 2 * radius, outer_y0, outer_x1, outer_y0 + 2 * radius], 270, 360, fill=border)
        draw.rectangle([(x0, y0), (x1 - radius, y1)], fill=fill)
        draw.rectangle([(x0, y0 + radius), (x1, y1)], fill=fill)
    elif position == 'bottom_left':
        draw.pieslice([outer_x0, outer_y1 - 2 * radius, outer_x0 + 2 * radius, outer_y1], 90, 180, fill=border)
        draw.rectangle([(x0 + radius, y0), (x1, y1)], fill=fill)
        draw.rectangle([(x0, y0), (x1, y1 - radius)], fill=fill)
    elif position == 'bottom_right':
        draw.pieslice([outer_x1 - 2 * radius, outer_y1 - 2 * radius, outer_x1, outer_y1], 0, 90, fill=border)
        draw.rectangle([(x0, y0), (x1 - radius, y1)], fill=fill)
        draw.rectangle([(x0, y0), (x1, y1 - radius)], fill=fill)

    # Внутренний скругленный угол (заливка), чтобы скрыть внешний бордер
    if position == 'top_left':
        draw.pieslice(
            [inner_x0, inner_y0, inner_x0 + 2 * (radius - border_width), inner_y0 + 2 * (radius - border_width)], 180,
            270, fill=fill)
    elif position == 'top_right':
        draw.pieslice(
            [inner_x1 - 2 * (radius - border_width), inner_y0, inner_x1, inner_y0 + 2 * (radius - border_width)], 270,
            360, fill=fill)
    elif position == 'bottom_left':
        draw.pieslice(
            [inner_x0, inner_y1 - 2 * (radius - border_width), inner_x0 + 2 * (radius - border_width), inner_y1], 90,
            180, fill=fill)
    elif position == 'bottom_right':
        draw.pieslice(
            [inner_x1 - 2 * (radius - border_width), inner_y1 - 2 * (radius - border_width), inner_x1, inner_y1], 0, 90,
            fill=fill)

    # Рисование оставшихся сторон бордера
    if position == 'top_left':
        draw.line([(x0 + radius, y0), (x1, y0)], fill=border, width=border_width)
        draw.line([(x0, y0 + radius), (x0, y1)], fill=border, width=border_width)
        draw.line([(x0, y1), (x1, y1)], fill=border, width=border_width)
    elif position == 'top_right':
        draw.line([(x0, y0), (x1 - radius, y0)], fill=border, width=border_width)
        draw.line([(x1, y0 + radius), (x1, y1)], fill=border, width=border_width)
        draw.line([(x0, y0), (x0, y1)], fill=border, width=border_width)
    elif position == 'bottom_left':
        draw.line([(x0 + radius, y1), (x1, y1)], fill=border, width=border_width)
        draw.line([(x0, y0), (x0, y1 - radius)], fill=border, width=border_width)
        draw.line([(x0, y0), (x1, y0)], fill=border, width=border_width)
    elif position == 'bottom_right':
        draw.line([(x0, y1), (x1 - radius, y1)], fill=border, width=border_width)
        draw.line([(x1, y0), (x1, y1 - radius)], fill=border, width=border_width)
        draw.line([(x0, y0), (x1, y0)], fill=border, width=border_width)


def draw_table(dataframe, fnt_path_header, fnt_path_body, fnt_size, pad_x, pad_y, img_width):
    num_cols = len(dataframe.columns)
    num_rows = len(dataframe)

    radius = 12

    cell_width = (img_width - start_x * 2) / len(dataframe.columns)
    cell_height = calculate_text_height(fnt_path_header, fnt_size, padding_y)

    # Создание изображения
    image_height = start_y * 2 + cell_height * (len(dataframe) + 1)  # Для заголовков и всех строк
    img = Image.new("RGB", (img_width, int(image_height)), "white")
    draw = ImageDraw.Draw(img)
    font_header = load_font(fnt_path_header, fnt_size)
    font_body = load_font(fnt_path_body, fnt_size)

    # Рисование заголовков таблицы
    for i, column in enumerate(dataframe.columns):
        x0 = start_x + cell_width * i
        y0 = start_y
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        # draw.rectangle(((x0, y0), (x1, y1)), outline="black", fill="lightgrey")
        # draw.text((x0 + pad_x, y0 + pad_y), column, fill="black", font=font)

        if i == 0:  # Первая ячейка
            draw_rounded_corner(draw, x0, y0, x1, y1, 'top_left', radius, "lightgrey", 'white')
            draw.text((x0 + pad_x, y0 + pad_y), column, fill="black", font=font_header)
        elif i == num_cols - 1:  # Последняя ячейка
            draw_rounded_corner(draw, x0, y0, x1, y1, 'top_right', radius, "lightgrey", 'white')
            draw.text((x0 + pad_x, y0 + pad_y), column, fill="black", font=font_header)
        else:
            draw.rectangle(((x0, y0), (x1, y1)), outline="white", fill="lightgrey")
            draw.text((x0 + pad_x, y0 + pad_y), column, fill="black", font=font_header)

    # Рисование данных таблицы
    for row_index, row in dataframe.iterrows():
        y0 = start_y + cell_height * (row_index + 1)
        for col_index, cell in enumerate(row):
            x0 = start_x + cell_width * col_index
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            # draw.rectangle(((x0, y0), (x1, y1)), outline="black", fill="white")
            # draw.text((x0 + pad_x, y0 + pad_y), str(cell), fill="black", font=font)

            if row_index == num_rows - 1:  # Последняя строка
                if col_index == 0:  # Первая ячейка
                    draw_rounded_corner(draw, x0, y0, x1, y1, 'bottom_left', radius, 'white', 'white')
                    draw.text((x0 + pad_x, y0 + pad_y), str(cell), fill="black", font=font_body)
                elif col_index == num_cols - 1:  # Последняя ячейка
                    draw_rounded_corner(draw, x0, y0, x1, y1, 'bottom_right', radius, 'white', 'white')
                    draw.text((x0 + pad_x, y0 + pad_y), str(cell), fill="black", font=font_body)
                else:
                    draw.rectangle(((x0, y0), (x1, y1)), outline="white", fill="white")
                    draw.text((x0 + pad_x, y0 + pad_y), str(cell), fill="black", font=font_body)
            else:
                draw.rectangle(((x0, y0), (x1, y1)), outline="white", fill="white")
                draw.text((x0 + pad_x, y0 + pad_y), str(cell), fill="black", font=font_body)

    return img


# Конфигурируем таблицу
image_width = 800

start_x = 10
start_y = 10

padding_x = 24
padding_y = 12

font_path_cells = 'font/Roboto-Regular.ttf'
font_path_header = 'font/Roboto-Bold.ttf'
font_size = 15

# Рисуем таблицу
image = draw_table(dataframe=df,
                   fnt_path_header=font_path_header,
                   fnt_path_body=font_path_cells,
                   fnt_size=font_size,
                   pad_x=padding_x,
                   pad_y=padding_y,
                   img_width=image_width
                   )

# Сохраняем изображение
image.save("table_image.png")
