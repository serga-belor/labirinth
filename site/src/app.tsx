// Copyright Sergei Belorusets, 2024-2026

export { App };


import { Labyrinth, LabyrinthInfo, SetCurrent } from "./labyrinth";

import React, { useEffect, useState } from "react";
import axios from "axios";


const App: React.FC = () => {
    const [m_labyrinth, setLabyrinth] = useState<LabyrinthInfo | null>(null);

    useEffect(() => {
        let stopped = false;
        (async () => {
            try {
                if(stopped) {
                    return;
                }
                const labyrinth = await LoadLabyrinthFromServer();
                if(stopped) {
                    return;
                }
                console.log(`Labyrinth: ${labyrinth.cells}`);
                setLabyrinth(labyrinth);
            } catch(e) {
                console.error("Error fetching the data:", e);
            }
        })();

        return () => {
            stopped = true;
        };
    }, []);

    return (
        <div className="app">
            <header className="app-header">
                <h1>Labyrinth</h1>
            </header>
            {m_labyrinth
                ?
                <div>
                    <p>#{m_labyrinth.id}, {m_labyrinth.width}:{m_labyrinth.height}</p>
                    <Labyrinth
                        value={m_labyrinth}
                        OnClick={(idx) => {
                            setLabyrinth({
                                ...m_labyrinth,
                                cells: m_labyrinth.cells.map((cell, i) => {
                                    return SetCurrent(cell, i === idx);
                                })
                            });
                    }}/>
                    {/*<Controls />*/}
                    <pre>{m_labyrinth.test}</pre>
                    <p>Status: {m_labyrinth.status}</p>
                </div>

                : <p>Loading...</p>
            }
        </div>
    );
};

async function LoadLabyrinthFromServer(): Promise<LabyrinthInfo>  {
    return (await axios.get("/get-labyrinth")).data;
}
