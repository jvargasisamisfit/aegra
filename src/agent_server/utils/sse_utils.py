def generate_event_id(run_id: str, sequence: int) -> str:
    """Generate SSE event ID in the format: {run_id}_event_{sequence}

    Args:
        run_id: The run identifier
        sequence: The event sequence number

    Returns:
        Formatted event ID string
    """
    return f"{run_id}_event_{sequence}"


def extract_event_sequence(event_id: str) -> int:
    """Extract numeric sequence from event_id format: {run_id}_event_{sequence}

    Args:
        event_id: The event ID string

    Returns:
        The sequence number, or 0 if extraction fails
    """
    try:
        return int(event_id.split("_event_")[-1])
    except (ValueError, IndexError):
        return 0


def validate_event_id(event_id: str) -> bool:
    """Validate if event_id follows the expected format.

    Args:
        event_id: The event ID string to validate

    Returns:
        True if event_id is valid, False otherwise
    """
    if not event_id or not isinstance(event_id, str):
        return False

    parts = event_id.split("_event_")
    if len(parts) != 2:
        return False

    try:
        int(parts[1])
        return True
    except ValueError:
        return False
