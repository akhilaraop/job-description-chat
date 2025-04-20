# Use Python 3.10 base image
FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Copy the .env file
COPY .env .

# Copy the rest of the application
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"] 