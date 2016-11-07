class BasePattern(object):
    capacity = (1, 1)

    def __init__(self, name):
        self.name = name


class BlankPattern(BasePattern):
    def matchQ(self, other):
        return True


class RawPattern(BasePattern):
    def __init__(self, name, value):
        super(RawPattern, self).__init__(name)
        self.value = value

    def matchQ(self, other):
        return self.value == other


class BlankSequencePattern(BlankPattern):
    capacity = (1, 2**63)


class BlankNullSequencePattern(BlankPattern):
    capacity = (0, 2**63)
