import os
from dotenv import load_dotenv, find_dotenv
import openpyxl
from mongo_init import mongoClient
from classifier import Classifier
load_dotenv(find_dotenv())

client = mongoClient()

level = os.environ.get('PATTERN_LEVEL')

def askii(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values


def extract_modify_replace(emotion):
    i=0

    emotion_pattern_coursor = client['patterns'][str(level)].find({'emotion': emotion})
    print(emotion_pattern_coursor)
    emotion_pattern_array = [obj['pattern'] for obj in emotion_pattern_coursor]
    print(emotion_pattern_array)


    file_emote = ''
    if emotion == "anger":
        file_emote = 'Злость'
    if emotion == "happyness":
        file_emote = 'Счастье'
    if emotion == "calm":
        file_emote = 'Спокойствие'
    if emotion == "disgust":
        file_emote = 'Отвращение'
    if emotion == "fear":
        file_emote = 'Страх'
    
    anger_count = 0
    happyness_count = 0
    calm_count = 0
    disgust_count = 0
    fear_count = 0

    print('*********************************************\n' + emotion + "\n*********************************************\n")

    
    for pattern in range(len(emotion_pattern_array)):
        
        #Начинается с 0
        deleted_doc = client['patterns'][str(level)].find_one_and_delete({'emotion': emotion})
        input = emotion_pattern_array[pattern]
        print(input)
        i+=1

        print(str(i) + "     ===============================")

        classified = Classifier(level).classify(input)

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

        client['patterns'][str(level)].insert_one(deleted_doc)

        # with open(filename, 'r') as f:
        #     lines = f.readlines()
        # lines.insert(pattern, input) # Вставляем новую строку перед указанной строкой
        # with open(filename, 'w') as f:
        #     f.writelines(lines) # Перезаписываем содержимое файла с новой строкой
    global_count = [file_emote, anger_count, happyness_count, calm_count, disgust_count, fear_count]
    return global_count

# Создаем новый файл Excel
workbook = openpyxl.Workbook()
# Выбираем активный лист
worksheet = workbook.active
# Задаем значения для матрицы
matrix = [["Реальная эмоция снизу/справа классифицируемая",'Злость' ,'Счастье' ,'Спокойствие' ,'Отвращение' ,'Страх' ],
    extract_modify_replace("anger"),
    extract_modify_replace("happyness"),
    extract_modify_replace("calm"),
    extract_modify_replace("disgust"),
    extract_modify_replace("fear")
]
client.close()
print(matrix)
# Записываем матрицу в ячейки на листе
for row in matrix:
    worksheet.append(row)

# Сохраняем файл
workbook.save('C:\\Users\mrwig\OneDrive\Desktop\matrix.xlsx')

	