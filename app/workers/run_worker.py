import asyncio

from backend.app.workers.background import BackgroundWorker


async def main() -> None:
    worker = BackgroundWorker()
    await worker.run_forever()


if __name__ == "__main__":
    asyncio.run(main())

