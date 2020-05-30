from mesa import Agent
from mesa.space import Coordinate


class EmasAgent(Agent):
    """
    Class implementing basic EMAS agent's behaviour.
    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    def __init__(self, unique_id, model, migration_level=10, death_level=0, energy=None):
        super().__init__(unique_id, model)
        self.energy = energy
        self.death_level = death_level
        self.migration_level = migration_level

    def died(self) -> bool:
        if self.energy < self.death_level:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.model.redistribute_energy(self.pos, self.energy)
            return False
        return True

    def migrated(self) -> bool:
        if self.energy > self.migration_level:
            self.model.grid._remove_agent(self.pos, self)
            self.model.grid._place_agent(self.migration_destination(), self)
            return True
        return False

    def reproduce(self):
        raise Exception("Reproduce strategy not implemented!")

    def migration_destination(self) -> Coordinate:
        raise Exception("Migration strategy not implemented!")
