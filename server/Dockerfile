FROM node:22-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source and static files
COPY src ./src
COPY public ./public
COPY tsconfig.json ./

# Build and run
RUN npm run build

EXPOSE 5000

CMD ["npm", "start"]
