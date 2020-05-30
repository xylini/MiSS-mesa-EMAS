from typing import List, Tuple

from mesa import Model
from mesa.space import MultiGrid, Coordinate


class EmasModel(Model):
    height = 20
    width = 20

    columns = 1
    rows = 1

    death_level = 0
    migration_level = 0
    energy_redistribution_radius = 4
    islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

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
    ):
        super().__init__()
        self.height = height
        self.width = width
        self.columns = columns
        self.rows = rows
        self.death_level = death_level
        self.migration_level = migration_level

        self.grid = MultiGrid(self.height, self.width, torus=True)

        # TODO: remember to set max volumns and rows
        columns_points = [(x, y) for x in range(self.columns - 1, self.width, int(width / columns)) for y in
                          range(height)]

    def get_neighborhood(self, pos: Coordinate, moore: bool, include_center=False, radius=1):
        next_moves = self.grid.get_neighborhood(pos, moore, include_center, radius)
        # Assuming (0, 0) is at the top left corner
        island = list(
            filter(lambda coors: coors[0][0] < pos[0] and coors[0][1] < pos < coors[1][0] and coors[1][1] > pos,
                   EmasModel.islands))[0]
        possible_moves = list(filter(lambda move: island[0][0] < move[0] < island[1][0] and island[0][1] < move[1] <
                                                  island[1][1], next_moves))
        return possible_moves
