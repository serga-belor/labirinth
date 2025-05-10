from typing import Final, Dict, List, Optional, Set
from enum import Enum, IntEnum
import random


class Walls(IntEnum):
    NONE = 0
    TOP = 0x01
    RIGHT = 0x02
    BOTTOM = 0x04
    LEFT = 0x08
    ALL = TOP | RIGHT| BOTTOM | LEFT

class Cell:
    """Cell of a labirinth."""

    @classmethod
    def Create(cls, top: bool, right: bool, bottom: bool, left: bool) -> "Cell":
        """Create a labirinth cell with specified walls"""
        walls: int = Walls.NONE
        if top:
            walls |= Walls.TOP
        if right:
            walls |= Walls.RIGHT
        if bottom:
            walls |= Walls.BOTTOM
        if left:
            walls |= Walls.LEFT
        return cls(walls)

    def __init__(self, initial: int) -> None:
        """Initialize cell with walls: [top, right, bottom, left]"""
        self._cell = initial & Walls.ALL

    def GetWalls(self) -> int:
        """Get walls of the cell: [top, right, bottom, left]"""
        return self._cell

    def IsEqual(self, rhv: "Cell") -> bool:
        return self._cell == rhv._cell

    def HaveWall(self, wall: Walls)-> bool:
        return (self._cell & wall) == wall



