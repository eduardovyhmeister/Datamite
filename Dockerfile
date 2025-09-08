FROM python:3.13-alpine3.22
LABEL maintainer="Bastien Pietropaoli - Insight Centre for Data Analytics / UCC"

#define that all errors are sent to terminal
ENV PYTHONUNBUFFERED=1

# Ensure the python site-packages scripts are in the PATH
# For Alpine, Python executables are often in /usr/local/bin
ENV PATH="/usr/local/bin:$PATH"

# Install system dependencies needed for building Python packages
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base \
    linux-headers \
    freetype-dev \
    libpng-dev \
    pkgconfig

# Install the dependencies specified in the requirements file
WORKDIR /install
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt && python3 -m pip list

# Copy the rest of the application code into the container
WORKDIR /ANPAHP
COPY . .

# Expose the port that your application will run on
# (change 8000 to the appropriate port if necessary)
EXPOSE 8000

# Set the environment variables if needed
#ENV PATH="/py/bin:$PATH"

# Define the command to run the application
# (change "your_script.py" to the main script of your application)
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]