from labirinth import Labirinth, Cell
from labirinth import PrintLabirinth


def Test_Cell():
    cell = Cell.Create(True, False, False, True)
    assert cell.IsEqual( Cell.Create(True, False, False, True) )
    assert not cell.IsEqual( Cell.Create(False, False, False, True) )

def Test_Labirinth():
    labirinth = Labirinth.Create(6, 3, Cell.Create(True, True, True, True))
    dimention = labirinth.Dimension()
    assert dimention[0] == 6 and dimention[1] == 3
    cell = labirinth.GetCell((0, 0))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    cell = labirinth.GetCell((0, 2))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    cell = labirinth.GetCell((5, 0))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    cell = labirinth.GetCell((5, 2))
    assert cell.IsEqual(Cell.Create(True, True, True, True))
    assert labirinth.GetCell((6, 3)) is None
    assert labirinth.GetCell((-1, -1)) is None
    assert labirinth.GetCell((0, -1)) is None
    assert labirinth.GetCell((-1, 0)) is None

def Test_Go():
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.UP, (0, 0)) is None
    assert Labirinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labirinth.Directions.UP, (1, 1)) is None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.UP, (1, 1)) is not None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.RIGHT, (5, 0)) is None
    assert Labirinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labirinth.Directions.RIGHT, (1, 1)) is None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.RIGHT, (1, 1)) is not None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.DOWN, (5, 2)) is None
    assert Labirinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labirinth.Directions.DOWN, (1, 1)) is None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.DOWN, (1, 1)) is not None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.LEFT, (0, 0)) is None
    assert Labirinth.Create(6, 3, Cell.Create(True, True, True, True)).Go(Labirinth.Directions.LEFT, (1, 1)) is None
    assert Labirinth.Create(6, 3, Cell.Create(False, False, False, False)).Go(Labirinth.Directions.LEFT, (1, 1)) is not None
    

if __name__ == "__main__":
    PrintLabirinth(Labirinth.Generate(5, 5), (3, 2))
    Test_Cell()
    Test_Labirinth()
    Test_Go()