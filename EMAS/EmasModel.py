from typing import List, Tuple

from mesa import Model
from mesa.space import MultiGrid, Coordinate

from EMAS.IslandBorderAgent import IslandBorderAgent


class EmasModel(Model):
    height = 20
    width = 20

    columns = 1
    rows = 1

    death_level = 0
    migration_level = 0
    energy_redistribution_radius = 4
    islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    init_energy = 10

    moore = True

    description = (
        "A model for simulating using EMAS model"
    )

    def __init__(
            self,
            height=20,
            width=20,
            columns=1,
            rows=1,
            death_level=0,
            migration_level=0,
            init_energy=100,
            moore=True,
            energy_redistribution_radius=4
    ):
        super().__init__()
        self.height = height
        self.width = width
        self.columns = columns
        self.rows = rows
        self.death_level = death_level
        self.migration_level = migration_level
        self.moore = moore
        self.init_energy = init_energy
        self.energy_redistribution_radius = energy_redistribution_radius

        self.grid = MultiGrid(self.height, self.width, torus=True)

        # TODO: remember to set max volumns and rows
        columns_points = {(int(self.width * part / columns), y) for part in range(1, self.columns) for y in
                          range(self.height)}
        rows_points = {(x, int(self.height * part / rows)) for x in range(self.width) for part in range(1, self.rows)}

        for border_cords in columns_points | rows_points:
            border = IslandBorderAgent(self.next_id(), border_cords, self)
            self.grid.place_agent(border, border_cords)

    def get_neighborhood(self, pos: Coordinate, moore: bool, include_center=False, radius=1):
        next_moves = self.grid.get_neighborhood(pos, moore, include_center, radius)
        # Assuming (0, 0) is at the top left corner
        island = list(
            filter(lambda coors: coors[0][0] < pos[0] and coors[0][1] < pos < coors[1][0] and coors[1][1] > pos,
                   EmasModel.islands))[0]
        possible_moves = list(filter(lambda move: island[0][0] < move[0] < island[1][0] and island[0][1] < move[1] <
                                                  island[1][1], next_moves))
        return possible_moves
