import os
import openpyxl 
from classifier import Classifier

classifier = Classifier(
    os.environ.get('PATTERNS_ANGER_FILE'),
    os.environ.get('PATTERNS_HAPPYNESS_FILE'),
    os.environ.get('PATTERNS_CALM_FILE'),
    os.environ.get('PATTERNS_DISGUST_FILE'),
    os.environ.get('PATTERNS_FEAR_FILE')
    )

def askii(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values


def extract_modify_replace(filename):
    i=0
    file_emote = ''
    if filename == os.environ.get('PATTERNS_ANGER_FILE'):
        file_emote = 'Злость'
    if filename == os.environ.get('PATTERNS_HAPPYNESS_FILE'):
        file_emote = 'Счастье'
    if filename == os.environ.get('PATTERNS_CALM_FILE'):
        file_emote = 'Спокойствие'
    if filename == os.environ.get('PATTERNS_DISGUST_FILE'):
        file_emote = 'Отвращение'
    if filename == os.environ.get('PATTERNS_FEAR_FILE'):
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
        anger = classifier.check_min(os.environ.get('PATTERNS_ANGER_FILE'), askii(input))
        print('Злость:' + str(anger))
        happyness = classifier.check_min(os.environ.get('PATTERNS_HAPPYNESS_FILE'), askii(input))
        print('Радость:' + str(happyness))
        calm = classifier.check_min(os.environ.get('PATTERNS_CALM_FILE'), askii(input))
        print('Спокойствие:' + str(calm))
        disgust = classifier.check_min(os.environ.get('PATTERNS_DISGUST_FILE'), askii(input))
        print('Отвращение:' + str(disgust))
        fear = classifier.check_min(os.environ.get('PATTERNS_FEAR_FILE'), askii(input))
        print('Страх:' + str(fear))
        classified = classifier.find_min_var_name(anger, happyness, calm, disgust, fear)
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

# Создаем новый файл Excel
workbook = openpyxl.Workbook()
# Выбираем активный лист
worksheet = workbook.active
# Задаем значения для матрицы
matrix = [["Реальная эмоция снизу/справа классифицируемая",'Злость' ,'Счастье' ,'Спокойствие' ,'Отвращение' ,'Страх' ],
    extract_modify_replace(os.environ.get('PATTERNS_ANGER_FILE')),
    extract_modify_replace(os.environ.get('PATTERNS_HAPPYNESS_FILE')),
    extract_modify_replace(os.environ.get('PATTERNS_CALM_FILE')),
    extract_modify_replace(os.environ.get('PATTERNS_DISGUST_FILE')),
    extract_modify_replace(os.environ.get('PATTERNS_FEAR_FILE'))
]
print(matrix)
# Записываем матрицу в ячейки на листе
for row in matrix:
    worksheet.append(row)

# Сохраняем файл
workbook.save('C:\\Users\mrwig\OneDrive\Desktop\matrix.xlsx')

	