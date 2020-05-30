from mesa import Agent
from mesa.space import Coordinate


class EmasAgent(Agent):
    """
    Class implementing basic EMAS agent's behaviour.
    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    def __init__(self, unique_id, model, migration_level=10, death_level=0, energy=None, genotype=None):
        super().__init__(unique_id, model)
        self.energy = energy
        self.death_level = death_level
        self.migration_level = migration_level
        self.genotype = genotype

    def die(self) -> bool:
        if self.energy < self.death_level:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            if self.energy > 0:
                self.model.redistribute_energy(self.pos, self.energy)
            return False
        return True

    def migrate(self) -> bool:
        if self.energy > self.migration_level:
            print("migrating hawk")
            self.model.grid.move_agent(self, self.migration_destination())
            return True
        return False

    def reproduce(self):
        raise Exception("Reproduce strategy not implemented!")

    def migration_destination(self) -> Coordinate:
        return self.model.generate_migration_destination(self.pos)
