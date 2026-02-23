# Copyright Sergei Belorusets, 2024-2026

from labyrinth import Labyrinth, Cell
from labyrinth import PrintLabyrinth


def Test_Cell():
    cell = Cell.Create(True, False, False, True)
    assert cell.IsEqual( Cell.Create(True, False, False, True) )
    assert not cell.IsEqual( Cell.Create(False, False, False, True) )

def Test_Labyrinth():
    labyrinth = Labyrinth.Create(6, 3, Cell.Create(True, True, True, True))
    dimention = labyrinth.Dimension()
    assert dimention[0] == 6 and dimention[1] == 3
    cell = labyrinth.GetCell((0, 0))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    cell = labyrinth.GetCell((0, 2))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    cell = labyrinth.GetCell((5, 0))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    cell = labyrinth.GetCell((5, 2))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    assert labyrinth.GetCell((6, 3)) is None
    assert labyrinth.GetCell((-1, -1)) is None
    assert labyrinth.GetCell((0, -1)) is None
    assert labyrinth.GetCell((-1, 0)) is None

def Test_Go():
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.UP, (0, 0)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labyrinth.Directions.UP, (1, 1)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.UP, (1, 1)) is not None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.RIGHT, (5, 0)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labyrinth.Directions.RIGHT, (1, 1)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.RIGHT, (1, 1)) is not None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.DOWN, (5, 2)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labyrinth.Directions.DOWN, (1, 1)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.DOWN, (1, 1)) is not None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.LEFT, (0, 0)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labyrinth.Directions.LEFT, (1, 1)) is None
    assert Labyrinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labyrinth.Directions.LEFT, (1, 1)) is not None
    

if __name__ == "__main__":
    PrintLabyrinth(Labyrinth.Generate(5, 5), (3, 2))
    Test_Cell()
    Test_Labyrinth()
    Test_Go()
