from mesa import Agent
from mesa.time import RandomActivation
import random


class Seed(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Fine"
        
        
    
    def spread_disease(self):
        if self.condition == "Contaminated":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "Fine":
                    if random.random() < 1:
                        neighbor.condition = "Contaminated"
            if random.random() < 1:
                self.condition = "Dead"
            else:
                self.condition = "Fine"
                
                
    
    def die(self):
        if self.condition == "Dead":
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
    
                
    def step(self):
        self.spread_disease()
        self.die()
        
        

class TreeAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Fine"
        self.distance = 'none'


    