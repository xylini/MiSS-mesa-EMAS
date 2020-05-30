from EMAS.EmasModel import EmasModel
from EMAS.HawkAgent import HawkAgent


class HawkModel(EmasModel):

    agent_per_island = 1

    def __init__(self):
        super().__init__()
        for island in self.islands:
            for i in range(HawkModel.agent_per_island):
                x = self.random.randrange(island[0][0]+1, island[1][0]-1)
                y = self.random.randrange(island[0][1]+1, island[1][1]-1)
                energy = self.init_energy
                hawk = HawkAgent(self.next_id(), (x, y), self, energy=energy)
                self.grid.place_agent(hawk, (x, y))
                self.schedule.add(hawk)