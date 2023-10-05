class Percents:
    def __init__(self, step, array_of_freq):
        self.step = step
        self.array_of_freq = array_of_freq

    def get_percents(self):
        percents = []
        split_array = [self.array_of_freq[d:d + self.step] for d in range(0, len(self.array_of_freq), self.step)]
        
        for freq_group in range(len(split_array)):
            maximum = max(split_array[freq_group]) #вычисляется максимальное значение в группе
            minimum = self.minim_non_zero(split_array[freq_group])              #А почему не берутся крайние значения, а просто максимум и минимум в группе, ведь между максимумом и минимумом может быть больщо перпад
                                                                                #Но первое значние группы может быть практически равным последнему?
            percent = ((maximum - minimum) / minimum) * 100                     #Что тут вообще происходит... почему проценты рассчитваются так?
            if percent != 0:
                percents.append(percent)
        return percents

    def minim_non_zero(self, list):
        minim = max(list)
        for i in list:
            if minim > i and i >= 1: 
                minim = i
        if minim == 0:
            minim = 1   #Почему минимум приравенивается именно к единице? Не лучше ли будет убрать элементы массивов в которых просто нет частоты? иначе будут несуществующие перепады частот, если их можно так назвать
        return minim
