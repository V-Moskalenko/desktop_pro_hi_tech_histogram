import logging
import os

import customtkinter as ctk
from PIL import Image
from tkinter import filedialog

from basic_logic import create_df_list, main_bar
from support_module import setup_logging

ctk.set_appearance_mode("dark")

logger = logging.getLogger(__name__)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PRO Hi-Tech")  # Заголовок окна
        self.geometry("1200x800")  # Размер окна при открытии
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Загружаем картинки -------------------------------------------------------------------------------------
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image")

        # Логотип "PRO Hi-Tech"
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "avatar.jpeg")), size=(100, 100))

        # Картинка "Распознавание документов"
        self.ocr_text_image = ctk.CTkImage(Image.open(os.path.join(image_path, "OCR_text_image.png")), size=(500, 150))

        # Логотип Excel
        self.excel_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "icon_excel.png")), size=(40, 40))

        # Логотип Данные
        self.data_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "data_icon.png")), size=(40, 40))

        # Картинки кнопки "Домой"
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                       dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))

        # Поле навигации ------------------------------------------------------------------------------------------
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, width=1000)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # Наполнение поля навигации:
        # - логотип с названием
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="",
                                                   image=self.logo_image,
                                                   compound="left",
                                                   font=ctk.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # - кнопка "Домой"
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Главная страница",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        # - кнопка выбора темы приложения
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame,
                                                      values=["Dark", "Light", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")
        # Конец блока Навигации ---------------------------------------------------------------------------------

        # Страницы приложения -----------------------------------------------------------------------------------
        # - Главная страница
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(10, weight=1)
        # -- картинка "Создание гистограммы"
        self.ocr_image = ctk.CTkLabel(self.home_frame, text="", image=self.ocr_text_image)
        self.ocr_image.grid(row=0, column=0, padx=20, pady=10)

        # -- поле для ввода разрешения исходной картинки и настроек
        self.image_height = ctk.CTkEntry(self.home_frame, placeholder_text="Высота картинки (1440)", width=400)
        self.image_width = ctk.CTkEntry(self.home_frame, placeholder_text="Ширина картинки (2560)", width=400)
        self.font_name_size = ctk.CTkEntry(self.home_frame, placeholder_text="Размер шрифта наименования графика (60)",
                                           width=400)
        self.font_x_y_size = ctk.CTkEntry(self.home_frame, placeholder_text="Размер шрифта оси X и Y (60)", width=400)
        self.font_value_size = ctk.CTkEntry(self.home_frame, placeholder_text="Размер шрифта значений графика (40)",
                                            width=400)
        self.font_legend_size = ctk.CTkEntry(self.home_frame, placeholder_text="Размер шрифта легенды (60)", width=400)
        self.zero_y = ctk.CTkCheckBox(self.home_frame, text="Нулевая линия оси Y")
        self.image_height.grid(row=1, column=0, padx=20, pady=10)
        self.image_width.grid(row=2, column=0, padx=20, pady=10)
        self.font_name_size.grid(row=3, column=0, padx=20, pady=10)
        self.font_x_y_size.grid(row=4, column=0, padx=20, pady=10)
        self.font_value_size.grid(row=5, column=0, padx=20, pady=10)
        self.font_legend_size.grid(row=6, column=0, padx=20, pady=10)
        self.zero_y.grid(row=7, column=0, padx=20, pady=10)

        # -- кнопка "Выберете файл"
        self.file_button = ctk.CTkButton(self.home_frame, text="Выберете excel файл",
                                         image=self.excel_icon_image, width=400, height=50,
                                         command=self.get_file)
        self.file_button.grid(row=8, column=0, padx=20, pady=10)
        # -- блок имени выбранного файла
        self.home_data = ctk.CTkTextbox(self.home_frame, width=400, height=30, corner_radius=0)
        self.home_data.grid(row=9, column=0)

        self.select_frame_by_name("Главная страница")

        # Новое окно
        self.toplevel_window = None

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

        # Действие при нажатии кнопки "Домой"

    def home_button_event(self):
        self.select_frame_by_name("Главная страница")

    def select_frame_by_name(self, name):
        """
        Функция действия (перехода на страницу) по нажатию кнопки, передаётся параметр наименования кнопки.

        :param name: Имя кнопки
        :return:
        """
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Главная страница" else "transparent")

        # Открыть назначенную страницу приложения по кнопке
        if name == "Главная страница":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def get_file(self) -> None:
        """
        Метод действия по кнопке "Выберете excel файл"

        :return: Открывает указанную папку с сохраненными гистограммами
        """
        # Очистим блок имени выбранного файла от старых значений
        self.home_data.delete("0.0", "end")
        # Вызовем окно получения файла
        ask = filedialog.askopenfilename(title="Выбор excel файла")
        text_ask = f'{os.path.basename(ask)}'
        logger.info(f"Получил на вход файл: {text_ask}")
        self.home_data.insert(index="0.0", text=text_ask)

        df_list = create_df_list(ask)

        save_dir_path = filedialog.askdirectory(title="Выберете папку для сохранения")
        logger.info(f"Выбрана папка для сохранения графиков: {save_dir_path}")

        try:
            height_png = int(self.image_height.get()) if self.image_height.get() else 1440
            width_png = int(self.image_width.get()) if self.image_width.get() else 2560
            font_name_size = int(self.font_name_size.get()) if self.font_name_size.get() else 60
            font_x_y_size = int(self.font_x_y_size.get()) if self.font_x_y_size.get() else 60
            font_value_size = int(self.font_value_size.get()) if self.font_value_size.get() else 40
            font_legend_size = int(self.font_legend_size.get()) if self.font_legend_size.get() else 60
            zero_y = True if self.zero_y.get() else False
        except Exception as e:
            logger.error(f'Ошибка в методе get_file: {e}')

        logger.info("Запускаю метод формирования графиков")
        try:
            main_bar(df_list=df_list, dir_path=save_dir_path, height_png=height_png, width_png=width_png,
                     font_name_size=font_name_size, font_x_y_size=font_x_y_size, font_value_size=font_value_size,
                     font_legend_size=font_legend_size, zero_y=zero_y)
        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")

        logger.info("Открываю папку с графиками")
        os.startfile(save_dir_path)


if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Запускаю приложение")
    app = App()
    app.mainloop()
    logger.info("Приложение остановленно")
    # pyinstaller --add-data "image;image" --onefile application.py
    # pyinstaller --noconfirm --onedir --windowed --add-data ".\.venv\Lib\site-packages\customtkinter;customtkinter\" --add-data "image;image"  application.py
