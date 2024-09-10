export { App };

import React, { useEffect, useState } from "react";
import axios from "axios";

interface GetDataServerResponse {
    message: string;
    status: string
}

const App: React.FC = () => {
    const [m_data, setData] = useState<GetDataServerResponse | null>(null);

    useEffect(() => {
        let stopped = false;
        (async () => {
            try {
                const data = await LoadFromServer();
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
            {m_data
                ?
                <div>
                    <p>Message:</p>
                    <pre>{m_data.message}</pre>
                    <p>Status: {m_data.status}</p>
                </div>

                : <p>Loading...</p>
            }
        </div>
    );
};

async function LoadFromServer(): Promise<GetDataServerResponse>  {
    return (await axios.get("/data")).data;
}
