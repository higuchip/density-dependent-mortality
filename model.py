from mesa import Model
from agents import TreeAgent, Seed
from scheduler import RandomActivationByTypeFiltered
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from pointpats import PointPattern
import pointpats.quadrat_statistics as qs


def get_mean_nnd(self):
        coords_seeds = []
        for (agents, x, y) in self.grid.coord_iter():
            if Seed in (type(agent) for agent in agents):
                coords_seeds.append([x, y])

        pp = PointPattern(coords_seeds)
        return pp.mean_nnd
            

            

class DispersalModel(Model):
    ''' 
    Simulação de dispersão de propágulos & Mortalidade Dependente de Densidade
    '''

    
    description = (
        "Desenvolvido por Pedro Higuchi. Contato: higuchip@gmail.com)" 
    )


    def __init__(self,
    width = 20, height = 20):
        super().__init__()
        '''
        Initialize the model.
        '''
        
        self.N = 1
        self.width = 50
        self.height = 50
        
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByTypeFiltered(self)

        self.datacollector = DataCollector(
            {
                'mdvp': get_mean_nnd            
            }
        )

        
        
        for i in range(self.N):
            a = TreeAgent(i, self)
            self.schedule.add(a)

            # add agent to the center of the grid

            x = int(self.grid.width / 2)
            y = int(self.grid.height / 2)
            self.grid.place_agent(a, (x, y))
     
            
           
            for (x, y) in self.grid.iter_neighborhood((int(self.grid.width / 2),int(self.grid.width / 2)), 
            moore=True, include_center=False, radius=4):
        
                if self.random.random() < 0.6:
                    seed = Seed((x, y), self)
                    if self.random.random()<0.1:
                        seed.condition = "Contaminated"
                    if self.grid.is_cell_empty((x, y)):
                        self.grid.place_agent(seed, (x, y))
                        self.schedule.add(seed)
                   

            for (x, y) in self.grid.iter_neighborhood((int(self.grid.width / 2),int(self.grid.width / 2)), moore=True, include_center=False, radius=10):
                if self.random.random() < 0.05:
                    seed = Seed((x, y), self)
                    if self.random.random()<0.1:
                        seed.condition = "Contaminated"
                    if self.grid.is_cell_empty((x, y)):
                        self.grid.place_agent(seed, (x, y))
                        self.schedule.add(seed)
               


        self.running = True


    def step(self):
        '''
        Advance the model by one step.
        '''
        self.schedule.step()

        
        # Halt if no more contamination
        seed_contaminated = (self.count_type(self, "Contaminated"))
        #print(seed_contaminated)
        if seed_contaminated <=1:
            self.running = False


        #print(self.datacollector.get_model_vars_dataframe())


         
         # Collect data each step
         # collect data



        self.datacollector.collect(self)
 
    
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

   
    