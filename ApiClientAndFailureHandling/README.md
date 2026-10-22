# Day 3 — API Client and Failure Handling

## 1. Project Overview

This project implements a Python API client to retrieve user data from an external REST API. It demonstrates HTTP requests, JSON response handling, timeout management, retry logic, error handling, pagination, and automated testing.

## 2. Objectives

- Implement API communication using Python's `requests` library.
- Configure request timeouts and retry temporary failures.
- Handle HTTP errors and malformed JSON responses.
- Implement bounded pagination to retrieve records safely.
- Write automated unit tests using `pytest` and mocked responses.

## 3. Technologies Used

- Python 3.14
- Requests
- Pytest
- JSONPlaceholder REST API
- Git and GitHub

## 4. Project Structure

```text
ApiClientAndFailureHandling/
├── api_client.py
├── main.py
├── requirements.txt
├── README.md
└── tests/
    └── test_api_client.py
```

## 5. Key Features

- **API Requests:** Retrieves user information from an external API.
- **Timeout Handling:** Limits how long a request can wait for a response.
- **Retry Logic:** Retries temporary failures, including timeouts and selected server errors.
- **HTTP Error Handling:** Handles unsuccessful HTTP responses appropriately.
- **JSON Validation:** Detects malformed JSON responses and unexpected response structures.
- **Pagination:** Limits the number of pages requested.
- **Automated Testing:** Uses mocked responses to test success and failure scenarios without relying on a live API.

## 6. Installation

Install the required dependencies:

```bash
py -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
requests
pytest
```

## 7. How to Run the Project

Run the API client application:

```bash
py main.py
```

Run the automated tests:

```bash
py -m pytest tests/test_api_client.py -v
```

## 8. Sample Output

```text
Successfully fetched 10 users
ID: 1, Name: Leanne Graham
ID: 2, Name: Ervin Howell
ID: 3, Name: Clementine Bauch
ID: 4, Name: Patricia Lebsack
ID: 5, Name: Chelsey Dietrich
ID: 6, Name: Mrs. Dennis Schulist
ID: 7, Name: Kurtis Weissnat
ID: 8, Name: Nicholas Runolfsdottir V
ID: 9, Name: Glenna Reichert
ID: 10, Name: Clementina DuBuque
```

## 9. Testing Results

All 8 automated test cases passed successfully.

The tests cover successful responses, timeout retries, retry limits, server errors, 404 responses, malformed JSON, pagination limits, and invalid page sizes.

## 10. Learning Outcomes

- Understanding REST API integration in Python.
- Implementing robust error handling and retry mechanisms.
- Working with JSON data and pagination.
- Writing automated tests using `pytest` and mocks.
- Documenting a Python project and preparing it for version control.

## 11. Conclusion

The project successfully demonstrates how to build and test a Python API client with configurable timeouts, retry logic, error handling, and bounded pagination. The live API run retrieved 10 user records, and all 8 automated tests passed.