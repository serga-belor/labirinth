# Labyrinth

This project contains a maze generator with:
- a Node.js backend server written in TypeScript
- a frontend built with Webpack, TypeScript, and React

## Install build tools
```bash
npm install -g webpack webpack-cli
```

## Before build
```bash
npm update
```

## Site address
`http://localhost:3001/`

## Project structure
```text
project-root/
├── server/                   # Node.js + TypeScript HTTP server
│   ├── src/
│   │   └── [...]             # TypeScript server code
│   ├── package.json          # Node dependencies and scripts
│   ├── tsconfig.json         # TypeScript config for server build
│   └── Dockerfile            # Container for the Node server
├── site/                     # TypeScript/HTML app
│   ├── src/
│   │   └── [...]             # TypeScript source code
│   ├── public/               # Static assets (HTML, CSS, images)
│   ├── package.json
│   ├── tsconfig.json
│   ├── webpack.config.js
│   └── Dockerfile            # Build container for the client
├── docker-compose.yml        # Compose file to run services
└── .gitignore                # Exclude build artifacts, node_modules, etc.
```

## Maze concept
A maze is an `M x N` grid of cells.

Between vertically or horizontally adjacent cells, movement may be allowed or blocked.
If one cell can reach another through a sequence of allowed moves, then a path exists between them.

### Goal
Generate a maze where:
- there is exactly one path between any two cells
- there are no loops

### Main implementation idea
Represent the maze as an undirected graph:
- cells are graph vertices
- transitions (allowed or blocked) are graph edges

The goal is achieved when the generated graph is connected and acyclic.

### Generation steps
1. Create a maze graph where all transitions are initially allowed.
2. Randomly block one transition.
3. Traverse the graph:
1. Move to the next vertex.
2. If the vertex is already in the visited set, the graph contains a cycle: block this transition, return to the previous vertex, and continue from step 7.
3. Add the vertex to the visited set.
4. Randomly choose the next allowed transition from this vertex.
5. If such a transition exists, go to step 1.
6. If no allowed transitions remain, return to the previous vertex.
7. If a previous vertex exists, go to step 4.
8. If there is no previous vertex, traversal is complete.
9. If the number of visited vertices equals the total number of vertices, the graph is connected.
