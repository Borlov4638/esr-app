import os
from dotenv import load_dotenv, find_dotenv

env_var = load_dotenv(find_dotenv())

class Config:
    def __init__(self):
        self.i_path = os.environ.get('INPUT_FILES_DIRECTORY') + "/*.wav" or input('Путь к директории входных файлов:') + "\*.wav"
        self.o_path = os.environ.get('OUTPUT_PATTERNS_DIRECTORY') or input('Путь сохранения паттернов:')
        self.g_path = os.environ.get('ALL_FILES_DIRECTORY') + "/*.wav" or input('Путь к директории всех файлов:') + "\*.wav"
        self.time = float(os.environ.get('PITCH_TIME_STEP')) or float(input('Шаг для частот:'))
        self.floor = float(os.environ.get('FLOOR_F0')) or float(input('Нижняя граница ЧОТ:'))
        self.ceiling = float(os.environ.get('CEILING_F0')) or float(input('Верхняя граница ЧОТ:'))
        self.step_per = int(os.environ.get('PERCENTAGE_STEP')) or int(input('Шаг для процентов:'))
        self.step_pat = int(os.environ.get('PATTERN_STEP')) or int(input('Шаг для паттернов:'))


    def get_input_path(self):
        return self.i_path

    def get_output_path(self):
        return self.o_path

    def get_general_path(self):
        return self.g_path

    def get_time(self):
        return self.time

    def get_floor(self):
        return self.floor

    def get_ceiling(self):
        return self.ceiling

    def get_step_per(self):
        return self.step_per

    def get_step_pat(self):
        return self.step_pat