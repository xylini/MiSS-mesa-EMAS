from mesa import Model
from mesa.space import MultiGrid


class EmasModel(Model):
    height = 20
    width = 20

    columns = 1
    rows = 1

    death_level = 0
    migration_level = 0
    energy_redistribution_radius = 4

    description = (
        "A model for simulating using EMAS model"
    )

    def __init__(
        self,
        height=20,
        width=20,
        columns=1,
        rows=1,
        death_level=0,
        migration_level=0,
    ):
        super().__init__()
        self.height = height
        self.width = width
        self.columns = columns
        self.rows = rows
        self.death_level = death_level
        self.migration_level = migration_level

        self.grid = MultiGrid(self.height, self.width, torus=True)

        #TODO: remember to set max volumns and rows
        columns_points = [(x, y) for x in range(self.columns-1, self.width, int(width/columns)) for y in range(height)]
