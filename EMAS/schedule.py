from mesa.time import RandomActivation


class RandomActivationByBreed(RandomActivation):
    def __init__(self, model, ):
        super().__init__(model)
        self.agents_by_breed = dict()

    def add(self, agent):
        self._agents[agent.unique_id] = agent
        agent_class = agent.genotype

        if agent_class in self.agents_by_breed:
            self.agents_by_breed[agent_class] += 1
        else:
            self.agents_by_breed[agent_class] = 1

    def remove(self, agent):
        del self._agents[agent.unique_id]
        agent_class = agent.genotype
        self.agents_by_breed[agent_class] -= 1
        if self.agents_by_breed[agent_class] == 0:
            del self.agents_by_breed[agent_class]

    def step_and_count(self):
        for agent in self.agent_buffer(shuffled=True):
            agent_class_before = agent.genotype
            agent.step()
            agent_class_after_step = agent.genotype

            if agent_class_before != agent_class_after_step:
                self.agents_by_breed[agent_class_before] -= 1
                self.agents_by_breed[agent_class_after_step] += 1

        self.steps += 1
        self.time += 1

    def get_breed_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        if breed_class not in self.agents_by_breed:
            return 0
        else:
            return self.agents_by_breed[breed_class]
