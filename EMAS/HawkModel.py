from mesa.time import RandomActivation

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
            energy_redistribution_radius
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
        print("Initializing hawk")
        self.schedule = RandomActivation(self)
        for island in self.islands:
            try:
                x = self.random.randrange(island[0][0] + 1, island[1][0] - 1)
                y = self.random.randrange(island[0][1] + 1, island[1][1] - 1)
            except ValueError:
                x = island[0][0] + 1
                y = island[0][1] + 1

            print("Creating hawk at: x=" + str(x) + " y=" + str(y))
            energy = self.init_energy
            hawk = HawkAgent(self.next_id(), (x, y), self, energy=energy)
            self.grid.place_agent(hawk, (x, y))
            self.schedule.add(hawk)
