# Step 1: Use an official Python runtime as the base image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose port 5000 to the outside world (Flask default)
EXPOSE 5000

# Step 6: Use Gunicorn to run the app in production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
