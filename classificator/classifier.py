import os
from mongo_init import mongoClient

from dtw import Dtw

client = mongoClient()

class Classifier:
    def __init__(self, level):
        anger_array = client['patterns'][str(level)].find({'emotion': 'anger'})
        self.anger_patterns = [obj['pattern'] for obj in anger_array]

        calm_array = client['patterns'][str(level)].find({'emotion': 'calm'})
        self.calm_patterns = [obj['pattern'] for obj in calm_array]

        happy_array = client['patterns'][str(level)].find({'emotion': 'happyness'})
        self.happy_patterns = [obj['pattern'] for obj in happy_array]

        disgust_array = client['patterns'][str(level)].find({'emotion': 'disgust'})
        self.disgust_patterns = [obj['pattern'] for obj in disgust_array]

        fear_array = client['patterns'][str(level)].find({'emotion': 'fear'})
        self.fear_patterns = [obj['pattern'] for obj in fear_array]

    def classify(self, input_pattern):
        anger = self.check_min(self.anger_patterns, askii(input_pattern))
        print('Злость:' + str(anger))
        happyness =self.check_min(self.happy_patterns, askii(input_pattern))
        print('Радость:' + str(happyness))
        calm = self.check_min(self.calm_patterns, askii(input_pattern))
        print('Спокойствие:' + str(calm))
        disgust = self.check_min(self.disgust_patterns, askii(input_pattern))
        print('Отвращение:' + str(disgust))
        fear = self.check_min(self.fear_patterns, askii(input_pattern))
        print('Страх:' + str(fear))
        return self.find_min_var_name(anger, happyness, calm, disgust, fear)
        

    def check_min(self, patterns_array, inputPattern):
        min = 100000
        for pattern in patterns_array:
            pattern = askii(pattern)
            temp = Dtw(inputPattern, pattern).getDistance()
            if temp < min:
                min = temp

        return (min)

    def find_min_var_name(self, a, b, c, d, e):
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

def askii(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values

