from labirinth2 import Walls, Go, Directions, Coordinates, Labirinth


def test_walls():
    cell = Walls(top=True, right=False, bottom=False, left=True)
    assert Walls.IsEqual(
        Walls(True, False, False, True),
        Walls(True, False, False, True) )

    assert not Walls.IsEqual(
        Walls(True, False, False, True),
        Walls(False, False, False, True) )


def test_go():
    assert Coordinates.IsEqual(
        Go((0, 0), Directions.UP, (6, 3)),
        None)
    assert Coordinates.IsEqual(
        Go((1, 1), Directions.UP, (6, 3)),
        Coordinates(1, 0))
    assert Coordinates.IsEqual(
        Go((5, 2), Directions.UP, (6, 3)),
        Coordinates(5, 1))
    assert Coordinates.IsEqual(
        Go((0, 0), Directions.RIGHT, (6, 3)),
        Coordinates(1, 0))
    assert Coordinates.IsEqual(
        Go((1, 1), Directions.RIGHT, (6, 3)),
        Coordinates(2, 1))
    assert Coordinates.IsEqual(
        Go((5, 2), Directions.RIGHT, (6, 3)),
        None)
    assert Coordinates.IsEqual(
        Go((0, 0), Directions.DOWN, (6, 3)),
        Coordinates(0, 1))
    assert Coordinates.IsEqual(
        Go((1, 1), Directions.DOWN, (6, 3)),
        Coordinates(1, 2))
    assert Coordinates.IsEqual(
        Go((5, 2), Directions.DOWN, (6, 3)),
        None)
    assert Coordinates.IsEqual(
        Go((0, 0), Directions.LEFT, (6, 3)),
        None)
    assert Coordinates.IsEqual(
        Go((1, 1), Directions.LEFT, (6, 3)),
        Coordinates(0, 1))
    assert Coordinates.IsEqual(
        Go((5, 2), Directions.LEFT, (6, 3)),
        Coordinates(4, 2))


def test_labirinth():
    labirinth = Labirinth.Create((6, 3), (True, True, True, True))
    assert Walls.IsEqual(
        labirinth.GetWalls((0, 0)),
        (True, True, True, True))
    assert Walls.IsEqual(
        labirinth.GetWalls((6, 0)),
        None)
        