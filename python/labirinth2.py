from dataclasses import dataclass
from typing import NamedTuple, Optional
from enum import Enum

@dataclass(frozen=True)
class Walls:
    """Walls of a cell in a labirinth"""
    top: bool
    right: bool
    bottom: bool
    left: bool

@dataclass(frozen=True)
class Coordinates:
    """Coordinates of a cell in a labirinth,
       (0, 0) means top left corner"""
    column: int
    row: int

@dataclass(frozen=True)
class Dimension:
    width: int
    height: int

class Directions(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Labirinth:
    @classmethod
    def Create(cls,
               dimension: Dimension,
               initial: Walls
               ) -> "Labirinth":
        return cls(dimension, [initial] * dimension.width * dimension.height)

    def GetWalls(self,
                 coord: Coordinates
                 ) -> Optional[Walls]:
        """Get walls of a cell specified by coordinates"""
        if(coord.column < 0 or coord.column >= self._dimension.width or coord.row < 0 or coord.row >= self._dimension.height):
            return None
        return self._walls[self._dimension.height * coord.row + coord.column]

    @staticmethod
    def _CoordByIndex(index: int,
                      dimension: Dimension
                      ) -> Coordinates:
        """Return coordinates by index"""
        y = index // dimension.width
        x = index - ( dimension.width * y)
        return Coordinates(column=x, row=y)

    @staticmethod
    def _IndexByCoord(coord: Coordinates,
                      dimension: Dimension
                      ) -> Optional[int]:
        """Return index by coordinates"""
        x = coord.column 
        if x < 0 or x >= dimension.width:
            return None
        y = coord.row
        if y < 0 or y >= dimension.height:
            return None
        return dimension.width * coord.row + coord.column

    def __init__(self,
                 dimension: Dimension,
                 walls: list[Walls]
                 ) -> None:
        self._dimension = dimension
        self._walls = walls


def Go(coord: Coordinates,
       direction: Directions,
       dimension: Dimension
       ) -> Optional[Coordinates]:
    """Get coordinate in specified direction relative specified coordinate"""
    if direction is Directions.UP:
        return Coordinates(coord.column, coord.row - 1) if coord.row > 0 else None
    if direction is Directions.RIGHT:
        return Coordinates(coord.column + 1, coord.row) if coord.column < dimension.width - 1 else None
    if direction is Directions.DOWN:
        return Coordinates(coord.column, coord.row + 1) if coord.row < dimension.height - 1 else None
    if direction is Directions.LEFT:
        return Coordinates(coord.column - 1, coord.row) if coord.column > 0 else None


if __name__ == "__main__":
    samples = ["""
    ╔════╦══════╦══╗
    ╠═══╗║╠═══╦╗║╚╗║
    ║╔═╗╬╠═╦═╣║║╚╚║║
    ║╚╗╠╚╦║║╔═╣╚═╦╝║
    ║║║╝╔═╩╝║╠╝╣╔╝╔╣
    ║║╚═╣╔══╣╔═╝║╩╣║
    ║╚═╗╚╝╣║╝║╝═╩╔╩║
    ╚══╩══╩══╩═════╝
    """,
    """
    ╔═╗
    ╚═╝
    """,
    """
    ╔═╦═╗
    ╠═╬═╣
    ╚═╩═╝
    """,
    """
    ┃┣━━━┳━━━━┳━━┓
    ┃┗┓┏┛┃╻╺━━┛╺┓┃
    ┣┓┃┗┓┗┻━━━┳╸┃┃
    ┃┃┣╸┣━━┳━┓┗━┛┃
    ┃┃┃┏┛┏╸┃╻┣━┳╸┃
    ┃┗━┫╻┣━━┫┗╸┃┏┫
    ┃┏━┫┃┃╺┓┗━┓┃┃┃
    ┃┃┃┃┃┗┓┗━┓┗┻╸┃
    ┗━┫┏┻━━━━┻━━━┛
    """,
    """
    ┏━┳━┓
    ┣━╋━┫
    ┗━┻━┛
    """]
    for sample in samples:
        print(sample)
