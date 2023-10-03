class Pattern:
    def __init__(self, percent, n):
        self.percent = percent
        self.segment = n

    def split(self):
        sort_array = sorted(self.percent)
        step = len(sort_array) // self.segment
        split_array = [sort_array[d:d + step] for d in range(0, len(sort_array), step)]
        return split_array


    def pattern(self, ranges, pc):          

        pattern = ''
        
        for i in pc:
            for j in ranges:
                if i>=j[1] and i<j[2]:
                    pattern+=(j[0]+' ')
        return pattern
