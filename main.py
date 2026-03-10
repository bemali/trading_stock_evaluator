from uvicorn import run

from src.api.app import create_app


app = create_app()


def main() -> None:
    """Entry point that starts the ASGI server."""
    run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()
