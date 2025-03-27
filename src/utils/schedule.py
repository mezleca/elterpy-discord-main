import asyncio

class Scheduler:
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval
        self.stop = False
        self.task = None

    async def _run(self):
        while not self.stop:
            await self.func()
            await asyncio.sleep(self.interval)

    def start(self):
        self.stop = False
        self.task = asyncio.create_task(self._run())

    def stop_scheduler(self):
        print("stoping scheduler")
        self.stop = True 
        if self.task:
            self.task.cancel()


