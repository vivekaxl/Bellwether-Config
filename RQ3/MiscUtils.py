from collections import Counter

class Misc:
    @classmethod
    def uniques(cls, lst):
        return Counter(lst).keys()