from SpireBackEnd.Discussion import Discussion

# Stores all information about a lecture
class Lecture():
    def __init__(self, class_start, class_end, prof_name, hotness_rating):
        self.class_start = class_start
        self.class_end = class_end
        self.prof_name = prof_name
        self.hotness_rating = hotness_rating
        self.discussions = []

    def size(self):
        return len(self.discussions)
    def add_disc(self, discussion):
        self.discussions.append(discussion)

    def get_disc(self, index):
        return self.discussions[index]

    def get_prof(self):
        return self.prof_name

    def get_start(self):
        return self.class_start

    def get_end(self):
        return self.class_end

    def get_rating(self):
        return self.hotness_rating