from mesa.time import RandomActivation

from EMAS.DoveAgent import DoveAgent
from EMAS.EmasModel import EmasModel
from EMAS.HawkAgent import HawkAgent


class HawkModel(EmasModel):
    def __init__(
            self,
            columns,
            rows,
            death_level,
            migration_level,
            init_energy,
            moore,
            energy_redistribution_radius,
            hawk_per_island,
            dove_per_island,
            hawk_met_dove,
            hawk_met_hawk,
            dove_met_hawk,
            dove_met_dove
    ):
        super().__init__(
            columns=columns,
            rows=rows,
            death_level=death_level,
            migration_level=migration_level,
            init_energy=init_energy,
            moore=moore,
            energy_redistribution_radius=energy_redistribution_radius
        )
        print("Initializing hawk and dove")
        self.schedule = RandomActivation(self)
        for island in self.islands:
            for _ in range(hawk_per_island):
                try:
                    x = self.random.randrange(island[0][0] + 1, island[1][0] - 1)
                    y = self.random.randrange(island[0][1] + 1, island[1][1] - 1)
                except ValueError:
                    x = island[0][0] + 1
                    y = island[0][1] + 1
                print("Creating hawk at: x=" + str(x) + " y=" + str(y))
                energy = self.init_energy
                hawk = HawkAgent(self.next_id(), (x, y), self, energy, hawk_met_hawk, hawk_met_dove)
                self.grid.place_agent(hawk, (x, y))
                self.schedule.add(hawk)

            for _ in range(dove_per_island):
                try:
                    x = self.random.randrange(island[0][0] + 1, island[1][0] - 1)
                    y = self.random.randrange(island[0][1] + 1, island[1][1] - 1)
                except ValueError:
                    x = island[0][0] + 1
                    y = island[0][1] + 1
                print("Creating dove at: x=" + str(x) + " y=" + str(y))
                energy = self.init_energy
                dove = DoveAgent(self.next_id(), (x, y), self, energy, dove_met_hawk, dove_met_dove)
                self.grid.place_agent(dove, (x, y))
                self.schedule.add(dove)

    def step(self):
        self.schedule.step()
