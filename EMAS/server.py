from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from EMAS.EmasModel import EmasModel
from EMAS.IslandBorderAgent import IslandBorderAgent

def EMAS_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # if type(agent) is Sheep:
    #     portrayal["Shape"] = "wolf_sheep/resources/sheep.png"
    #     # https://icons8.com/web-app/433/sheep
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 1
    #
    # elif type(agent) is Wolf:
    #     portrayal["Shape"] = "wolf_sheep/resources/wolf.png"
    #     # https://icons8.com/web-app/36821/German-Shepherd
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 2
    #     portrayal["text"] = round(agent.energy, 1)
    #     portrayal["text_color"] = "White"

    if type(agent) is IslandBorderAgent:
        portrayal["Color"] = ["#802000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(EMAS_model_portrayal, 20, 20, 500, 500)
# canvas_element_2 = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
# chart_element = ChartModule(
#     [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
# )

model_params = {
    "moore": UserSettableParameter("checkbox", "Move in all directions", True),
    "columns": UserSettableParameter(
        "slider", "Columns", 1, 1, 10
    ),
    "rows": UserSettableParameter(
        "slider", "Rows", 1, 1, 10
    ),
    "migration_level": UserSettableParameter(
        "slider", "Energy level to allow migration", 5, 1, 10, 0.01
    ),
    "death_level": UserSettableParameter(
        "slider", "Energy level to die", 1, 1, 10, 0.01
    ),
    "energy_redistribution_radius": UserSettableParameter(
        "slider", "Energy redistribution radius", 4, 1, 20
    ),
    "init_energy": UserSettableParameter(
        "slider", "Energy agent starts with", 5, 1, 10, 0.1
    )
}

server = ModularServer(
    EmasModel, [canvas_element], "EMAS Model", model_params
)
server.port = 8521
