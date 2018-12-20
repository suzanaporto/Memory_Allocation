class Process:

    def __init__(self, id_p, name, burst_time, color, arrival_time, size, x_place=0, y_place=0):

        self.id_p = id_p
        self.name = name
        self.burst_time = burst_time
        self.color = color
        self.arrival_time = arrival_time
        self.size = size
        self.x_place = x_place
        self.y_place = y_place
