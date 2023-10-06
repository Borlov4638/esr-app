import numpy

class Ranges:
    def __init__(self, percentage_arr):
        self.percentage_arr = percentage_arr

    #По своей сути не является алфавитом. Эта функция возвращает массив чисел от 0 до 100
    #А сам массив представляет собой набор уровней, которым в последствии будут присвоены границы

    def falphabet(self):                         
        alph = []
        for number in range (0, 100):
            alph.append(str(number))
        return alph


    def getRanges(self, level):
        alphabet = self.falphabet()
        ranges = []
        level_char = 0
        X = (int)(len(self.percentage_arr)/(level-1))                #рассчет того, как много процентных значений будет в одном шаге цикла(в одном уровне)
        for i in range(0,(len(self.percentage_arr)),X):                                     #TODO скорее всего проблема возникает из-за того что оно не делится нацело
            if (i+X)>len(self.percentage_arr)-1:                                                         #условие для последнего уровня
                ranges.append((alphabet[level_char],self.percentage_arr[i],numpy.Inf))               
                print("================================================\n")
                print(ranges)
                break
            else:
                if i==0:
                    ranges.append((alphabet[level_char],0,self.percentage_arr[i+X]))                         #Условие для первого уровня
                    level_char+=1
                    print("================================================\n")
                    print(ranges)

                else:
                    ranges.append((alphabet[level_char],self.percentage_arr[i],self.percentage_arr[i+X]))         #условие для остальных уровней
                    level_char+=1
                    print("================================================\n")
                    print(ranges)
        # print(ranges)    
        return ranges

