// Copyright Sergei Belorusets, 2024

export { App };


import { Labirinth, LabitinthInfo, SetCurrent } from "./labirinth";

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
        <div className="app">
            <header className="app-header">
                <h1>Labirinth</h1>
            </header>
            {m_labirinth
                ?
                <div>
                    <p>#{m_labirinth.id}, {m_labirinth.width}:{m_labirinth.height}</p>
                    <Labirinth
                        value={m_labirinth}
                        OnClick={(idx) => {
                            SetLabirinth({
                                ...m_labirinth,
                                cells: m_labirinth.cells.map((cell, i) => {
                                    return SetCurrent(cell, i === idx);
                                })
                            });
                    }}/>
                    {/*<Controls />*/}
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
