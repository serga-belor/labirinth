// Copyright Sergei Belorusets, 2024-2026

export { Walls, Cell, Labyrinth, printLabyrinth };

enum Walls {
  NONE = 0,
  TOP = 0x01,
  RIGHT = 0x02,
  BOTTOM = 0x04,
  LEFT = 0x08,
  ALL = TOP | RIGHT | BOTTOM | LEFT
}

class Cell {
  private readonly cell: number;

  static create(top: boolean, right: boolean, bottom: boolean, left: boolean): Cell {
    let walls = Walls.NONE;
    if (top) {
      walls |= Walls.TOP;
    }
    if (right) {
      walls |= Walls.RIGHT;
    }
    if (bottom) {
      walls |= Walls.BOTTOM;
    }
    if (left) {
      walls |= Walls.LEFT;
    }
    return new Cell(walls);
  }

  constructor(initial: number) {
    this.cell = initial & Walls.ALL;
  }

  getWalls(): number {
    return this.cell;
  }

  isEqual(rhs: Cell): boolean {
    return this.cell === rhs.cell;
  }

  haveWall(wall: Walls): boolean {
    return (this.cell & wall) === wall;
  }
}

class Labyrinth {
  static readonly Directions = {
    UP: 1,
    RIGHT: 2,
    DOWN: 3,
    LEFT: 4
  } as const;

  static create(width: number, height: number, initial: Cell): Labyrinth {
    return new Labyrinth(
      width,
      height,
      Array.from({ length: width * height }, () => new Cell(initial.getWalls()))
    );
  }

  static generate(width: number, height: number): Labyrinth {
    const cells: Cell[] = Array.from({ length: width * height }, () =>
      Cell.create(true, true, true, true)
    );
    const freeCells = new Set<number>(Array.from({ length: width * height }, (_, i) => i));
    const candidates: Array<[number, number]> = [];

    const addFreeNeighboursAsCandidate = (cellIndex: number): void => {
      const [x, y] = Labyrinth.coordByIndex(cellIndex, width);
      const neighbours = [
        Labyrinth.indexByCoord([x, y - 1], width, height),
        Labyrinth.indexByCoord([x + 1, y], width, height),
        Labyrinth.indexByCoord([x, y + 1], width, height),
        Labyrinth.indexByCoord([x - 1, y], width, height)
      ];

      for (const neighbourIdx of neighbours) {
        if (neighbourIdx === null || !freeCells.has(neighbourIdx)) {
          continue;
        }
        candidates.push([neighbourIdx, cellIndex]);
      }
    };

    const removeNeighbourCellsWall = (cellIdx1: number, cellIdx2: number): void => {
      const [x1, y1] = Labyrinth.coordByIndex(cellIdx1, width);
      const [x2, y2] = Labyrinth.coordByIndex(cellIdx2, width);
      const deltaX = x1 - x2;
      const deltaY = y1 - y2;

      if (Math.abs(deltaX) > 1 || Math.abs(deltaY) > 1) {
        return;
      }
      if (deltaX !== 0 && deltaY !== 0) {
        return;
      }

      const cell1 = cells[cellIdx1];
      const cell2 = cells[cellIdx2];

      if (deltaX === 1) {
        cells[cellIdx1] = Cell.create(
          cell1.haveWall(Walls.TOP),
          cell1.haveWall(Walls.RIGHT),
          cell1.haveWall(Walls.BOTTOM),
          false
        );
        cells[cellIdx2] = Cell.create(
          cell2.haveWall(Walls.TOP),
          false,
          cell2.haveWall(Walls.BOTTOM),
          cell2.haveWall(Walls.LEFT)
        );
      } else if (deltaX === -1) {
        cells[cellIdx1] = Cell.create(
          cell1.haveWall(Walls.TOP),
          false,
          cell1.haveWall(Walls.BOTTOM),
          cell1.haveWall(Walls.LEFT)
        );
        cells[cellIdx2] = Cell.create(
          cell2.haveWall(Walls.TOP),
          cell2.haveWall(Walls.RIGHT),
          cell2.haveWall(Walls.BOTTOM),
          false
        );
      } else if (deltaY === 1) {
        cells[cellIdx1] = Cell.create(
          false,
          cell1.haveWall(Walls.RIGHT),
          cell1.haveWall(Walls.BOTTOM),
          cell1.haveWall(Walls.LEFT)
        );
        cells[cellIdx2] = Cell.create(
          cell2.haveWall(Walls.TOP),
          cell2.haveWall(Walls.RIGHT),
          false,
          cell2.haveWall(Walls.LEFT)
        );
      } else if (deltaY === -1) {
        cells[cellIdx1] = Cell.create(
          cell1.haveWall(Walls.TOP),
          cell1.haveWall(Walls.RIGHT),
          false,
          cell1.haveWall(Walls.LEFT)
        );
        cells[cellIdx2] = Cell.create(
          false,
          cell2.haveWall(Walls.RIGHT),
          cell2.haveWall(Walls.BOTTOM),
          cell2.haveWall(Walls.LEFT)
        );
      }
    };

    const firstIdx = randomChoice(Array.from(freeCells));
    freeCells.delete(firstIdx);
    addFreeNeighboursAsCandidate(firstIdx);

    while (candidates.length > 0) {
      const candidateToAdd = randomChoice(candidates);
      const candidateIdx = candidateToAdd[0];

      for (let i = candidates.length - 1; i >= 0; i -= 1) {
        if (candidates[i][0] === candidateIdx) {
          candidates.splice(i, 1);
        }
      }

      freeCells.delete(candidateIdx);
      addFreeNeighboursAsCandidate(candidateIdx);
      removeNeighbourCellsWall(candidateToAdd[0], candidateToAdd[1]);
    }

    return new Labyrinth(width, height, cells);
  }

