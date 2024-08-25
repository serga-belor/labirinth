export { App };

import React, { useState, useEffect } from "react";
import axios from "axios";

interface GetDataServerResponse {
    message: string;
    status: string
}

const App: React.FC = () => {
    const [data, setData] = useState<GetDataServerResponse | null>(null);

    useEffect(() => {
        try {
            (async () => {
                const response = await axios.get("/data");
                setData(response.data);
            })();
        } catch(e) {
            console.error("Error fetching the data:", e);
        }
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Labirinth</h1>
            </header>
            {data
                ?
                <div>
                    <p>Message:</p>
                    <pre>{data.message}</pre>
                    <p>Status: {data.status}</p>
                </div>

                : <p>Loading...</p>
            }
        </div>
    );
};
