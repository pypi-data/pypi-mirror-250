# Email Verification
## Description
This project is a FastAPI application designed to interact with the Hunter.io API. It provides functionality to verify email addresses and search emails by domain, with CRUD operations for managing the results. The application stores results in a local variable and is structured to demonstrate basic API interaction and data handling in FastAPI.

## Features
 - Email verification using Hunter.io API
 - Search for emails associated with a domain
 - CRUD operations for managing email verification results
 - Local storage of verification results
 - Asynchronous request handling

## Installation
This project uses Poetry for dependency management. To set up the project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/alexsproject/email-verification.git
cd pythonProject
```
2. Install dependencies using Poetry:
```bash
poetry install
```
## Usage
To run the FastAPI server:
```bash
poetry run python3 -m main
```
This command will start the FastAPI application with hot-reload enabled.

## API Endpoints
 - POST /verify-email: Verifies the email address.
 - POST /search-email: Search for email addresses by domain.
 - POST /email-results/: Create a result entry for an email address or domain.
 - GET /email-results/{identifier}: Retrieve a specific verification result by email or domain.
 - PUT /email-results/{identifier}: Update a specific verification result.
 - DELETE /email-results/{identifier}: Delete a specific verification result.

## Configuration
The application can be configured through environment variables. Here are the available configurations:

 - API_KEY: Your Hunter.io API key.

## Contributing
Contributions to this project are welcome. Please ensure to follow the code of conduct and coding standards of the project.