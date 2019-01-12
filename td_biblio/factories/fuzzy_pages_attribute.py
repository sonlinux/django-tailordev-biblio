import random

from factory.fuzzy import BaseFuzzyAttribute

# Custom fuzzy attributes definition


class FuzzyPages(BaseFuzzyAttribute):
    """Random pages numbers separated by double-hyphens"""

    def __init__(self, low, high=None, **kwargs):
        if high is None:
            high = low
            low = 1

        self.low = low
        self.high = high

        super(FuzzyPages, self).__init__(**kwargs)

    def fuzz(self):
        start = random.randint(self.low, self.high)
        end = random.randint(start, self.high)
        return "%d--%d" % (start, end)
