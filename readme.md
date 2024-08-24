# DailyFileGuardian

This microservice monitors specified folders within the `/data` directory (or another specified directory) and checks daily if they have been updated. If any folder has not been updated by the specified time, an email notification is sent to the configured recipients.

## Features

- **Daily Monitoring**: The service checks the last modification date of specified folders.
- **Email Notifications**: If a folder has not been updated, an email alert is sent to the recipients.
- **Configurable Settings**: The service uses a `config.ini` file for easy configuration of email settings, recipients, folders to monitor, and the cron job schedule.
- **Dockerized Service**: The microservice is containerized using Docker, making it easy to deploy and run in isolated environments.

## Configuration

All settings are stored in a `config.ini` file located in the same directory as the script. Below is a template for the configuration file:

```ini
[EMAIL]
email_address = your-email@example.com
email_password = your-password
smtp_server = smtp.example.com
smtp_port = 465

[SETTINGS]
cron_time = 20:00
folders = reports, logs

[RECIPIENTS]
to_array = recipient1@example.com, recipient2@example.com
```

### Configuration Details

- **[EMAIL] Section**:
  - `email_address`: The email address used to send notifications.
  - `email_password`: The password for the email account (use an app-specific password if necessary).
  - `smtp_server`: The SMTP server address (e.g., `smtp.example.com`).
  - `smtp_port`: The SMTP port (typically 465 for SSL).

- **[SETTINGS] Section**:
  - `cron_time`: The time at which the daily check should run (in 24-hour format, e.g., `20:00` for 8:00 PM).
  - `folders`: A comma-separated list of folder names within the specified directory (usually `/data`) to monitor.

- **[RECIPIENTS] Section**:
  - `to_array`: A comma-separated list of email addresses that should receive notifications.

## Running the Service with Docker

This microservice is designed to run within a Docker container. Below are the steps to build and run the service using Docker.

### Prerequisites

Ensure that both Docker and Docker Compose are installed on your system.

- **Install Docker**: Follow the official Docker [installation guide](https://docs.docker.com/get-docker/) for your operating system.
- **Install Docker Compose**: Follow the official Docker Compose [installation guide](https://docs.docker.com/compose/install/).

### Setting Up Docker Compose

1. **Create a `Dockerfile`**: The `Dockerfile` included in the project is used to create a Docker image for the service. It installs the necessary dependencies, adds the service script and configuration files, and sets up the environment for running the service.

2. **Create a `docker-compose.yml` file**: This file is used to manage the service as a Docker container. It defines the service, builds the Docker image, and mounts a volume where the folders to be monitored are located.

   Example `docker-compose.yml`:

   ```yaml
   version: "3.9"
   services:
     script:
       build: .
       volumes:
         - /home/docker/nextcloud/nextcloud/data:/data
   ```

   #### Customizing the Directory to Monitor

   The volume mapping in the `docker-compose.yml` file specifies which directory on the host machine will be mounted to the `/data` directory inside the Docker container. For example:

   - **Monitoring a Specific Directory**: To monitor a specific directory, modify the volume path:

     ```yaml
     volumes:
       - /path/to/your/directory:/data
     ```

   - **Monitoring the Entire System**: To monitor the entire file system, map the root directory:

     ```yaml
     volumes:
       - /:/data
     ```

### Building and Running the Docker Container

1. **Navigate to the directory containing your `docker-compose.yml` file**:

   ```bash
   cd /path/to/your/project
   ```

2. **Build the Docker Image**:

   ```bash
   docker-compose build
   ```

   This command will build the Docker image based on the `Dockerfile` and install all necessary dependencies.

3. **Run the Docker Container**:

   ```bash
   docker-compose up -d
   ```

   This command will start the container in detached mode (running in the background).

4. **Check Logs and Monitor the Service**:

   You can monitor the logs of the running container to ensure everything is functioning correctly:

   ```bash
   docker logs <container_name>
   ```

   Replace `<container_name>` with the name of the running container, which you can find by running:

   ```bash
   docker ps
   ```

5. **Stopping the Container**:

   To stop the running container, use the following command:

   ```bash
   docker-compose down
   ```

## Dependencies

The service requires the following Python packages:

- `schedule`
- `smtplib`
- `configparser`

These are specified in the `requirements.txt` file and will be installed automatically when the Docker image is built.

## License

This project is open-source and available under the [MIT License](LICENSE).