class Labirinth:
    # Coordinate of a cell in a matrix
    # [column, row]
    CoordType = tuple[int, int]

    # candidate to connect with already connected cell
    # [candfidate cell, connected cell]
    _ConnectCandidateType = tuple[int, int]

    class Directions(IntEnum):
        UP = 1
        RIGHT = 2
        DOWN = 3
        LEFT = 4

    @classmethod
    def Create(cls, width: int, height: int, initial: Cell) -> "Labirinth":
        return cls(width, height, [initial] * width * height)

    @classmethod
    def Generate(cls, width: int, height: int) -> "Labirinth":
        """Generate random connected labirinth with specified dimensions"""

        # fill up the list of cells with non-connected cells
        cells: list[Cell] = [Cell.Create(True, True, True, True)] * width * height

        # free cells that do not connect any other cell
        # at the first time all cells are not connected
        free_cells: set[int] = {i for i in range(width * height)}

        # cells that are a candidate to connect with already connected cell
        candidates: list[Labirinth._ConnectCandidateType] = list()

        def _AddFreeNeighboursAsCandidate(cell_idx: int) -> None:
            cell_coord = cls.CoordByIndex(cell_idx, width)
            neighbours = (
                cls.IndexByCoord((cell_coord[0], cell_coord[1]-1), width, height), # top
                cls.IndexByCoord((cell_coord[0]+1, cell_coord[1]), width, height), # right
                cls.IndexByCoord((cell_coord[0], cell_coord[1]+1), width, height), # bottom
                cls.IndexByCoord((cell_coord[0]-1, cell_coord[1]), width, height), # left
            )
            for neighbour_idx in neighbours:
                if neighbour_idx is None:
                    continue
                if neighbour_idx not in free_cells:
                    continue
                candidates.append((neighbour_idx, cell_idx))
                # print("Labirinth.Generate.AddFreeNeighboursAsCandidate: {}, add neighbour: {}".format(
                #     str(cell_coord), str(cls.CoordByIndex(neighbour_idx, width))))

        def _RemoveNeighbourCellsWall(cell_idx1: int, cell_idx2: int) -> None:
            cell_coord1 = cls.CoordByIndex(cell_idx1, width)
            cell_coord2 = cls.CoordByIndex(cell_idx2, width)
            delta_x = cell_coord1[0] - cell_coord2[0]
            delta_y = cell_coord1[1] - cell_coord2[1]
            if delta_x > 1 or delta_x < -1 or delta_y > 1 or delta_y < -1:
                return
            if delta_x != 0 and delta_y != 0:
                return
            cell1 = cells[cell_idx1]
            cell2 = cells[cell_idx2]
            if delta_x == 1:
                # remove left wall in cell1 and right wall in cell2
                cells[cell_idx1] = Cell.Create(cell1.HaveWall(Walls.TOP), cell1.HaveWall(Walls.RIGHT), cell1.HaveWall(Walls.BOTTOM), False)
                cells[cell_idx2] = Cell.Create(cell2.HaveWall(Walls.TOP), False, cell2.HaveWall(Walls.BOTTOM), cell2.HaveWall(Walls.LEFT))
            elif delta_x == -1:
                # remove right wall in cell1 and left wall in cell2
                cells[cell_idx1] = Cell.Create(cell1.HaveWall(Walls.TOP), False, cell1.HaveWall(Walls.BOTTOM), cell1.HaveWall(Walls.LEFT))
                cells[cell_idx2] = Cell.Create(cell2.HaveWall(Walls.TOP), cell2.HaveWall(Walls.RIGHT), cell2.HaveWall(Walls.BOTTOM), False)
            elif delta_y == 1:
                # remove top wall in cell1 and bottom wall in cell2
                cells[cell_idx1] = Cell.Create(False, cell1.HaveWall(Walls.RIGHT), cell1.HaveWall(Walls.BOTTOM), cell1.HaveWall(Walls.LEFT))
                cells[cell_idx2] = Cell.Create(cell2.HaveWall(Walls.TOP), cell2.HaveWall(Walls.RIGHT), False, cell2.HaveWall(Walls.LEFT))
            elif delta_y == -1:
                # remove bottom wall in cell1 and top wall in cell2
                cells[cell_idx1] = Cell.Create(cell1.HaveWall(Walls.TOP), cell1.HaveWall(Walls.RIGHT), False, cell1.HaveWall(Walls.LEFT))
                cells[cell_idx2] = Cell.Create(False, cell2.HaveWall(Walls.RIGHT), cell2.HaveWall(Walls.BOTTOM), cell2.HaveWall(Walls.LEFT))
            # print("Labirinth.Generate.RemoveNeighbourCellsWall: {}, {}; new walls: {}, {}".format(
            #     str(cell_coord1), str(cell_coord2), str(cells[cell_idx1].Walls()), str(cells[cell_idx2].Walls())))


        # - choose first random cell
        # - remove it from free cells set
        # - add its neighbour into the candidates list
        first_idx: int = random.choice(list(free_cells))
        free_cells.remove(first_idx)
        _AddFreeNeighboursAsCandidate(first_idx)
        #print("Labirinth.Generate, first cell: " + str(cls.CoordByIndex(first_idx, width)))

        while len(candidates) > 0:
            # - choose random cell from candidates
            # - remove it from candidates
            # - remove it from free cells set
            # - add its neighbour into the candidates list
            # - remove cell wall

            candidate_to_add = random.choice(candidates)
            candidate_idx = candidate_to_add[0]
            for candidate in candidates:
                if candidate[0] == candidate_idx:
                    candidates.remove(candidate)
            if candidate_idx in free_cells:
                free_cells.remove(candidate_idx)
            _AddFreeNeighboursAsCandidate(candidate_idx)
            _RemoveNeighbourCellsWall(candidate_to_add[0], candidate_to_add[1])
            #print("Labirinth.Generate, chosen candidate cell: " + str(cls.CoordByIndex(candidate_idx, width)))
            #cls(width, height, cells).Print(cls.CoordByIndex(candidate_idx, width))

        return cls(width, height, cells)

    @staticmethod
    def CoordByIndex(index: int, width: int) -> "Labirinth.CoordType":
        """Return coordinates by index"""
        y = index // width
        x = index - ( width * y)
        return (x, y)

    @staticmethod
    def IndexByCoord(coord: "Labirinth.CoordType", width: int, height: int) -> Optional[int]:
        """Return index by coordinates"""
        x = coord[0] 
        if x < 0 or x >= width:
            return None
        y = coord[1]
        if y < 0 or y >= height:
            return None
        return width * coord[1] + coord[0]

    def __init__(self, width: int, height: int, cells: list[Cell]) -> None:
        self._width = width
        self._height = height
        self._cells = cells

    def Dimension(self) -> tuple[int, int]:
        """Get dimension of the labirinth [width, height]"""
        return (self._width, self._height)
    
    def Cells(self) -> tuple[int, ...]:
        """Get list of cells"""
        return tuple(item.GetWalls() for item in self._cells)

    def GetCell(self, coord: CoordType) -> Optional[Cell]:
        """Get a labirinth cell by coordinates"""
        column = coord[0]
        row = coord[1]
        if(column < 0 or column >= self._width or row < 0 or row >= self._height):
            return None
        return self._cells[self._width * row + column]

    def Go(self, direction: Directions, coord: CoordType) -> Optional[Cell]:
        """Get a cell in specified direction of the specified cell if there is no wall in this direction"""
        cell: Final = self.GetCell(coord)
        if not cell:
            return None

        if direction == Labirinth.Directions.UP:
            if cell.HaveWall(Walls.TOP):
                return None
            return self.GetCell((coord[0], coord[1]-1))

        if direction == Labirinth.Directions.RIGHT:
            if cell.HaveWall(Walls.RIGHT):
                return None
            return self.GetCell((coord[0]+1, coord[1]))

        if direction == Labirinth.Directions.DOWN:
            if cell.HaveWall(Walls.BOTTOM):
                return None
            return self.GetCell((coord[0], coord[1]+1))

        if direction == Labirinth.Directions.LEFT:
            if cell.HaveWall(Walls.LEFT):
                return None
            return self.GetCell((coord[0]-1, coord[1]))
        raise ValueError("Unknown direction: {}".format(direction))


