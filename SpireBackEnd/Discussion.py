# Stores all information about a discussion
class Discussion():
    def __init__(self, class_start, class_end):
        self.class_start = class_start
        self.class_end = class_end

    def get_start(self):
        return self.class_start

    def get_end(self):
        return self.class_end