
class exercises():
    def __init__(self, name, bodypart):
        self.name=name
        self.bodypart=bodypart

class rep_ex(exercises):
    def __init__(self, name, bodypart, weight, rep_goal):
        super().__init__(name, bodypart)
        self.weight = weight
        self.rep_goal = rep_goal

    def print(self): 
        print("Exercise: "+self.name)
        print("Weight: "+self.weight)
        print("Reps: "+self.rep_goal)

    def to_json(self):
        return {"name": self.name, "bodypart": self.bodypart, "weight": self.weight, "rep_goal": self.rep_goal}

class dur_ex(exercises):
    def __init__(self, name, bodypart, dur_goal):
        super().__init__(name, bodypart)
        self.dur_goal = dur_goal

    def print(self): 
        print("------------------\nExercise: "+self.name+"\n------------------")
        print("Duration: "+self.dur_goal)

    def to_json(self):
        return {"name": self.name, "bodypart": self.bodypart, "dur_goal": self.dur_goal}