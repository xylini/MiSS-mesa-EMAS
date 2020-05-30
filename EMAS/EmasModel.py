from typing import List, Tuple, Set, Union, Optional

from mesa import Model, Agent
from mesa.space import MultiGrid, Coordinate

from EMAS.EmasAgent import EmasAgent
from EMAS.IslandBorderAgent import IslandBorderAgent


class EmasModel(Model):
    # death_level: float = 0
    # migration_level: float = 0
    # energy_redistribution_radius: int = 4
    islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    # init_energy: float = 10
    # moore: bool = True

    description = (
        "A model for simulating using EMAS model"
    )

    def __init__(
            self,
            height=20,
            width=20,
            columns=2,
            rows=2,
            death_level=0,
            migration_level=0,
            init_energy=100,
            moore=True,
            energy_redistribution_radius=4,
            islands=[]
    ):
        super().__init__()
        print("Executing emas model contructor")
        self.height: int = height
        self.width: int = width
        self.columns: int = columns
        self.rows: int = rows
        self.death_level: float = death_level
        self.migration_level: float = migration_level
        self.moore: bool = moore
        self.init_energy: float = init_energy
        self.energy_redistribution_radius: int = energy_redistribution_radius
        self.islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = islands
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # TODO: remember to set max volumns and rows
        borders_x_indexes = sorted([int(self.width * part / columns) for part in range(1, self.columns)])
        columns_points: Set[Tuple[int, int]] = {(x, y) for x in borders_x_indexes for y in range(self.height)}

        borders_y_indexes = sorted([int(self.height * part / rows) for part in range(1, self.rows)])
        rows_points: Set[Tuple[int, int]] = {(x, y) for x in range(self.width) for y in borders_y_indexes}

        for border_cords in columns_points | rows_points:
            border = IslandBorderAgent(self.next_id(), border_cords, self)
            self.grid.place_agent(border, border_cords)

        islands_x_corners = [-1] + borders_x_indexes + [self.width]
        islands_y_corners = [-1] + borders_y_indexes + [self.height]

        # left upper and right lower corner
        self.islands = [
            ((x, y), (islands_x_corners[x_u + 1], islands_y_corners[y_u + 1]))
            for x_u, x in enumerate(islands_x_corners) if x != self.width
            for y_u, y in enumerate(islands_y_corners) if y != self.height
        ]
        print(self.islands)

    def get_neighborhood(self, pos: Coordinate, include_center=False, radius=1):
        next_moves = self.grid.get_neighborhood(pos, self.moore, include_center, radius)
        island = self.__get_island(pos)
        return self.__filter_coors_in_island(island, next_moves)

    def redistribute_energy(self, pos: Coordinate, energy: float, include_center=False, radius=100):
        print("REDISTRIBUTING FOR RADIUS : " + str(radius))
        neighbours = self.grid.get_neighbors(pos, self.moore, include_center, radius)
        island = self.__get_island(pos)
        print("DISCOVERED NEIGHBOURS: "+ str(neighbours))
        close_neighbours = list(filter(lambda n: self.is_in_island(island, n.pos), neighbours))
        print("DISCOVERED ISLAND NEIGHBOURS: "+ str(close_neighbours))
        emas_neighbours = list(filter(lambda a: isinstance(a, EmasAgent), close_neighbours))
        print("DISCOVERED EMAS ISLAND NEIGHBOURS: "+ str(emas_neighbours))

        energy_delta = energy/len(emas_neighbours)
        for neighbour in emas_neighbours:
            neighbour.energy += energy_delta
            print("Giving " + str(energy_delta) + " to "+str(neighbour.pos))


    def __get_island(self, pos: Coordinate):
        print("Getting island for " + str(pos))
        return list(filter(lambda coors: coors[0][0] < pos[0] < coors[1][0] and coors[0][1] < pos[1] < coors[1][1],
                           self.islands)).pop()

    def __filter_coors_in_island(self, island: Tuple[Tuple[int, int], Tuple[int, int]],
                                 positions: List[Tuple[int, int]]):
        return list(filter(lambda move: island[0][0] < move[0] < island[1][0] and island[0][1] < move[1] <
                                        island[1][1], positions))

    def is_in_island(self, island, pos):
        return island[0][0] < pos[0] < island[1][0] and island[0][1] < pos[1] < island[1][1]