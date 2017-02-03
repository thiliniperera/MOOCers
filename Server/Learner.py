import json

class Learner:

    def __init__(self, name, index, grade):
        self.name = name
        self.index = index
        self.grade = grade


    def getLearner(self):
        return self.name + " "+self.grade

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)