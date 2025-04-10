# Running the Project with Docker

To run this project using Docker, follow these steps:

## Prerequisites

- Ensure Docker and Docker Compose are installed on your system.
- Verify that the `Requirements.txt` file contains all necessary Python dependencies.

## Environment Variables

- `FLASK_APP`: Set to `app.py` to specify the Flask application entry point.
- Database service:
  - `POSTGRES_USER`: Database username (default: `user`).
  - `POSTGRES_PASSWORD`: Database password (default: `password`).
  - `POSTGRES_DB`: Database name (default: `casino`).

## Build and Run Instructions

1. Build and start the services:

   ```bash
   docker-compose up --build
   ```

2. Access the application:

   - Application: [http://localhost:5000](http://localhost:5000)

## Exposed Ports

- Application service: `5000` (mapped to host `5000`).
- Database service: Not exposed to the host.

## Notes

- The application code is located in the `./` directory.
- The database data is persisted in the `db_data` volume.

For further details, refer to the existing documentation in the repository.