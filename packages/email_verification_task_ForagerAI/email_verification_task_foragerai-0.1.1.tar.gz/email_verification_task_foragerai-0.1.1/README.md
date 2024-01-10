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
Install this package using `pip`:

```bash
pip install email_verification_task_ForagerAI
```
Or install using poetry:
```bash
poetry add email_verification_task_ForagerAI
```
## Usage
After installation, you can use it like this:
```bash
import email_verification_task_ForagerAI
```

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