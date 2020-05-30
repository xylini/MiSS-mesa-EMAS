from EMAS.RandomWalker import RandomWalker


class DoveAgent(RandomWalker):

    def __init__(self, unique_id, pos, model, energy: float, dove_met_hawk, dove_met_dove):
        super().__init__(unique_id, pos, model, energy)
        self.dove_met_hawk = dove_met_hawk
        self.dove_met_dove = dove_met_dove

    def step(self):
        print("Performing dove step")
        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])

        for agent in this_cell:
            if agent is not self:
                from EMAS.HawkAgent import HawkAgent
                if isinstance(agent, HawkAgent):
                    self.met_hawk()
                elif isinstance(agent, DoveAgent):
                    self.met_dove()

                agent.met_dove()

        self.migrate()
        self.die()

    def met_hawk(self):
        self.energy += self.dove_met_hawk

    def met_dove(self):
        self.energy += self.dove_met_dove
