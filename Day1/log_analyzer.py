from collections import Counter


LOG_LEVELS = ("INFO", "WARNING", "ERROR")


def parse_log_line(line):
    """
    Parse one server log line.

    Expected format:
    2026-10-06 10:15:20 ERROR Database connection failed

    Returns:
        (timestamp, level, message)

    Returns None for a malformed line.
    """

    line = line.strip()

    if not line:
        return None

    parts = line.split(" ", 3)

    if len(parts) != 4:
        return None

    date = parts[0]
    time = parts[1]
    level = parts[2].upper()
    message = parts[3]

    if level not in LOG_LEVELS:
        return None

    timestamp = f"{date} {time}"

    return timestamp, level, message


def read_log_file(filename):
    """Read and parse the server log file."""

    logs = []

    try:
        with open(filename, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                parsed = parse_log_line(line)

                if parsed is None:
                    print(
                        f"Warning: Skipping malformed line "
                        f"{line_number}"
                    )
                    continue

                timestamp, level, message = parsed

                logs.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message
                })

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")

    except PermissionError:
        print(f"Error: Permission denied for '{filename}'.")

    except OSError as error:
        print(f"Error reading file: {error}")

    return logs


def count_levels(logs):
    """Count INFO, WARNING and ERROR log entries."""

    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    for log in logs:

        level = log["level"]

        if level in counts:
            counts[level] += 1

    return counts


def find_top_errors(logs, limit=5):
    """Find the most frequent ERROR messages."""

    error_messages = []

    for log in logs:

        if log["level"] == "ERROR":
            error_messages.append(log["message"])

    message_counts = Counter(error_messages)

    return message_counts.most_common(limit)


def write_error_lines(logs, filename):
    """Write only ERROR log lines to another file."""

    try:

        with open(filename, "w", encoding="utf-8") as file:

            for log in logs:

                if log["level"] == "ERROR":

                    file.write(
                        f"{log['timestamp']} "
                        f"{log['level']} "
                        f"{log['message']}\n"
                    )

    except PermissionError:
        print(
            f"Error: Permission denied while writing "
            f"'{filename}'."
        )

    except OSError as error:
        print(f"Error writing file: {error}")


def print_summary(filename, logs, counts, top_errors):
    """Print the final log analysis report."""

    print()
    print("=" * 60)
    print("              SERVER LOG ANALYSIS REPORT")
    print("=" * 60)

    print(f"File analyzed : {filename}")
    print(f"Valid records : {len(logs)}")

    print()
    print("LOG LEVEL COUNTS")
    print("-" * 30)

    print(f"INFO          : {counts['INFO']}")
    print(f"WARNING       : {counts['WARNING']}")
    print(f"ERROR         : {counts['ERROR']}")

    print()
    print("TOP 5 ERROR MESSAGES")
    print("-" * 30)

    if not top_errors:
        print("No ERROR messages found.")

    else:

        for number, (message, count) in enumerate(
            top_errors,
            start=1
        ):
            print(
                f"{number}. {message} "
                f"({count} occurrence(s))"
            )

    print()
    print("ERROR OUTPUT")
    print("-" * 30)
    print("ERROR lines were written to: errors_only.log")

    print()
    print("=" * 60)


def main():

    input_file = "sample_server.log"
    output_file = "errors_only.log"

    logs = read_log_file(input_file)

    counts = count_levels(logs)

    top_errors = find_top_errors(logs)

    write_error_lines(
        logs,
        output_file
    )

    print_summary(
        input_file,
        logs,
        counts,
        top_errors
    )


if __name__ == "__main__":
    main()