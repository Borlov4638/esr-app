import parselmouth

class PitchDetect:
    #Этот класс предназначен для проеобразования аудиофайла в массив частот
    def __init__(self, path):
        self.sound = parselmouth.Sound(path)

    def getFreqArrayFromFile(self, time, floor, ceiling):
        pitch = self.sound.to_pitch(time, floor, ceiling)
        pitchArray = pitch.selected_array['frequency']
        pitchArray = pitchArray[pitchArray != 0]
        return pitchArray
