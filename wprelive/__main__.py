import uvicorn

from .app import app


def main() -> None:
    """Entry point for starting Uvicorn ASGI host."""
    uvicorn.run(app, host="0.0.0.0", port=80, reload=False)


if __name__ == "__main__":
    main()
