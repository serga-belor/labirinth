// Copyright Sergei Belorusets, 2024

export { Labirinth };
export { SetCurrent };

export type { LabitinthInfo };


import { AppendClassName } from "./utils";


interface LabitinthInfo {
    readonly id: number;
    readonly width: number;
    readonly height: number;
    readonly cells: ReadonlyArray<number>;
    readonly test: string;
    readonly status: string;
}

interface LabirinthParams {
    readonly value: LabitinthInfo;
    readonly OnClick: (idx: number) => void;
}
function Labirinth(params: LabirinthParams
                   ): JSX.Element
{
    const wall_to_class_name: readonly (readonly[CellWalls, string])[] = [
        [CellWalls.top, "wall-top"],
        [CellWalls.right, "wall-right"],
        [CellWalls.bottom, "wall-bottom"],
        [CellWalls.left, "wall-left"]
    ];

    const labirinth =
        <table className="labirinth"><tbody>
            {params.value.cells.reduce((acc: {rows: JSX.Element[], cur_row: JSX.Element[]}, cell, idx) => {
                const border_class_name =
                    wall_to_class_name.reduce((acc, wall_to_class) => {
                        if(HasWall(cell, wall_to_class[0])) {
                            return AppendClassName(acc, [wall_to_class[1]]);
                        } else {
                            return acc;
                        }
                    }, "");

                const status_class_name =
                        IsCurrent(cell)
                            ? "current"
                            : "";

                const td_el =
                    <td className={AppendClassName("labirinth-cell", [border_class_name, status_class_name])}
                        onClick={() => params.OnClick(idx)}
                        key={`cell${idx}`}
                    />;

                if(idx === 0) {
                    // first cell
                    acc.cur_row.push(td_el);

                } else if(idx === params.value.cells.length-1) {
                    // last cell
                    acc.cur_row.push(td_el);
                    acc.rows.push(
                        <tr key={`row${idx}`}>{acc.cur_row}</tr>
                    );
                } else if(idx % params.value.width === 0) {
                    // next row
                    acc.rows.push(
                        <tr key={`row${idx}`}>{acc.cur_row}</tr>
                    );
                    acc.cur_row = [td_el];

                } else {
                    acc.cur_row.push(td_el);
                }
                return acc;
            }, {rows: [], cur_row: []}).rows}
        </tbody></table>;

    return labirinth;
}

const enum CellWalls {
    top = 0x01,
    right = 0x02,
    bottom = 0x04,
    left = 0x08,
}
const enum CellStatus {
    current = 0x10,
}

function HasWall(cell: number,
                 wall: CellWalls
                 ): boolean
{
    return (cell & wall) === wall;
}

function IsCurrent(cell: number): boolean
{
    return (cell & CellStatus.current) === CellStatus.current;
}

function SetCurrent(cell: number,
                    current: boolean
                    ): number
{
    return current
            ? cell | CellStatus.current
            : cell & ~CellStatus.current;
}
