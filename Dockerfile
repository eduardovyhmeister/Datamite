FROM python:3.14-bookworm
# FROM python:3.13-alpine3.22
LABEL maintainer="Bastien Pietropaoli - Insight Centre for Data Analytics / UCC"

#define that all errors are sent to terminal
ENV PYTHONUNBUFFERED=1

# Ensure the python site-packages scripts are in the PATH
# For Alpine, Python executables are often in /usr/local/bin
ENV PATH="/usr/local/bin:$PATH"

# Install system dependencies needed for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config \
        libcairo2-dev \
        libffi-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update --fix-missing && \
    apt-get install -y --fix-missing build-essential
# RUN apk add --no-cache \
#     gcc \
#     musl-dev \
#     libffi-dev \
#     openssl-dev \
#     python3-dev \
#     build-base \
#     linux-headers \
#     freetype-dev \
#     libpng-dev \
#     cairo-dev \
#     pkgconfig \
#     cmake

# Install the dependencies specified in the requirements file
WORKDIR /install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --verbose
RUN python3 -m pip install openai
# RUN python3 -m pip install onnxruntime
RUN python3 -m pip install chromadb --verbose
RUN python3 -m pip install langchain
RUN python3 -m pip install langchain-community
RUN python3 -m pip install langchain-core
RUN python3 -m pip install langchain-openai
RUN python3 -m pip install langchain-anthropic
RUN python3 -m pip install langchain-deepseek
# RUN python3 -m pip install langchain-chroma
RUN python3 -m pip install langchain-huggingface
RUN python3 -m pip install langchain-text-splitters

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