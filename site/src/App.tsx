import React, { useState, useEffect } from "react";
import axios from "axios";

const App: React.FC = () => {
    const [data, setData] = useState<{ message: string; status: string } | null>(null);

    useEffect(() => {
        axios.get("/data")
            .then(response => {
                setData(response.data);
            })
            .catch(error => {
                console.error("Error fetching the data:", error);
            });
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>React + Flask Example</h1>
                {data ? (
                    <div>
                        <p>Message: {data.message}</p>
                        <p>Status: {data.status}</p>
                    </div>
                ) : (
                    <p>Loading...</p>
                )}
            </header>
        </div>
    );
}

export default App;
