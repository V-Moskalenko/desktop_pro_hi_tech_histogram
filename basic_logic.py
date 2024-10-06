import logging

import pandas
from PIL import Image, ImageDraw
from plotly.subplots import make_subplots
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

CONSTANT_BRAND = ('RTX', 'RX', 'ARC', 'NVIDIA', 'RYZEN', 'AMD', 'INTEL', 'I3', 'I5', 'I7', 'I9')


def create_df_list(excel_path: str):
    """
    Метод формирует DataFrame из каждого листа переданного excel файла

    :param excel_path: путь до excel файла
    :return:
    """
    xls = pandas.ExcelFile(excel_path)
    sheet_names = xls.sheet_names
    df_list = [xls.parse(sheet, parse_dates=True) for sheet in sheet_names]
    xls.close()
    return df_list


def get_videocart_color(value: str) -> str:
    """
    Метод формирование цвета по бренду видеокарты или процессора

    :param value: текст значения столбца
    :return: цвет
    """
    if any([value.upper().startswith(i) for i in ('RTX', 'NVIDIA')]):
        return '#76B900'
    elif any([value.upper().startswith(i) for i in ('RX', 'RYZEN', 'AMD', 'R3', 'R5', 'R7', 'R9')]):
        return '#af1319'  # '#FF4500'
    elif any([value.upper().startswith(i) for i in ('ARC', 'INTEL', 'I3', 'I5', 'I7', 'I9')]):
        return '#0071c5'
    else:
        return 'yellow'


def get_colors_from_list(df_x_values) -> list:
    """
    Если столбцы содержат информацию о видеокарте или процессоре, сформируем список цветов бренда

    :param df_x_values: значения столбцов
    :return: список цветов
    """
    check = any([i in j for i in CONSTANT_BRAND for j in df_x_values.str.upper().to_list()])
    if check:
        result = [get_videocart_color(value) for value in df_x_values]
        return result


def create_df_bar(df,
                  save_dir: str,
                  height_png: int = 1440,
                  width_png: int = 2560,
                  font_name_size: int = 60,
                  font_x_y_size: int = 60,
                  font_value_size: int = 40,
                  font_legend_size: int = 60,
                  zero_y: bool = False) -> str:
    """
    Формирование гистограммы

    :param df: DataFrame с данными
    :param save_dir: путь до сохранения изображения
    :param height_png: высота изображения
    :param width_png: ширина изображения
    :param font_name_size: размер шрифта названия гистограммы
    :param font_x_y_size: размер шрифта оси гистограммы
    :param font_value_size: размер шрифта данных гистограммы
    :param font_legend_size: размер шрифта легенды гистограммы
    :param zero_y: флаг отображения оси Y на гистограмме
    :return: путь до сохраненного изображения
    """
    cell_a1 = df.columns[0]
    test_name, y_title = cell_a1[:cell_a1.index('(')].strip(), cell_a1[cell_a1.index('(') + 1: cell_a1.index(')')]

    # Создание гистограммы
    fig = make_subplots(rows=1, cols=1)

    time_flag = False
    for metric in df.columns.tolist()[1:]:
        colors = get_colors_from_list(df[df.columns[0]])

        fig.add_trace(
            go.Bar(
                x=df[df.columns[0]],
                y=df[metric],
                name=metric,
                text=df[metric],
                textposition='outside',
                marker_color=colors,
                marker_line=dict(color='black', width=3),
                showlegend=True,
                textfont=dict(size=font_value_size, family="Bebas Neue, sans-serif")
            ),
            row=1, col=1
        )

    # Настройка внешнего вида
    fig.update_layout(
        autosize=True,
        height=height_png, width=width_png,
        title=dict(text=test_name.upper(), x=0.1, y=0.9),
        title_font_size=font_name_size,
        yaxis_title=y_title,
        yaxis_title_font_size=font_x_y_size,
        legend_title_font_size=font_legend_size,
        legend=dict(yanchor="bottom", y=0.9, xanchor="right", x=0.9, orientation='h', bgcolor='rgba(0,0,0,0)',
                    itemsizing='constant',
                    font=dict(
                        family="Bebas Neue, sans-serif",
                        size=font_legend_size,
                        color="white"),
                    ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Bebas Neue, sans-serif", size=font_value_size, color="white"),
        margin=dict(t=100, b=100, l=300, r=300),  # Отступы
        xaxis=dict(showgrid=False),
        yaxis=dict(
            domain=[0, 0.75],  # Высота гистограммы
            showgrid=False,
            showticklabels=False,
            zeroline=zero_y,
            type='date',
            tickformat='%H:%M',
        ) if time_flag else dict(showgrid=False,
                                 showticklabels=False,
                                 zeroline=zero_y,
                                 domain=[0, 0.75])
    )

    fig.update_yaxes(title_standoff=0)
    # Сохранение гистограммы в PNG
    save_path = f'{save_dir}/{test_name}.png'
    fig.write_image(save_path, height=height_png, width=width_png)
    pillow_background_color(save_path, height=height_png, width=width_png)
    return save_path


def pillow_background_color(save_path: str, height: int, width: int) -> str:
    """
    Наложение темного полупрозрачного слоя на изображение

    :param save_path: путь до изображения
    :param height: высота
    :param width:ширина
    :return: путь до изображения
    """
    with Image.open(save_path).convert("RGBA") as image:
        alpha = int(0.20 * 255)
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        # Создать ограниченный слой, можно применить ко всей картинке, тогда строки с draw пропустить
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([100, 50, (width - 100), (height - 50)], fill=(0, 0, 0, alpha))
        combined = Image.alpha_composite(image, overlay)
        combined.save(save_path)
        return save_path


def main_bar(df_list: list,
             dir_path: str,
             height_png: int = 1440,
             width_png: int = 2560,
             font_name_size: int = 60,
             font_x_y_size: int = 60,
             font_value_size: int = 40,
             font_legend_size: int = 60,
             zero_y: bool = False
             ):
    try:
        for df in df_list:
            create_df_bar(df=df,
                          save_dir=dir_path,
                          height_png=height_png,
                          width_png=width_png,
                          font_name_size=font_name_size,
                          font_x_y_size=font_x_y_size,
                          font_value_size=font_value_size,
                          font_legend_size=font_legend_size,
                          zero_y=zero_y)
        logger.info("Метод формирования графиков, отработал")
        return True
    except Exception as e:
        logger.error(e)
        return False