  static coordByIndex(index: number, width: number): [number, number] {
    const y = Math.floor(index / width);
    const x = index - width * y;
    return [x, y];
  }

  static indexByCoord(coord: [number, number], width: number, height: number): number | null {
    const [x, y] = coord;
    if (x < 0 || x >= width || y < 0 || y >= height) {
      return null;
    }
    return width * y + x;
  }

  private readonly width: number;
  private readonly height: number;
  private readonly cells: Cell[];

  constructor(width: number, height: number, cells: Cell[]) {
    this.width = width;
    this.height = height;
    this.cells = cells;
  }

  dimension(): [number, number] {
    return [this.width, this.height];
  }

  cellsData(): number[] {
    return this.cells.map((cell) => cell.getWalls());
  }

  getCell(coord: [number, number]): Cell | null {
    const [x, y] = coord;
    if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
      return null;
    }
    return this.cells[this.width * y + x];
  }

  go(direction: number, coord: [number, number]): Cell | null {
    const cell = this.getCell(coord);
    if (!cell) {
      return null;
    }

    if (direction === Labyrinth.Directions.UP) {
      if (cell.haveWall(Walls.TOP)) {
        return null;
      }
      return this.getCell([coord[0], coord[1] - 1]);
    }
    if (direction === Labyrinth.Directions.RIGHT) {
      if (cell.haveWall(Walls.RIGHT)) {
        return null;
      }
      return this.getCell([coord[0] + 1, coord[1]]);
    }
    if (direction === Labyrinth.Directions.DOWN) {
      if (cell.haveWall(Walls.BOTTOM)) {
        return null;
      }
      return this.getCell([coord[0], coord[1] + 1]);
    }
    if (direction === Labyrinth.Directions.LEFT) {
      if (cell.haveWall(Walls.LEFT)) {
        return null;
      }
      return this.getCell([coord[0] - 1, coord[1]]);
    }

    throw new Error(`Unknown direction: ${direction}`);
  }
}

function printLabyrinth(
  labyrinth: Labyrinth,
  activeCellCoord: [number, number] | null
): string {
  const [labyrinthWidth, labyrinthHeight] = labyrinth.dimension();
  let out = "";

  for (let y = 0; y < labyrinthHeight; y += 1) {
    let line1 = "";
    let line2 = "";
    let line3 = "";

    for (let x = 0; x < labyrinthWidth; x += 1) {
      const cellThis = labyrinth.getCell([x, y]);
      if (!cellThis) {
        return `Labyrint is broken, cannot get cell: ${x}, ${y}`;
      }

      const cellUp = labyrinth.getCell([x, y - 1]);
      const cellRight = labyrinth.getCell([x + 1, y]);
      const cellDown = labyrinth.getCell([x, y + 1]);
      const cellLeft = labyrinth.getCell([x - 1, y]);
      const width = cellRight === null ? 4 : 3;

      if (cellUp === null) {
        line1 += "\u2584".repeat(width);
      } else if (cellThis.haveWall(Walls.TOP) && cellUp.haveWall(Walls.BOTTOM)) {
        line1 += "\u2588".repeat(width);
      } else if (!cellThis.haveWall(Walls.TOP) && cellUp.haveWall(Walls.BOTTOM)) {
        line1 += "\u2580".repeat(width);
      } else if (cellThis.haveWall(Walls.TOP) && !cellUp.haveWall(Walls.BOTTOM)) {
        line1 += "\u2584".repeat(width);
      } else if (cellLeft === null) {
        line1 += "\u2588\u2504\u2504";
      } else if (cellRight === null) {
        line1 += "\u2504\u2504\u2504\u2588";
      } else {
        line1 += "\u2504".repeat(width);
      }

      if (cellLeft === null) {
        line2 += "\u2588";
      } else if (cellThis.haveWall(Walls.LEFT) && cellLeft.haveWall(Walls.RIGHT)) {
        line2 += "\u2588";
      } else if (!cellThis.haveWall(Walls.LEFT) && cellLeft.haveWall(Walls.RIGHT)) {
        line2 += "\u258c";
      } else if (cellThis.haveWall(Walls.LEFT) && !cellLeft.haveWall(Walls.RIGHT)) {
        line2 += "\u2590";
      } else {
        line2 += "\u2506";
      }

      if (activeCellCoord && activeCellCoord[0] === x && activeCellCoord[1] === y) {
        line2 += "**";
      } else {
        line2 += "  ";
      }

      if (cellRight === null) {
        line2 += "\u2588";
      }

      if (cellDown === null) {
        line3 += "\u2580".repeat(width);
      }
    }

    out += `${line1}\n`;
    out += `${line2}\n`;
    if (line3) {
      out += `${line3}\n`;
    }
  }

  return out;
}

function randomChoice<T>(items: readonly T[]): T {
  if (items.length === 0) {
    throw new Error("Cannot choose from an empty array.");
  }
  const idx = Math.floor(Math.random() * items.length);
  return items[idx];
}
