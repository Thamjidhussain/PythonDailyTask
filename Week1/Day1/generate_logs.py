from datetime import datetime, timedelta
import random


levels = [
    "INFO",
    "INFO",
    "INFO",
    "WARNING",
    "WARNING",
    "ERROR"
]


messages = {
    "INFO": [
        "Application started",
        "User login successful",
        "Request processed successfully",
        "Application health check passed",
        "User logout successful"
    ],

    "WARNING": [
        "Memory usage is high",
        "CPU usage is high",
        "Slow response detected",
        "Connection pool is almost full"
    ],

    "ERROR": [
        "Database connection failed",
        "File not found",
        "Authentication failed",
        "Request timeout",
        "Unable to process request"
    ]
}


start_time = datetime(
    2026, 10, 6, 9, 0, 0
)


with open(
    "sample_server.log",
    "w",
    encoding="utf-8"
) as file:

    for i in range(600):

        timestamp = start_time + timedelta(
            seconds=i * 30
        )

        level = random.choice(levels)

        message = random.choice(
            messages[level]
        )

        file.write(
            f"{timestamp:%Y-%m-%d %H:%M:%S} "
            f"{level} "
            f"{message}\n"
        )


print("sample_server.log created with 600 lines.")