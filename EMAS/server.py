from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from EMAS.EmasModel import EmasModel
from EMAS.IslandBorderAgent import IslandBorderAgent
from EMAS.constants import HEIGHT, WIDTH, HEIGHT_RESOLUTION, WIDTH_RESOLUTION


def EMAS_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is IslandBorderAgent:
        portrayal["Color"] = ["#802000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(EMAS_model_portrayal, HEIGHT, WIDTH, HEIGHT_RESOLUTION, WIDTH_RESOLUTION)

chart_element = ChartModule(
    [{"Label": "Hawks", "Color": "#AA0000"}, {"Label": "Doves", "Color": "#666666"}]
)

model_params = {
    "moore": UserSettableParameter("checkbox", "Move in all directions", True),
    "columns": UserSettableParameter(
        "slider", "Columns", 3, 1, 10
    ),
    "rows": UserSettableParameter(
        "slider", "Rows", 3, 1, 10
    ),
    "migration_level": UserSettableParameter(
        "slider", "Energy level to allow migration", 8, 1, 10, 0.01
    ),
    "death_level": UserSettableParameter(
        "slider", "Energy level to die", 0, 0, 10, 0.01
    ),
    "energy_redistribution_radius": UserSettableParameter(
        "slider", "Energy redistribution radius", 4, 1, 20
    ),
    "init_energy": UserSettableParameter(
        "slider", "Energy agent starts with", 5, 1, 10, 0.1
    )
}

server = ModularServer(
    EmasModel, [canvas_element, chart_element], "EMAS Model", model_params
)
server.port = 8521
