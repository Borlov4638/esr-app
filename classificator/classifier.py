import os
from classificator.dtw import Dtw
from classificator.testing import askii


class Classifier:
    def __init__(self):
        self.anger_path = os.environ.get('PATTERNS_ANGER_FILE'),
        self.happyness_path = os.environ.get('PATTERNS_HAPPYNESS_FILE'),
        self.calm_path = os.environ.get('PATTERNS_CALM_FILE'),
        self.disgust_path = os.environ.get('PATTERNS_DISGUST_FILE'),
        self.fear_path = os.environ.get('PATTERNS_FEAR_FILE')


    def classify(self):
        anger = self.check_min(self.anger_file, askii(input))
        print('Злость:' + str(anger))
        happyness =self.check_min(self.happyness_file, askii(input))
        print('Радость:' + str(happyness))
        calm = self.check_min(self.calm_file, askii(input))
        print('Спокойствие:' + str(calm))
        disgust = self.check_min(self.disgust_file, askii(input))
        print('Отвращение:' + str(disgust))
        fear = self.check_min(self.fear_file, askii(input))
        print('Страх:' + str(fear))
        return self.find_min_var_name(anger, happyness, calm, disgust, fear)
        

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
