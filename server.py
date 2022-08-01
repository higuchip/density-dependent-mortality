import mesa
from agents import TreeAgent, Seed
from model import DispersalModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from pointpats import PointPattern
import pointpats.quadrat_statistics as qs

def get_mean_nnd(self):
        coords_seeds = []
        for (agents, x, y) in self.grid.coord_iter():
            if Seed in (type(agent) for agent in agents):
                coords_seeds.append([x, y])

        pp = PointPattern(coords_seeds)
       
        
        return f"Distância Média do Vizinho Mais Próximo: {round(pp.mean_nnd,1)}"

def get_max_nnd(self):
        coords_seeds = []
        for (agents, x, y) in self.grid.coord_iter():
            if Seed in (type(agent) for agent in agents):
                coords_seeds.append([x, y])

        pp = PointPattern(coords_seeds)
        return f"Distância Máxima do Vizinho Mais Próximo: {round(pp.max_nnd,1)}"

def get_min_nnd(self):
        coords_seeds = []
        for (agents, x, y) in self.grid.coord_iter():
            if Seed in (type(agent) for agent in agents):
                coords_seeds.append([x, y])

        pp = PointPattern(coords_seeds)
        return f"Distância Mínima do Vizinho Mais Próximo: {round(pp.min_nnd,1)}"
 
    
COLORS = {"Fine": "darkgreen", "Contaminated": "yellow"}

def seed_dispersal_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    if type(agent) is TreeAgent:
        portrayal["Shape"] =  "resources/tree.png"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    
    elif type(agent) is Seed:
        portrayal["Color"] = COLORS[agent.condition]
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.4
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1


    return portrayal


canvas_element = CanvasGrid(seed_dispersal_portrayal, 20, 20, 500, 500)

#chart_element = ChartModule([{"Label": "mdvp", "Color": "black"}])


server = mesa.visualization.ModularServer(
    DispersalModel, [get_min_nnd, get_mean_nnd, get_max_nnd, canvas_element], 
    "Dispersão de Propágulos - Mortalidade Dependente de Densidade")
server.port = 8521





