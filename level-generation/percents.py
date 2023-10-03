class Percents:
    def __init__(self, step, array_of_freq):
        self.step = step
        self.array_of_freq = array_of_freq

    def get_percents(self):
        percents = []
        split_array = [self.array_of_freq[d:d + self.step] for d in range(0, len(self.array_of_freq), self.step)]
        for i in range(len(split_array)):
            maximum = max(split_array[i])
            minimum = self.minim_non_zero(split_array[i])
            percent = ((maximum - minimum) / minimum) * 100
            if percent != 0:
                percents.append(percent)
        return percents

    def minim_non_zero(self, list):
        minim = max(list)
        for i in list:
            if minim > i and i >= 1:
                minim = i
        if minim == 0:
            minim = 1
        return minim
