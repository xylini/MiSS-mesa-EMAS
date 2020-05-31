from random import random
from EMAS.RandomWalker import RandomWalker


class HawkAndDoveAgent(RandomWalker):
    HAWK = 'hawk'
    DOVE = 'dove'

    def __init__(
            self,
            unique_id,
            pos,
            model,
            migration_level,
            death_level,
            energy: float,
            hawk_met_hawk,
            hawk_met_dove,
            dove_met_hawk,
            dove_met_dove,
            genotype
    ):
        super().__init__(unique_id, pos, model, migration_level, death_level, energy, genotype)
        self.hawk_met_hawk = hawk_met_hawk
        self.hawk_met_dove = hawk_met_dove
        self.dove_met_hawk = dove_met_hawk
        self.dove_met_dove = dove_met_dove
        self.genotype = genotype
        self.last_5_meetings = []

    def step(self):
        self.random_move()
        this_cell = self.model.grid.get_cell_list_contents([self.pos])

        for agent in this_cell:
            if agent is not self:
                if agent.genotype is HawkAndDoveAgent.HAWK:
                    self.met_hawk()
                elif agent.genotype is HawkAndDoveAgent.DOVE:
                    self.met_dove()
                if self.genotype is HawkAndDoveAgent.HAWK:
                    agent.met_hawk()
                elif self.genotype is HawkAndDoveAgent.DOVE:
                    agent.met_dove()

        self.migrate()
        self.die()

    def met_hawk(self):
        self.last_5_meetings = self.last_5_meetings[1:5] + [HawkAndDoveAgent.HAWK]
        if self.genotype is HawkAndDoveAgent.HAWK:
            self.energy += self.hawk_met_hawk
        elif self.genotype is HawkAndDoveAgent.DOVE:
            self.energy += self.dove_met_hawk
        self.genotype = self.evolve()

    def met_dove(self):
        self.last_5_meetings = self.last_5_meetings[1:5] + [HawkAndDoveAgent.DOVE]
        if self.genotype is HawkAndDoveAgent.HAWK:
            self.energy += self.hawk_met_dove
        elif self.genotype is HawkAndDoveAgent.DOVE:
            self.energy += self.dove_met_dove
        self.genotype = self.evolve()

    def evolve(self):
        most_commonly_occurring = \
        sorted({(self.last_5_meetings.count(value), value) for value in self.last_5_meetings})[-1]
        if most_commonly_occurring[1] != self.genotype and most_commonly_occurring[0] > (
                self.last_5_meetings + [self.genotype]).count(self.genotype):
            return most_commonly_occurring[1]

        if most_commonly_occurring[0] == len(self.last_5_meetings) and most_commonly_occurring[
            1] == self.genotype and random() < 0.1:
            return ({HawkAndDoveAgent.HAWK, HawkAndDoveAgent.DOVE} - {self.genotype}).pop()
        return self.genotype
