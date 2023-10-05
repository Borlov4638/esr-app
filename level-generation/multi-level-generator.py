
import glob
import os
import numpy
from pattern import Pattern
from percents import Percents
from pitchDetection import PitchDetect
from config import Config


#По своей сути не является алфавитом. Эта функция возвращает массив чисел от 0 до 100
#А сам массив представляет собой набор уровней, которым в последствии будут присвоены границы
def falphabet():                         
    alph = []
    for number in range (0, 100):
        alph.append(str(number))
    return alph

alphabet = falphabet()
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

for j in range(5,20):
    level = j
    print(str(j) + '++++++++++++++++++++++++++++++++++++++++++')

    #------------------------------------------------------------------------------
    ranges = []
    level_char = 0
    X = (int)(len(percentage_arr)/(level-1))                #рассчет того, как много процентных значений будет в одном шаге цикла(в одном уровне)
    for i in range(0,(len(percentage_arr)),X):
        if (i+X)>len(percentage_arr)-1:                                                         #условие для последнего уровня
            ranges.append((alphabet[level_char],percentage_arr[i],numpy.Inf))               
            print("================================================\n")
            print(ranges)
            break
        else:
            if i==0:
                ranges.append((alphabet[level_char],0,percentage_arr[i+X]))                         #Условие для первого уровня
                level_char+=1
                print("================================================\n")
                print(ranges)

            else:
                ranges.append((alphabet[level_char],percentage_arr[i],percentage_arr[i+X]))         #условие для остальных уровней
                level_char+=1
                print("================================================\n")
                print(ranges)

    # print(ranges)
    #------------------------------------------------------------------------------


    for i in inputFiles:
        file = os.path.basename(i)
        pitch = PitchDetect(i).getFreqArrayFromFile(config.get_time(), config.get_floor(), config.get_ceiling())
        pitch = pitch.tolist()
        per = Percents(config.step_per(), pitch).get_percents()
        per = [i for i in per if i >= 0]
        pat = Pattern(per, level).pattern(ranges, per)
        if not os.path.exists(config.o_path +"\P"+ str(j)):
            os.mkdir(config.o_path +"\P"+ str(j))
        o_temp = config.o_path +"\P"+ str(j) + "\Pattern---" + file + ".txt"
        f = open(o_temp, "a")
        f.write(str(pat))
        f.close()
        
    folder_path = config.o_path +"\P"+ str(j)  # указываем путь к папке с файлами
    output_file = config.o_path +"\P"+ str(j) + "\Output.txt"  # указываем имя файла, в котором будут записаны данные

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
