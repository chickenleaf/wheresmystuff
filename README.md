# Lost and Found Matcher

This project is a Lost and Found Matcher system built with FastAPI, MongoDB, Elasticsearch, and Celery. It allows users to submit descriptions of lost items and found items, and automatically matches them using smart search algorithms.

## Features

- User registration and authentication
- Submission of lost and found items
- Automated matching of lost and found items
- Search functionality with filters (category, location, date)
- Asynchronous processing of submissions
- Logging and monitoring with ELK stack

## Tech Stack

- Backend: FastAPI
- Database: MongoDB
- Search Engine: Elasticsearch
- Message Queue: Celery with RabbitMQ
- Frontend: Basic Bootstrap
- Containerization: Docker
- Logging and Monitoring: ELK Stack (Elasticsearch, Logstash, Kibana)

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/lost-and-found-matcher.git
   cd lost-and-found-matcher
   ```

2. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Kibana Dashboard: http://localhost:5601

## API Endpoints

- `/auth/register`: Register a new user
- `/auth/token`: Get authentication token
- `/items/`: Create and list items
- `/items/{item_id}`: Get, update, or delete a specific item
- `/matches/{item_id}`: Get potential matches for an item

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.