// Copyright Sergei Belorusets, 2024-2026

import express from "express";
import path from "path";
import { Labyrinth, printLabyrinth } from "./labyrinth";

const publicDirPath = path.resolve(__dirname, "../public");

const app = express();
const port = Number(process.env.PORT ?? 5000);

const width = 5;
const height = 5;
let labyrinthCounter = 0;

console.log(`Public folder: ${publicDirPath}`);

app.use(express.static(publicDirPath));

app.get("/test", (_req, res) => {
  res.json({
    test: "this is test"
  });
});

app.get("/", (_req, res) => {
  res.sendFile(path.join(publicDirPath, "index.html"));
});

app.get("/get-labyrinth", (_req, res) => {
  const labyrinth = Labyrinth.generate(width, height);
  labyrinthCounter += 1;

  res.json({
    id: labyrinthCounter,
    width,
    height,
    cells: labyrinth.cellsData(),
    test: printLabyrinth(labyrinth, [0, 0]),
    status: "success"
  });
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Labyrinth server started on port ${port}`);
});
