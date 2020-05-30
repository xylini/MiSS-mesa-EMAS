from EMAS.EmasAgent import EmasAgent


class RandomWalker(EmasAgent):

    def __init__(self, unique_id, pos, model, energy: float):
        super().__init__(unique_id, model, energy=energy)
        self.pos = pos

    def random_move(self):
        next_moves = self.model.get_neighborhood(self.pos)
        next_move = self.random.choice(next_moves) if next_moves else self.pos
        self.model.grid.move_agent(self, next_move)
