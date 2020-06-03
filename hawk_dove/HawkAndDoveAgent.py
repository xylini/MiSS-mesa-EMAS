from random import random
from EMAS.RandomWalker import RandomWalker
from collections import Counter


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
            self_mutation,
            meeting_history_len,
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
        self.self_mutation = self_mutation
        self.meetings_history = []
        self.meeting_history_len = meeting_history_len

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

    def update_meetings(self, who_visited_me):
        if self.meeting_history_len > 0:
            if len(self.meetings_history) == self.meeting_history_len:
                self.meetings_history = self.meetings_history[1:self.meeting_history_len] + [who_visited_me]
            else:
                self.meetings_history = self.meetings_history + [who_visited_me]

    def met_hawk(self):
        self.update_meetings(HawkAndDoveAgent.HAWK)

        if self.genotype is HawkAndDoveAgent.HAWK:
            self.energy += self.hawk_met_hawk
        elif self.genotype is HawkAndDoveAgent.DOVE:
            self.energy += self.dove_met_hawk

        if self.self_mutation:
            self.genotype = self.evolve()

    def met_dove(self):
        self.update_meetings(HawkAndDoveAgent.DOVE)

        if self.genotype is HawkAndDoveAgent.HAWK:
            self.energy += self.hawk_met_dove
        elif self.genotype is HawkAndDoveAgent.DOVE:
            self.energy += self.dove_met_dove

        if self.self_mutation:
            self.genotype = self.evolve()

    def evolve(self, chance_for_random_mutation=0.1):
        most_common_met_genotype, met_counts = Counter(self.meetings_history).most_common(1)[0]

        # Mutation if most of met genotypes are opposite to myself
        if most_common_met_genotype is not self.genotype \
                and met_counts > self.meetings_history.count(self.genotype):
            return most_common_met_genotype

        # Random genotype mutation if whole meeting history is the same as self genotype
        if met_counts == len(self.meetings_history) \
                and most_common_met_genotype is self.genotype \
                and random() < chance_for_random_mutation:
            return ({HawkAndDoveAgent.HAWK, HawkAndDoveAgent.DOVE} - {self.genotype}).pop()

        return self.genotype
