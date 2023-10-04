import openpyxl 
import numpy as np

def askii(text):
    #text = input("enter a string to convert into ascii values:")
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values



##Заполняем матрицу расстояний
def fill_dtw_cost_matrix(s1, s2):
    l_s_1, l_s_2 = len(s1), len(s2)
    cost_matrix = np.zeros((l_s_1+1, l_s_2+1))
    for i in range(l_s_1+1):
        for j in range(l_s_2+1):
            cost_matrix[i, j] = np.inf
    cost_matrix[0, 0] = 0
    
    for i in range(1, l_s_1+1):
        for j in range(1, l_s_2+1):
            cost = abs(s1[i-1] - s2[j-1])
            
            prev_min = np.min([cost_matrix[i-1, j], cost_matrix[i, j-1], cost_matrix[i-1, j-1]])
            cost_matrix[i, j] = cost + prev_min

    
    cost_matrix = cost_matrix[1:, 1:]
    return cost_matrix

def dp(dist_mat):

    N, M = dist_mat.shape
    
    # Инициализация матрицы расстояний
    cost_mat = np.zeros((N + 1, M + 1))
    for i in range(1, N + 1):
        cost_mat[i, 0] = np.inf
    for i in range(1, M + 1):
        cost_mat[0, i] = np.inf

    # Заполнение матрицы расстояний с сохранением информации о пути
    traceback_mat = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            penalty = [
                cost_mat[i, j],      # match (0)
                cost_mat[i, j + 1],  # insertion (1)
                cost_mat[i + 1, j]]  # deletion (2)
            i_penalty = np.argmin(penalty)
            cost_mat[i + 1, j + 1] = dist_mat[i, j] + penalty[i_penalty]
            traceback_mat[i, j] = i_penalty

    # Возврат из нижнего правого угла
    i = N - 1
    j = M - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        tb_type = traceback_mat[i, j]
        if tb_type == 0:
            # Match
            i = i - 1
            j = j - 1
        elif tb_type == 1:
            # Insertion
            i = i - 1
        elif tb_type == 2:
            # Deletion
            j = j - 1
        path.append((i, j))

    # Убираем бесконечности из cost_mat до отображения
    distanceFin = cost_mat[dist_mat.shape]
    #print (cost_mat[dist_mat.shape])
    cost_mat = cost_mat[1:, 1:]
    #print (path[::-1])
    #print (cost_mat)
    #print (cost_mat([M-3][N-3]))
    return (distanceFin )

def check_min(path, seriesDif):
    min = 10000
    f = open(path, 'r')
    lines = f.read().splitlines()
    for line in lines:
        line = askii(line)
        temp = dp(fill_dtw_cost_matrix(seriesDif, line))
        if temp < min:
            min = temp
    f.close
    return (min)

# def count_lines_in_files(file1, file2, file3):
#     total_lines = 0
#     with open(file1, 'r') as f1:
#         total_lines += len(f1.readlines())
#     with open(file2, 'r') as f2:
#         total_lines += len(f2.readlines())
#     with open(file3, 'r') as f3:
#         total_lines += len(f3.readlines())
#     return total_lines

#=========================================================================================
#=========================================================================================



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


        # print('     Злость:', (check_min(anger, askii(input))))
        # print('     Радость:', (check_min(happyness, askii(input))))
        # print('     Спокойствие:', (check_min(calm, askii(input))))
        # print("     ===============================")
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

# extract_modify_replace(anger_file)
# extract_modify_replace(calm_file)
# extract_modify_replace(happyness_file)
# print(np.array([extract_modify_replace(anger_file), extract_modify_replace(calm_file), extract_modify_replace(happyness_file)]))
# print(extract_modify_replace(anger_file))


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

	