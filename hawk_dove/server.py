from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from hawk_dove.HawkAndDoveAgent import HawkAndDoveAgent
from hawk_dove.HawkModel import HawkModel
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

    elif agent.genotype is HawkAndDoveAgent.HAWK:
        portrayal["Shape"] = "resources/hawk.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["text"] = 'e: %.1f  id: %s' % (agent.energy, agent.unique_id)

    elif agent.genotype is HawkAndDoveAgent.DOVE:
        portrayal["Shape"] = "resources/dove.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["text"] = 'e: %.1f  id: %s' % (agent.energy, agent.unique_id)

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
    ),
    "hawk_per_island": UserSettableParameter(
        "slider", "Hawks per island", 2, 0, 10
    ),
    "dove_per_island": UserSettableParameter(
        "slider", "Doves per island", 2, 0, 10
    ),
    "hawk_met_dove": UserSettableParameter(
        "slider", "Points when Hawk met Dove", 1, -10, 10, 0.1
    ),
    "hawk_met_hawk": UserSettableParameter(
        "slider", "Points when Hawk met Hawk", -3, -3, 10, 0.1
    ),
    "dove_met_dove": UserSettableParameter(
        "slider", "Points when Dove met Dove", 0, -10, 10, 0.1
    ),
    "dove_met_hawk": UserSettableParameter(
        "slider", "Points when Dove met Hawk", -1, -10, 10, 0.1
    ),
}

server = ModularServer(
    HawkModel, [canvas_element, chart_element], "EMAS Model", model_params
)
server.port = 8521
