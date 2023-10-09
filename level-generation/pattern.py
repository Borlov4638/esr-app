class Pattern:
    def __init__(self, percent_array, level):
        self.percent_array = percent_array
        self.level = level

    def split(self):
        sort_array = sorted(self.percent_array)
        step = len(sort_array) // self.level
        split_array = [sort_array[d:d + step] for d in range(0, len(sort_array), step)]
        return split_array


    def pattern(self, ranges, percentage_array):          

        pattern = ''
        for percent in percentage_array:
            for single_range in ranges:
                if percent>=single_range[1] and percent<single_range[2]:
                    pattern+=(single_range[0]+' ')
        return pattern
