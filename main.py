import os
import sys
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append('./classificator')
sys.path.append('./level-generation')
from classificator.classifier import Classifier
from levelGeneration.percents import Percents
from levelGeneration.pitchDetection import PitchDetect
from levelGeneration.config import Config
from levelGeneration.pattern import Pattern
from pymongo import MongoClient

import time
start_time = time.time()


level = os.environ.get('PATTERN_LEVEL')

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client

db = get_database()

config = Config()

db_range_coursor = db['ranges'][str(level)].find()
db_range = [obj['level_ranges'] for obj in db_range_coursor][0]


file = '/home/karakul/diploma/esr-app/experemental-data/in/disgust/03-01-07-01-01-01-03.wav'

         

pitch_array = PitchDetect(file).getFreqArrayFromFile(config.get_time(), config.get_floor(), config.get_ceiling())

pitch_array = pitch_array.tolist()

percent_array = Percents(config.get_step_pat(), pitch_array).get_percents()

percent_array = [percent for percent in percent_array if percent >= 0]

pattern = Pattern(percent_array, level).pattern(db_range, percent_array)




classifier = Classifier(level)
print(classifier.classify(pattern))

print("Process finished --- %s seconds ---" % (time.time() - start_time))
    # Далее можно работать с результатом


