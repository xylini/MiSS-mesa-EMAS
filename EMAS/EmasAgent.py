from mesa import Agent

from EMAS.EmasModel import EmasModel


class EmasAgent(Agent):
    """
    Class implementing basic EMAS agent's behaviour.
    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    energy_required = -5

    energy = None

    def __init__(self, unique_id, model: EmasModel, energy=None):
        super().__init__(unique_id, model)
        self.energy = energy

    def died(self) -> bool:
        if self.energy < EmasAgent.energy_required:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.model.redistribute_energy(self.pos, self.energy)
            return False
        return True

    def reproduce(self):
        raise Exception("Reproduce strategy not implemented!")
