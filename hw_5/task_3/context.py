import asyncio

class AppContext:
    def __init__(self):
        self.file_lock = asyncio.Lock()

context = AppContext()
