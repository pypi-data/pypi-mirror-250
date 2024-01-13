# Alternate approach to handle KeyboardInterrupt as in previous approach, input can't be done in signal handler function


from threading import Event

global terminate_event


def signal_handler(sig, frame):
    # Set a flag to trigger termination from the main loop
    terminate_event.set()


def main():
    global terminate_event
    terminate_event = Event()

    # ...your lineage management code...

    while not terminate_event.is_set():
        # ...handle user input using your preferred methods...
        # ...perform lineage actions based on user input...

        # Check for termination flag set by signal handler
        if terminate_event.is_set():
            # Perform cleanup and exit gracefully
            break

    # ...further cleanup tasks...


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()
