FROM python:3.12
LABEL authors="gabriel.cerioni"

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable - lets mount this somewhere else, such as secrets from vault then K8s with Harness
#ENV REDIS_CONN_STR=redis://default:password@localhost:6379/0
#ENV REDIS_CSV_FILE_NAME=/tmp/output.csv

# Copy the entrypoint script and make it executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]

# Default command
CMD ["--help"]