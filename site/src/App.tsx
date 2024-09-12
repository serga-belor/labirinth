export { App };

import React, { useEffect, useState } from "react";
import axios from "axios";

interface TestServerResponse {
    message: string;
    status: string
}

const App: React.FC = () => {
    const [m_test, setData] = useState<TestServerResponse | null>(null);

    useEffect(() => {
        let stopped = false;
        (async () => {
            try {
                const data = await LoadTestFromServer();
                if(!stopped) {
                    setData(data);
                }
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
            {m_test
                ?
                <div>
                    <p>Message:</p>
                    <pre>{m_test.message}</pre>
                    <p>Status: {m_test.status}</p>
                </div>

                : <p>Loading...</p>
            }
        </div>
    );
};

async function LoadTestFromServer(): Promise<TestServerResponse>  {
    return (await axios.get("/test")).data;
}

interface LabitinthInfoResponse {
    readonly width: number;
    readonly height: number;
    readonly cells: ReadonlyArray<number>;
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
    return (cell & wall) === wall;
}
