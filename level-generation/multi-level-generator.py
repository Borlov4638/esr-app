
import glob
import os
import numpy
from pattern import Pattern
from percents import Percents
from pitchDetection import PitchDetect

#По своей сути не является алфавитом. Эта функция возвращает массив чисел от 0 до 100
#А сам массив представляет собой набор уровней, которым в последствии будут присвоены границы
def falphabet():                         
    alph = []
    for i in range (0, 100):
        alph.append(str(i))
    return alph

alphabet = falphabet()

#TODO вынести в отдельный конфиг файл
#=========================================================
i_path = ''
o_path = ''
g_path = ''
time = 0.0
floor = 0.0
ceiling = 0.0
step_per = 0
step_pat = 0


if os.path.isfile('config.txt'):
    conf = open('config.txt')
    for string in conf:
        # if string[0] == 'A':
        #     alphabet = string[1:-1]
        if string[0] == 'I':
            i_path = string[1:-1] + "\*.wav"
        elif string[0] == 'O':
            o_path = string[1:-1]
        elif string[0] == 'G':
            g_path = string[1:-1] + "\*.wav"
        elif string[0] == 't':
            time = float(string[1:])
        elif string[0] == 'F':
            floor = float(string[1:])
        elif string[0] == 'C':
            ceiling = float(string[1:])
        elif string[0] == '%':
            step_per = int(string[1:])
        elif string[0] == 'P':
            step_pat = int(string[1:])
    conf.close()


if i_path == '':
    i_path = input('Путь к директории входных файлов:') + "\*.wav"
if o_path == '':
    o_path = input('Путь сохранения паттернов:')
if g_path == '':
    g_path = input('Путь к директории всех файлов:') + "\*.wav"
if time == 0.0:
    time = float(input('Шаг для частот:'))
if floor == 0.0:
    floor = float(input('Нижняя граница ЧОТ:'))
if ceiling == 0.0:
    ceiling = float(input('Верхняя граница ЧОТ:'))
if step_per == 0:    
    step_per = int(input('Шаг для процентов:'))
if step_pat == 0:
    step_pat = int(input('Шаг для паттернов:'))
    

#===============================================================

files = glob.glob(i_path)
globl = glob.glob(g_path)
array = []

for i in globl:
        pitch = PitchDetect(i).freq_array(time, floor, ceiling)
        temp = pitch.tolist()
        array += temp

proc = Percents(step_per, array).get_percents()
proc = [i for i in proc if i >= 0]

proc.sort()
print(proc)

for j in range(5,101):
    step_pat = j
    print(str(j) + '++++++++++++++++++++++++++++++++++++++++++')

    #------------------------------------------------------------------------------
    ranges = []
    cntr = 0
    X = (int)(len(proc)/(step_pat-1))
    for i in range(0,(len(proc)),X):
        if (i+X)>len(proc)-1:
            ranges.append((alphabet[cntr],proc[i],numpy.Inf))               #proc[len(proc)-1]+1
            print("================================================\n")
            print(ranges)
            break
        else:
            if i==0:
                ranges.append((alphabet[cntr],0,proc[i+X]))
                cntr+=1
                print("================================================\n")
                print(ranges)

            else:
                ranges.append((alphabet[cntr],proc[i],proc[i+X]))
                cntr+=1
                print("================================================\n")
                print(ranges)

    # print(ranges)
    #------------------------------------------------------------------------------




    for i in files:
        file = os.path.basename(i)
        pitch = PitchDetect(i).freq_array(time, floor, ceiling)
        pitch = pitch.tolist()
        per = Percents(step_per, pitch).get_percents()
        per = [i for i in per if i >= 0]
        pat = Pattern(per, step_pat).pattern(ranges, per)
        if not os.path.exists(o_path +"\P"+ str(j)):
            os.mkdir(o_path +"\P"+ str(j))
        o_temp = o_path +"\P"+ str(j) + "\Pattern---" + file + ".txt"
        f = open(o_temp, "a")
        f.write(str(pat))
        f.close()
        
    folder_path = o_path +"\P"+ str(j)  # указываем путь к папке с файлами
    output_file = o_path +"\P"+ str(j) + "\Output.txt"  # указываем имя файла, в котором будут записаны данные

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
