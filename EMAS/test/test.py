import unittest
from typing import List, Tuple


def return_island(pos):
    return list(filter(lambda coors: coors[0][0] < pos[0] < coors[1][0] and coors[0][1] < pos[1] < coors[1][1],
                       TestIslandResolution.islands))[0]


class TestIslandResolution(unittest.TestCase):
    islands: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [((0, 0), (5, 5)), ((5, 0), (10, 5)), ((0, 5), (5, 10)),
                                                              ((5, 5), (10, 10))]

    def test(self):
        self.assertEqual(return_island((1, 1)), TestIslandResolution.islands[0])
        self.assertEqual(return_island((4, 1)), TestIslandResolution.islands[0])
        self.assertEqual(return_island((1, 4)), TestIslandResolution.islands[0])
        self.assertEqual(return_island((6, 1)), TestIslandResolution.islands[1])
        self.assertEqual(return_island((7, 4)), TestIslandResolution.islands[1])
        self.assertEqual(return_island((9, 4)), TestIslandResolution.islands[1])
        with self.assertRaises(IndexError):
            return_island((1, 5))
            return_island((5, 3))
            return_island((5, 5))


if __name__ == '__main__':
    unittest.main()
