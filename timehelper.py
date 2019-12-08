import datetime as dt

class Time:
    
    def __init__(self):
        self.time_left = 40
        self.overtime = 0

    def log_hours(self, hrs):
        assert(isinstance(hrs, int))
        if (self.time_left - hrs >= 0):
            self.time_left -= hrs
        else:
            self.overtime = hrs - self.time_left
            self.time_left = 0
    
    def get_time_left(self):
        return self.time_left
        
    def get_overtime(self):
        return self.overtime
    
    def reset_hours(self):
        self.time_left = 40
