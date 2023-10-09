import numpy as np

#При инициализации объекта класса передаются 2 строки, для которых требуется применить метод DTW

class Dtw:
        ##Заполняем матрицу расстояний
    def __init__(self, s1, s2):
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
        self.dist_mat = cost_matrix

    def getDistance(self):

        N, M = self.dist_mat.shape
        
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
                cost_mat[i + 1, j + 1] = self.dist_mat[i, j] + penalty[i_penalty]
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
        distanceFin = cost_mat[self.dist_mat.shape]
        #print (cost_mat[dist_mat.shape])
        cost_mat = cost_mat[1:, 1:]
        return (distanceFin )


        
