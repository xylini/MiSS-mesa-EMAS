from collections import defaultdict

from mesa.time import RandomActivation


class RandomActivationByGenotype(RandomActivation):
    def __init__(self, model, ):
        super().__init__(model)
        self.agents_by_genotype = defaultdict(int)

    def add(self, agent):
        self._agents[agent.unique_id] = agent
        agent_class = agent.genotype

        self.agents_by_genotype[agent_class] += 1

    def remove(self, agent):
        del self._agents[agent.unique_id]
        agent_class = agent.genotype
        self.agents_by_genotype[agent_class] -= 1

    def step_and_count(self):
        for agent in self.agent_buffer(shuffled=True):
            agent_class_before = agent.genotype
            agent.step()
            agent_class_after_step = agent.genotype

            if agent_class_before != agent_class_after_step:
                print(agent.unique_id, agent_class_before, agent_class_after_step)
                self.agents_by_genotype[agent_class_before] -= 1
                self.agents_by_genotype[agent_class_after_step] += 1

        self.steps += 1
        self.time += 1

    def get_genotype_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        if breed_class not in self.agents_by_genotype:
            return 0
        else:
            return self.agents_by_genotype[breed_class]
