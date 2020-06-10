from mesa import Agent
from mesa.space import Coordinate


class EmasAgent(Agent):
    """
    Class implementing basic EMAS agent's behaviour.
    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    def __init__(self, unique_id, model, migration_level, death_level, energy, genotype):
        super().__init__(unique_id, model)
        self.energy = energy
        self.death_level = death_level
        self.migration_level = migration_level
        self.genotype = genotype

    def step(self):
        self.reproduce()
        self.migrate()
        self.die()

    def die(self) -> bool:
        if self.energy <= self.death_level:
            position = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            if self.energy > 0:
                self.model.redistribute_energy(position, self.energy, radius=self.model.energy_redistribution_radius)
            return False
        return True

    def migrate(self) -> bool:
        if self.energy > self.migration_level:
            self.model.grid.move_agent(self, self.migration_destination())
            return True
        return False

    def reproduce(self):
        raise Exception("Reproduce genotype strategy not implemented!")

    def generate_new_genotype(self, other_parent):
        raise Exception("Reproduce genotype strategy not implemented!")

    def migration_destination(self) -> Coordinate:
        raise Exception("Migration strategy not implemented!")
