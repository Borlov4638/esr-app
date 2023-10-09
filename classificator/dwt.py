import openpyxl 
import numpy as np
from dtw import Dtw



def askii(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values

def check_min(path, inputPattern):
    min = 10000
    f = open(path, 'r')
    lines = f.read().splitlines()
    for line in lines:
        line = askii(line)
        temp = Dtw(inputPattern, line).getDistance()
        if temp < min:
            min = temp
    f.close
    return (min)

def find_min_var_name(a, b, c, d, e):
    smallest = a
    if b < smallest:
        smallest = b
    if c < smallest:
        smallest = c
    if d < smallest:
        smallest = d
    if e < smallest:
        smallest = e
    if smallest == a:
        return "anger"
    elif smallest == b:
        return "happyness"
    elif smallest == c:
        return "calm"
    elif smallest == d:
        return "disgust"
    else:
        return "fear"

def extract_modify_replace(filename):
    i=0
    file_emote = ''
    if filename == anger_file:
        file_emote = 'Злость'
    if filename == happyness_file:
        file_emote = 'Счастье'
    if filename == calm_file:
        file_emote = 'Спокойствие'
    if filename == disgust_file:
        file_emote = 'Отвращение'
    if filename == fear_file:
        file_emote = 'Страх'
    
    anger_count = 0
    happyness_count = 0
    calm_count = 0
    disgust_count = 0
    fear_count = 0

    print('*********************************************\n' + filename + "\n*********************************************\n")
    file_lines = 0
    with open(filename, 'r') as f1:
        file_lines += len(f1.readlines())
    for l in range(file_lines) :
        

        with open(filename, 'r') as f:
            lines = f.readlines()
            input = lines[l] # Извлекаем первую строку
            del lines[l] # Удаляем первую строку из списка
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line) # Перезаписываем остальное содержимое файла

        i=i+1
        print(str(i) + "     ===============================")
        anger = check_min(anger_file, askii(input))
        print('Злость:' + str(anger))
        happyness =check_min(happyness_file, askii(input))
        print('Радость:' + str(happyness))
        calm = check_min(calm_file, askii(input))
        print('Спокойствие:' + str(calm))
        disgust = check_min(disgust_file, askii(input))
        print('Отвращение:' + str(disgust))
        fear = check_min(fear_file, askii(input))
        print('Страх:' + str(fear))
        classified = find_min_var_name(anger, happyness, calm, disgust, fear)
        if classified == 'anger':
            anger_count += 1
        if classified == 'happyness':
            happyness_count += 1
        if classified == 'calm':
            calm_count += 1
        if classified == 'disgust':
            disgust_count += 1
        if classified == 'fear':
            fear_count += 1

        with open(filename, 'r') as f:
            lines = f.readlines()
        lines.insert(l, input) # Вставляем новую строку перед указанной строкой
        with open(filename, 'w') as f:
            f.writelines(lines) # Перезаписываем содержимое файла с новой строкой

    global_count = [file_emote, anger_count, happyness_count, calm_count, disgust_count, fear_count]
    return global_count


anger_file = 'C:\\Users\mrwig\OneDrive\Desktop\\EmoDB\P20\\Angry_male.txt'
happyness_file = 'C:\\Users\mrwig\OneDrive\Desktop\\EmoDB\P20\\Calm_male.txt'
calm_file = 'C:\\Users\mrwig\OneDrive\Desktop\\EmoDB\P20\\Happy_male.txt'
disgust_file = 'C:\\Users\mrwig\OneDrive\Desktop\\EmoDB\P20\\Disgust_male.txt'
fear_file = 'C:\\Users\mrwig\OneDrive\Desktop\\EmoDB\P20\\Fear_male.txt'

# Создаем новый файл Excel
workbook = openpyxl.Workbook()
# Выбираем активный лист
worksheet = workbook.active
# Задаем значения для матрицы
matrix = [["Реальная эмоция снизу/справа классифицируемая",'Злость' ,'Счастье' ,'Спокойствие' ,'Отвращение' ,'Страх' ],
    extract_modify_replace(anger_file),
    extract_modify_replace(happyness_file),
    extract_modify_replace(calm_file),
    extract_modify_replace(disgust_file),
    extract_modify_replace(fear_file)
]
print(matrix)
# Записываем матрицу в ячейки на листе
for row in matrix:
    worksheet.append(row)

# Сохраняем файл
workbook.save('C:\\Users\mrwig\OneDrive\Desktop\matrix.xlsx')

	