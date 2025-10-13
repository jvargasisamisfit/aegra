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


def format_event_summary(run_id: str, event_count: int) -> str:
    """Format a summary of events for a run.

    Args:
        run_id: The run identifier
        event_count: Number of events

    Returns:
        Formatted summary string
    """
    if event_count == 0:
        return f"Run {run_id} has no events"
    elif event_count == 1:
        return f"Run {run_id} has 1 event"
    else:
        return f"Run {run_id} has {event_count} events"
