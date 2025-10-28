from database import Base

##
print(Base.classes.keys())
task = Base.classes.Task

class Task(task):
    pass
