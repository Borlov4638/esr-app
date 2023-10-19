
import glob
import os
import numpy
from pattern import Pattern
from percents import Percents
from pitchDetection import PitchDetect
from config import Config
from ranges import Ranges
from pymongo import MongoClient

def finder():
    all_files = []
    names = os.listdir(config.get_input_path())
    for name in names:
        fullname = os.path.join(config.get_input_path(), name)
        files = glob.glob(fullname + "/*.wav" )
        all_files += files
    return all_files
        


def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client

db = get_database()
config = Config()

inputFiles = finder()
generalFiles = glob.glob(config.get_general_path())
pitch_array = []                                            #Массив частот всех аудиофайлов датасета

for file in generalFiles:
    pitch = PitchDetect(file).getFreqArrayFromFile(config.get_time(), config.get_floor(), config.get_ceiling())
    pitch_array += pitch.tolist() #разве можно вставлять частоты файлов просто подряд друг за другом? в таком случае будут и такие группы, куда входят конец одного файла и начало другого и тогда это нарушит картину


percentage_arr = Percents(config.get_step_pat(), pitch_array).get_percents() #Рассчет массива процентов, где каждый элемент массива - отдельный аудиофайл
percentage_arr = [file_data_in_perc for file_data_in_perc in percentage_arr if file_data_in_perc >= 0]

percentage_arr.sort()


print('Maccив процентов: \t')
print(percentage_arr)

for level in range(5,21):

    print(str(level) + '++++++++++++++++++++++++++++++++++++++++++')
    

    #TODO Решить проблему с модулем генерации уровней, а именно с переменной X - идет рассчет слишком большого количества уровней 
    # (Проблема проявляется только при малом общем количестве входных аудизаписей в tst)
    ranges = Ranges(percentage_arr).getRanges(level)


    for file in inputFiles:
        fileName = os.path.basename(file)                                                                                  
        pitch_array = PitchDetect(file).getFreqArrayFromFile(config.get_time(), config.get_floor(), config.get_ceiling())
        pitch_array = pitch_array.tolist()
        percent_array = Percents(config.get_step_pat(), pitch_array).get_percents()
        percent_array = [percent for percent in percent_array if percent >= 0]
        pattern = Pattern(percent_array, level).pattern(ranges, percent_array)

        emote = file.split('/')[-2:][0]
        db['patterns'][str(level)].insert_one({"pattern":pattern, "emotion": emote})
        

