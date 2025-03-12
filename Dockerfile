# Use a specific Python version
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . /app/

# Expose port
EXPOSE 8000

# Command to run the app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
