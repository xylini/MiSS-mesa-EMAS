from EMAS.random_walk import RandomWalker


class HawkAgent(RandomWalker):

    def __init__(self, unique_id, pos, model, energy: float):
        super().__init__(unique_id, pos, model, energy)

    def step(self):
        print("Performing hawk step")
        self.random_move()
