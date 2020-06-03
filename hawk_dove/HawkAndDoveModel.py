import random
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from EMAS.EmasModel import EmasModel
from hawk_dove.HawkAndDoveAgent import HawkAndDoveAgent


class HawkAndDoveModel(EmasModel):
    def __init__(
            self,
            columns,
            rows,
            death_level,
            migration_level,
            reproduction_level,
            parent_part_to_child,
            base_child_energy,
            init_energy,
            moore,
            self_mutation,
            meeting_history_len,
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
            reproduction_level=reproduction_level,
            parent_part_to_child=parent_part_to_child,
            base_child_energy=base_child_energy,
            energy_redistribution_radius=energy_redistribution_radius
        )

        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            {
                "Doves": lambda model: [agent.genotype for agent in model.schedule.agents].count(
                    HawkAndDoveAgent.DOVE),
                "Hawks": lambda model: [agent.genotype for agent in model.schedule.agents].count(
                    HawkAndDoveAgent.HAWK),
            }
        )

        for island in self.islands:
            for _ in range(hawk_per_island):
                try:
                    x = self.random.randrange(island[0][0] + 1, island[1][0] - 1)
                    y = self.random.randrange(island[0][1] + 1, island[1][1] - 1)
                except ValueError:
                    x = island[0][0] + 1
                    y = island[0][1] + 1
                energy = self.init_energy
                hawk = HawkAndDoveAgent(
                    self.next_id(),
                    (x, y),
                    self,
                    migration_level,
                    death_level,
                    energy,
                    self_mutation,
                    meeting_history_len,
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
                energy = self.init_energy
                dove = HawkAndDoveAgent(
                    self.next_id(),
                    (x, y),
                    self,
                    migration_level,
                    death_level,
                    energy,
                    self_mutation,
                    meeting_history_len,
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
        self.schedule.step()
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
        return x, y
