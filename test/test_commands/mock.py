from unittest.mock import PropertyMock

from aiogram.fsm.state import State


class MockFSMContext:
    def __init__(self):
        self.state: State = None
        self.data: dict = None

    async def set_state(self, state: State):
        self.state = state

    async def get_state(self) -> State:
        return self.state

    async def update_data(self, **kwargs):
        if self.data is None:
            self.data = {}
        self.data.update(kwargs)

    async def get_data(self) -> dict:
        if self.data is None:
            return {}
        return self.data

    async def clear(self):
        self.state = None
        self.data = None

    def is_clear_state(self):
        return self.state is None

