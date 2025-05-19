# Use a minimal Python image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "main.py"]