def PrintLabirinth(labirinth: Labirinth,
                   active_cell_coord: Optional[Labirinth.CoordType]
                   ) -> str:
    labirinth_dim: Final = labirinth.Dimension()
    labirinth_width: Final = labirinth_dim[0]
    labirinth_height: Final = labirinth_dim[1]
    out = ""
    for y in range(0, labirinth_height):
        line1 = ""
        line2 = ""
        line3 = ""
        for x in range(0, labirinth_width):
            cell_this = labirinth.GetCell((x, y))
            if cell_this is None:
                return f"Labirint is broken, cannot get cell: {x}, {y}"

            cell_up = labirinth.GetCell((x, y - 1))
            cell_right = labirinth.GetCell((x + 1, y))
            cell_down = labirinth.GetCell((x, y + 1))
            cell_left = labirinth.GetCell((x - 1, y))
            width = 4 if cell_right is None else 3
            if cell_up is None:
                line1 += "\u2584" * width
            elif cell_this.HaveWall(Walls.TOP) and cell_up.HaveWall(Walls.BOTTOM):
                line1 += "\u2588" * width
            elif not cell_this.HaveWall(Walls.TOP) and cell_up.HaveWall(Walls.BOTTOM):
                line1 += "\u2580" * width
            elif cell_this.HaveWall(Walls.TOP) and not cell_up.HaveWall(Walls.BOTTOM):
                line1 += "\u2584" * width
            elif cell_left is None:
                line1 += "\u2588\u2504\u2504"
            elif cell_right is None:
                line1 += "\u2504\u2504\u2504\u2588"
            else:
                line1 += "\u2504" * width

            if cell_left is None:
                line2 += "\u2588"
            elif cell_this.HaveWall(Walls.LEFT) and cell_left.HaveWall(Walls.RIGHT):
                line2 += "\u2588"
            elif not cell_this.HaveWall(Walls.LEFT) and cell_left.HaveWall(Walls.RIGHT):
                line2 += "\u258c"
            elif cell_this.HaveWall(Walls.LEFT) and not cell_left.HaveWall(Walls.RIGHT):
                line2 += "\u2590"
            else:
                line2 += "\u2506"

            if active_cell_coord and active_cell_coord[0] == x and active_cell_coord[1] == y:
                line2 += "**"
            else:
                line2 += "  "

            if not cell_right:
                line2 += "\u2588"

            if cell_down is None:
                line3 += "\u2580" * width

        out += line1 + "\n"
        out += line2 + "\n"
        if line3:
            out += line3 + "\n"
    return out


if __name__ == "__main__":
    # Labirinth(
    #     2, 2,
    #     [
    #         Cell.Create(True, True, True, True), Cell.Create(True, True, True, True),
    #         Cell.Create(True, True, True, True), Cell.Create(True, True, True, True)
    #     ]
    # ).Print(None)
    # Labirinth(
    #     2, 2,
    #     [
    #         Cell.Create(True, True, False, True), Cell.Create(True, True, True, True),
    #         Cell.Create(False, False, True, True), Cell.Create(True, True, True, False)
    #     ]
    # ).Print(None)
    PrintLabirinth(Labirinth(
        2, 2,
        [
            Cell.Create(True, False, True, True), Cell.Create(True, True, False, False),
            Cell.Create(True, False, True, True), Cell.Create(False, True, True, False)
        ]
    ), None)
    # Labirinth.Generate(30, 10).Print(None)
