FROM python:3.13
LABEL maintainer="eduardo vyhmeister - insight centre"

#define that all errors are sent to terminal
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /ANPAHP

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your application will run on
# (change 8000 to the appropriate port if necessary)
EXPOSE 8000

# Set the environment variables if needed
#ENV PATH="/py/bin:$PATH"

# Define the command to run the application
# (change "your_script.py" to the main script of your application)
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]