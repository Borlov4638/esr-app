
import glob
import os
import numpy
from pattern import Pattern
from percents import Percents
from pitchDetection import PitchDetect
from config import Config
from ranges import Ranges

config = Config()

inputFiles = glob.glob(config.get_input_path())
generalFiles = glob.glob(config.get_general_path())
pitch_array = []                                            #Массив частот всех аудиофайлов датасета

for file in generalFiles:
        pitch = PitchDetect(file).getFreqArrayFromFile(config.get_time(), config.get_floor(), config.get_ceiling())
        pitch_array += pitch.tolist() #разве можно вставлять частоты файлов просто подряд друг за другом? в таком случае будут и такие группы, куда входят конец одного файла и начало другого и тогда это нарушит картину

percentage_arr = Percents(config.get_step_pat(), pitch_array).get_percents() #Рассчет массива процентов, где каждый элемент массива - отдельный аудиофайл
percentage_arr = [file_data_in_perc for file_data_in_perc in percentage_arr if file_data_in_perc >= 0]

percentage_arr.sort()
print(percentage_arr)

for level in range(5,21):

    print(str(level) + '++++++++++++++++++++++++++++++++++++++++++')
    

    #TODO Решить проблему с модулем генерацией уровней, а именно с переменной X - идет рассчет слишком большого количества уровней
    ranges = Ranges(percentage_arr).getRanges(level)

    for i in inputFiles:
        fileName = os.path.basename(i)                                                                                  #Берет имя waf файла
        pitch = PitchDetect(i).getFreqArrayFromFile(config.get_time(), config.get_floor(), config.get_ceiling())
        pitch = pitch.tolist()
        per = Percents(config.get_step_pat(), pitch).get_percents()
        per = [i for i in per if i >= 0]
        pat = Pattern(per, level).pattern(ranges, per)
        if not os.path.exists(config.get_output_path() +"/P"+ str(level)):
            os.mkdir(config.get_output_path() +"/P"+ str(level))
        o_temp = config.get_output_path() +"/P"+ str(level) + "/Pattern---" + fileName + ".txt"
        f = open(o_temp, "a")
        f.write(str(pat))
        f.close()
        

    # Эта часть отвечает за то чтобы сгруппировать все получившиеся паттерны с данным значением уровня в один файл
    
    folder_path = config.get_output_path() +"/P"+ str(level)  # указываем путь к папке с файлами
    output_file = config.get_output_path() +"/P"+ str(level) + "/Output.txt"  # указываем имя файла, в котором будут записаны данные

    with open(output_file, "w") as out_file:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):   # Проверяем, что это текстовый файл
                with open(os.path.join(folder_path, filename), "r") as in_file:
                    contents = in_file.read().strip()  # Читаем файл и удаляем начальные и конечные пробелы
                    if contents:  # Проверяем содержимое на отсутствие пустых строк
                        out_file.write(contents + "\n")  # Добавляем содержимое файла в выходной файл

    with open(output_file, "r+") as out_file:
        out_file.seek(0, os.SEEK_END)  # Перемещаем указатель в конец файла
        pos = out_file.tell() - 1     # Определяем позицию последнего символа
        while pos > 0 and out_file.read(1) != "\n":  # Перемещаемся назад до первого символа конца строки
            pos -= 1
            out_file.seek(pos, os.SEEK_SET)
        if pos > 0:  # Если найден символ конца строки, обрезаем файл
            out_file.seek(pos, os.SEEK_SET)
            out_file.truncate()
