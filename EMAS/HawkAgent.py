import random

from EMAS.random_walk import RandomWalker


class HawkAgent(RandomWalker):

    def __init__(self, unique_id, pos, model, energy: float, hawk_met_hawk, hawk_met_dove):
        super().__init__(unique_id, pos, model, energy)
        self.hawk_met_hawk = hawk_met_hawk
        self.hawk_met_dove = hawk_met_dove

    def step(self):
        print("Performing hawk step")
        self.migrate()
        self.random_move()
        this_cell = self.model.grid.get_cell_list_contents([self.pos])

        for agent in this_cell:
            if agent is not self:
                from EMAS.DoveAgent import DoveAgent
                if isinstance(agent, HawkAgent):
                    self.met_hawk()
                elif isinstance(agent, DoveAgent):
                    self.met_dove()

                agent.met_hawk()

    def met_hawk(self):
        self.energy += self.hawk_met_hawk

    def met_dove(self):
        self.energy += self.hawk_met_dove
