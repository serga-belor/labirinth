from typing import Dict, List, Optional, Set
from enum import Enum, IntEnum
import random


class Walls(IntEnum):
    NONE = 0
    TOP = 0x1000
    RIGHT = 0x0100
    BOTTOM = 0x0010
    LEFT = 0x0001
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
        # candidate to connect with already connected cell
        # [candfidate cell, connected cell]
        ConnectCandidateType = tuple[int, int]

        # fill up the list of cells with non-connected cells
        cells: list[Cell] = [Cell.Create(True, True, True, True)] * width * height

        # free cells that do not connect any other cell
        # at the first time all cells are not connected
        free_cells: set[int] = {i for i in range(width * height)}

        # cells that are a candidate to connect with already connected cell
        candidates: list[ConnectCandidateType] = list()

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
                cells[cell_idx1] = Cell.Create(cell1.HaveWall()[0], cell1[1], cell1[2], False)
                cells[cell_idx2] = Cell.Create(cell2[0], False, cell2[2], cell2[3])
            elif delta_x == -1:
                # remove right wall in cell1 and left wall in cell2
                cells[cell_idx1] = Cell.Create(cell1[0], False, cell1[2], cell1[3])
                cells[cell_idx2] = Cell.Create(cell2[0], cell2[1], cell2[2], False)
            elif delta_y == 1:
                # remove top wall in cell1 and bottom wall in cell2
                cells[cell_idx1] = Cell.Create(False, cell1[1], cell1[2], cell1[3])
                cells[cell_idx2] = Cell.Create(cell2[0], cell2[1], False, cell2[3])
            elif delta_y == -1:
                # remove bottom wall in cell1 and top wall in cell2
                cells[cell_idx1] = Cell.Create(cell1[0], cell1[1], False, cell1[3])
                cells[cell_idx2] = Cell.Create(False, cell2[1], cell2[2], cell2[3])
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

            candidate_to_add: ConnectCandidateType = random.choice(candidates)
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

    def GetCell(self, coord: CoordType) -> Optional[Cell]:
        """Get a labirinth cell by coordinates"""
        column = coord[0]
        row = coord[1]
        if(column < 0 or column >= self._width or row < 0 or row >= self._height):
            return None
        return self._cells[self._width * row + column]

    def Go(self, direction: Directions, coord: CoordType) -> Optional[Cell]:
        """Get a cell in specified direction of the specified cell if there is no wall in this direction"""
        cell = self.GetCell(coord)
        if not cell:
            return None
        walls = cell.Walls()
        if direction == Labirinth.Directions.UP:
            if walls[0]:
                return None
            return self.GetCell((coord[0], coord[1]-1))
        if direction == Labirinth.Directions.RIGHT:
            if walls[1]:
                return None
            return self.GetCell((coord[0]+1, coord[1]))
        if direction == Labirinth.Directions.DOWN:
            if walls[2]:
                return None
            return self.GetCell((coord[0], coord[1]+1))
        if direction == Labirinth.Directions.LEFT:
            if walls[3]:
                return None
            return self.GetCell((coord[0]-1, coord[1]))
        raise ValueError("Unknown direction: {}".format(direction))


    def Print(self, active_cell: Optional[CoordType]) -> None:
        for y in range(0, self._height):
            line1 = ""
            line2 = ""
            line3 = ""
            for x in range(0, self._width):
                walls_this = self._cells[self._width * y + x].Walls()
                walls_up = self._cells[self._width * (y-1) + x].Walls() if y > 0 else None
                walls_right = self._cells[self._width * y + x +1].Walls() if x < self._width - 1 else None
                walls_down = self._cells[self._width * (y+1) + x].Walls() if y < self._height - 1 else None
                walls_left = self._cells[self._width * y + x -1].Walls() if x > 0 else None
                width = 4 if walls_right is None else 3
                if walls_up is None:
                    line1 += "\u2584" * width
                elif walls_this[0] and walls_up[2]:
                    line1 += "\u2588" * width
                elif not walls_this[0] and walls_up[2]:
                    line1 += "\u2580" * width
                elif walls_this[0] and not walls_up[2]:
                    line1 += "\u2584" * width
                elif walls_left is None:
                    line1 += "\u2588\u2504\u2504"
                elif walls_right is None:
                    line1 += "\u2504\u2504\u2504\u2588"
                else:
                    line1 += "\u2504" * width

                if walls_left is None:
                    line2 += "\u2588"
                elif walls_this[3] and walls_left[1]:
                    line2 += "\u2588"
                elif not walls_this[3] and walls_left[1]:
                    line2 += "\u258c"
                elif walls_this[3] and not walls_left[1]:
                    line2 += "\u2590"
                else:
                    line2 += "\u2506"

                if active_cell and active_cell[0] == x and active_cell[1] == y:
                    line2 += "**"
                else:
                    line2 += "  "

                if not walls_right:
                    line2 += "\u2588"

                if walls_down is None:
                    line3 += "\u2580" * width

            print(line1)
            print(line2)
            if line3:
                print(line3)


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
    Labirinth(
        2, 2,
        [
            Cell.Create(True, False, True, True), Cell.Create(True, True, False, False),
            Cell.Create(True, False, True, True), Cell.Create(False, True, True, False)
        ]
    ).Print(None)
    # Labirinth.Generate(30, 10).Print(None)
