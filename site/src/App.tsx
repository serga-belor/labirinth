export { App };

import React, { useEffect, useState } from "react";
import axios from "axios";


const App: React.FC = () => {
    const [m_labirinth, SetLabirinth] = useState<LabitinthInfo | null>(null);

    useEffect(() => {
        let stopped = false;
        (async () => {
            try {
                if(stopped) {
                    return;
                }
                const labirinth = await LoadLagirinthFromServer();
                if(stopped) {
                    return;
                }
                console.log(`Labirinth: ${labirinth.cells}`);
                SetLabirinth(labirinth);
            } catch(e) {
                console.error("Error fetching the data:", e);
            }
        })();

        return () => {
            stopped = true;
        };
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Labirinth</h1>
            </header>
            {m_labirinth
                ?
                <div>
                    <p>#{m_labirinth.id}, {m_labirinth.width}:{m_labirinth.height}</p>
                    <Labirinth value={m_labirinth} OnClick={() => {}}/>
                    <pre>{m_labirinth.test}</pre>
                    <p>Status: {m_labirinth.status}</p>
                </div>

                : <p>Loading...</p>
            }
        </div>
    );
};

async function LoadLagirinthFromServer(): Promise<LabitinthInfo>  {
    return (await axios.get("/get-labirinth")).data;
}

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
                            return AppendClassName(acc, wall_to_class[1]);
                        } else {
                            return acc;
                        }
                    }, "");

                const td =
                    <td className={AppendClassName("labirinth-cell", border_class_name)}
                        onClick={() => params.OnClick(idx)}
                        key={`cell${idx}`}
                    />;

                if(idx === 0) {
                    // first cell
                    acc.cur_row.push(td);
                } else if(idx === params.value.cells.length-1) {
                    // last cell
                    acc.cur_row.push(td);
                    acc.rows.push(
                        <tr key={`row${idx}`}>{acc.cur_row}</tr>
                    );
                } else if(idx % params.value.width === 0) {
                    // next row
                    acc.rows.push(
                        <tr key={`row${idx}`}>{acc.cur_row}</tr>
                    );
                    acc.cur_row = [td];
                } else {
                    acc.cur_row.push(td);
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

function HasWall(cell: number,
                 wall: CellWalls
                 ): boolean
{
    const check = (cell & wall) === wall;
    return check;
}

function AppendClassName(to: string,
                         class_name: string
                        ): string
{
    if(to) {
        return to + " " + class_name;

    } else {
        return class_name;
    }
}
