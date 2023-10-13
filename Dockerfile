# Use the official Python image as base
FROM python:3.11

# Set the working directory in the container
WORKDIR /src

# Create the 'data' directory if it doesn't exist
RUN mkdir -p /src/data && chown -R root:root /src/data

# # Set permissions for the 'data' directory
# RUN chmod 777 /app/data

# Copy the 'data' directory into the image
# COPY data /app/data
# RUN if [ -d "data" ]; then cp -r data /app/; fi

# Copy the project files and install dependencies
COPY . /src/

RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir poetry && poetry install --no-root

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Start the FastAPI application
CMD ["poetry", "run", "uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8000"]
