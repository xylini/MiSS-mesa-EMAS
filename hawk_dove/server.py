from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from EMAS.IslandBorderAgent import IslandBorderAgent
from EMAS.constants import HEIGHT, WIDTH, HEIGHT_RESOLUTION, WIDTH_RESOLUTION
from hawk_dove.HawkAndDoveAgent import HawkAndDoveAgent
from hawk_dove.HawkAndDoveModel import HawkAndDoveModel


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
        portrayal["Color"] = "#AA0000"
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.8
        portrayal["Layer"] = 1
        portrayal["text_color"] = "black"
        portrayal["text"] = 'e: %.1f' % agent.energy

    elif agent.genotype is HawkAndDoveAgent.DOVE:
        portrayal["Color"] = "#666666"
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        portrayal["text_color"] = "black"
        portrayal["text"] = 'e: %.1f' % agent.energy

    return portrayal


canvas_element = CanvasGrid(EMAS_model_portrayal, HEIGHT, WIDTH, HEIGHT_RESOLUTION, WIDTH_RESOLUTION)

chart_element = ChartModule(
    [{"Label": "Hawks", "Color": "#AA0000"}, {"Label": "Doves", "Color": "#666666"}]
)

model_params = {
    "moore": UserSettableParameter("checkbox", "Move in all directions", True),
    "self_mutation": UserSettableParameter("checkbox", "Self mutation", True),
    "hawk_met_dove": UserSettableParameter("number", "Points for Hawk when met Dove", value=1),
    "hawk_met_hawk": UserSettableParameter("number", "Points for Hawk when met Hawk", value=-3),
    "dove_met_dove": UserSettableParameter("number", "Points for Dove when met Dove", value=0.5),
    "dove_met_hawk": UserSettableParameter("number", "Points for Dove when met Hawk", value=-1),
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
    "reproduction_level": UserSettableParameter(
        "slider", "Energy level to reproduce", 7, 0, 10, 0.01
    ),
    "parent_part_to_child": UserSettableParameter(
        "slider", "% of parent energy for child", 30, 0, 100, 0.1
    ),
    "base_child_energy": UserSettableParameter(
        "slider", "Child base energy level", 5, 0, 10, 0.01
    ),
    "energy_redistribution_radius": UserSettableParameter(
        "slider", "Energy redistribution radius", 4, 1, 20
    ),
    "init_energy": UserSettableParameter(
        "slider", "Energy agent starts with", 5, 1, 10, 0.1
    ),
    "meeting_history_len": UserSettableParameter(
        "slider", "How many meetings should be remembered", 5, 0, 20
    ),
    "hawk_per_island": UserSettableParameter(
        "slider", "Hawks per island", 2, 0, 10
    ),
    "dove_per_island": UserSettableParameter(
        "slider", "Doves per island", 2, 0, 10
    )
}

server = ModularServer(
    HawkAndDoveModel, [canvas_element, chart_element], "EMAS Model", model_params
)
server.port = 8521
