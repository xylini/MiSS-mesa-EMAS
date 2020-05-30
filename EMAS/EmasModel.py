from typing import List, Tuple, Set

from mesa import Model
from mesa.space import MultiGrid, Coordinate

from EMAS.IslandBorderAgent import IslandBorderAgent


class EmasModel(Model):
    height: int = 20
    width: int = 20

    columns: int = 1
    rows: int = 1

    death_level: float = 0
    migration_level: float = 0
    energy_redistribution_radius: int = 4
    islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    init_energy: float = 10

    moore: bool = True

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
        self.height: int = height
        self.width: int = width
        self.columns: int = columns
        self.rows: int = rows
        self.death_level: float = death_level
        self.migration_level: float = migration_level
        self.moore: bool = moore
        self.init_energy: float = init_energy
        self.energy_redistribution_radius: int = energy_redistribution_radius

        self.grid = MultiGrid(self.height, self.width, torus=True)

        # TODO: remember to set max volumns and rows
        columns_points: Set[Tuple[int, int]] = {(int(self.width * part / columns), y) for part in range(1, self.columns)
                                                for y in range(self.height)}

        rows_points: Set[Tuple[int, int]] = {(x, int(self.height * part / rows)) for x in range(self.width) for part in
                                             range(1, self.rows)}

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
