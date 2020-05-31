import random

from mesa.datacollection import DataCollector
from EMAS.EmasModel import EmasModel
from hawk_dove.HawkAndDoveAgent import HawkAndDoveAgent
from EMAS.schedule import RandomActivationByGenotype


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

        self.schedule = RandomActivationByGenotype(self)

        self.datacollector = DataCollector(
            {
                "Doves": lambda m: m.schedule.get_breed_count(HawkAndDoveAgent.DOVE),
                "Hawks": lambda m: m.schedule.get_breed_count(HawkAndDoveAgent.HAWK),
            }
        )

        print("Initializing hawk and dove")
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
                hawk = HawkAndDoveAgent(
                    self.next_id(),
                    (x, y), self,
                    energy,
                    hawk_met_hawk,
                    hawk_met_dove,
                    dove_met_hawk,
                    dove_met_dove,
                    HawkAndDoveAgent.HAWK
                )
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
                dove = HawkAndDoveAgent(
                    self.next_id(),
                    (x, y), self,
                    energy,
                    hawk_met_hawk,
                    hawk_met_dove,
                    dove_met_hawk,
                    dove_met_dove,
                    HawkAndDoveAgent.DOVE
                )

                self.grid.place_agent(dove, (x, y))
                self.schedule.add(dove)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step_and_count()
        self.datacollector.collect(self)

    def generate_migration_destination(self, old_pos):
        old_island = self.get_island(old_pos)
        new_islands = set(self.islands) - {old_island}
        if len(new_islands) > 0:
            new_island = random.choice(list(new_islands))
        else:
            new_island = old_island
        x = self.random.randrange(new_island[0][0] + 1, new_island[1][0] - 1)
        y = self.random.randrange(new_island[0][1] + 1, new_island[1][1] - 1)
        return (x, y)