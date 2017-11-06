from SpireBackEnd.Lecture import Lecture

# A class that stores all sections of the course and Course data
class Course():
    def __init__(self, course_subject, course_num, num_credits):
        self.lectures = []
        self.course_subject = course_subject
        self.course_num = course_num
        self.num_credits = num_credits

    def size(self):
        return len(self.lectures)
    def add_lecture(self, section):
        self.lectures.append(section)
    def get_lecture(self, index):
        return self.lectures[index]
    def get_course_subject(self):
        return self.course_subject
    def get_course_num(self):
        return self.course_num
    def get_credits(self):
        return self.num_credits