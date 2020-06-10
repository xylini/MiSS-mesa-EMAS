from typing import List, Tuple, Set
from mesa import Model
from mesa.space import MultiGrid, Coordinate
from EMAS.EmasAgent import EmasAgent
from EMAS.IslandBorderAgent import IslandBorderAgent
from EMAS.constants import HEIGHT, WIDTH


class EmasModel(Model):
    description = (
        "A model for simulating using EMAS model"
    )

    def __init__(
            self,
            height=HEIGHT,
            width=WIDTH,
            columns=2,
            rows=2,
            death_level=0,
            migration_level=10,
            init_energy=100,
            moore=True,
            reproduction_level=7,
            parent_part_to_child=30,
            base_child_energy=5,
            energy_redistribution_radius=4,
            islands=[]
    ):
        super().__init__()
        self.height: int = height
        self.width: int = width
        self.columns: int = columns
        self.rows: int = rows
        self.death_level: float = death_level
        self.migration_level: float = migration_level
        self.moore: bool = moore
        self.reproduction_level: float = reproduction_level
        self.parent_part_to_child: float = parent_part_to_child
        self.base_child_energy: float = base_child_energy
        self.init_energy: float = init_energy
        self.energy_redistribution_radius: int = energy_redistribution_radius
        self.islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = islands
        self.grid = MultiGrid(self.height, self.width, torus=True)

        borders_x_indexes = sorted([int(self.width * part / columns) for part in range(1, self.columns)])
        columns_points: Set[Tuple[int, int]] = {(x, y) for x in borders_x_indexes for y in range(self.height)}

        borders_y_indexes = sorted([int(self.height * part / rows) for part in range(1, self.rows)])
        rows_points: Set[Tuple[int, int]] = {(x, y) for x in range(self.width) for y in borders_y_indexes}

        for border_cords in columns_points | rows_points:
            border = IslandBorderAgent(self.next_id(), border_cords, self)
            self.grid.place_agent(border, border_cords)

        islands_x_corners = [-1] + borders_x_indexes + [self.width]
        islands_y_corners = [-1] + borders_y_indexes + [self.height]

        # left lower and right upper corner
        self.islands = [
            ((x, y), (islands_x_corners[x_u + 1], islands_y_corners[y_u + 1]))
            for x_u, x in enumerate(islands_x_corners) if x != self.width
            for y_u, y in enumerate(islands_y_corners) if y != self.height
        ]

    def get_neighborhood(self, pos: Coordinate, include_center=False, radius=1, moore=True):
        next_moves = self.grid.get_neighborhood(pos, moore, include_center, radius)
        island = self.get_island(pos)
        return self._filter_coors_in_island(island, next_moves)

    def redistribute_energy(self, pos: Coordinate, energy: float, include_center=False, radius=10):
        neighbours = self.grid.get_neighbors(pos, self.moore, include_center, radius)
        island = self.get_island(pos)
        close_neighbours = list(filter(lambda n: self._is_in_island(island, n.pos), neighbours))
        emas_neighbours = list(filter(lambda a: isinstance(a, EmasAgent), close_neighbours))
        if emas_neighbours:
            energy_delta = energy / len(emas_neighbours)
            for neighbour in emas_neighbours:
                neighbour.energy += energy_delta

    def get_island(self, pos: Coordinate):
        return list(filter(lambda coors: coors[0][0] < pos[0] < coors[1][0] and coors[0][1] < pos[1] < coors[1][1],
                           self.islands)).pop()

    def _filter_coors_in_island(self, island: Tuple[Tuple[int, int], Tuple[int, int]],
                                positions: List[Tuple[int, int]]):
        return list(filter(lambda move: island[0][0] < move[0] < island[1][0] and island[0][1] < move[1] <
                                        island[1][1], positions))

    def _is_in_island(self, island, pos):
        print(str(island) + "  " + str(pos))
        return island[0][0] < pos[0] < island[1][0] and island[0][1] < pos[1] < island[1][1]

    def _filter_for_emas_agents(self, agents):
        return filter(lambda a: isinstance(a, EmasAgent), agents)

    def get_closest_neighbour_on_island(self, pos: Coordinate):
        island = self.get_island(pos)

        taxi_radius = abs(island[0][0] - island[1][0]) + abs(island[0][1] - island[1][1])

        # moore=False -> find neighbourhood using taxi metric
        neighbours = self.grid.get_neighbors(pos, False, include_center=False, radius=taxi_radius)
        island_neighbours = [
            agent for agent in neighbours if self._is_in_island(island, agent.pos) and isinstance(agent, EmasAgent)
        ]

        closest_neighbour = None
        closest_distance = taxi_radius
        for agent in island_neighbours:
            if self.taxi_distance(pos, agent.pos) < closest_distance:
                closest_distance = self.taxi_distance(pos, agent.pos)
                closest_neighbour = agent

        return closest_neighbour

    def taxi_distance(self, pos_a: Coordinate, pos_b: Coordinate):
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])
