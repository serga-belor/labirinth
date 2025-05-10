FROM python:3.13-alpine

WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the server files
COPY . .

# Expose the port your server listens on
EXPOSE 5000

# Start the server
CMD ["python", "server.py"]
