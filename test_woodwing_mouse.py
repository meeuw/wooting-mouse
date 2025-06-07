"""
wooting_mouse unit tests
"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, call
import asyncio
import wooting_mouse
import evdev
import collections

CONFIG = {
    "mouse": {
        "ev_abs_mouse_write_map": {
            evdev.ecodes.ecodes["ABS_X"]: evdev.ecodes.ecodes["REL_X"],
            evdev.ecodes.ecodes["ABS_Y"]: evdev.ecodes.ecodes["REL_Y"],
            evdev.ecodes.ecodes["ABS_RX"]: evdev.ecodes.ecodes["REL_HWHEEL_HI_RES"],
            evdev.ecodes.ecodes["ABS_RY"]: evdev.ecodes.ecodes["REL_WHEEL_HI_RES"],
        }
    },
    "gamepad": {
        "ev_key_mouse_write_map": {
            evdev.ecodes.ecodes["BTN_SOUTH"]: evdev.ecodes.ecodes["KEY_CAPSLOCK"],
            evdev.ecodes.ecodes["BTN_TL"]: evdev.ecodes.ecodes["KEY_LEFTCTRL"],
            evdev.ecodes.ecodes["BTN_TR"]: evdev.ecodes.ecodes["KEY_LEFTALT"],
            evdev.ecodes.ecodes["BTN_EAST"]: evdev.ecodes.ecodes["BTN_LEFT"],
            evdev.ecodes.ecodes["BTN_NORTH"]: evdev.ecodes.ecodes["BTN_MIDDLE"],
            evdev.ecodes.ecodes["BTN_WEST"]: evdev.ecodes.ecodes["BTN_RIGHT"],
        },
        "ev_abs_mouse_write_map": {
            evdev.ecodes.ecodes["ABS_HAT0X"]: (
                evdev.ecodes.ecodes["BTN_BACK"],
                evdev.ecodes.ecodes["BTN_FORWARD"],
            )
        },
    },
}


class FakeInputDevice:
    def __init__(self, queue):
        self.queue = queue

    def async_read_loop(self):
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.queue.get()


class Test(IsolatedAsyncioTestCase):
    """
    Test Case
    """

    def setUp(self):
        self.events = asyncio.Queue()
        self.state = {
            evdev.ecodes.ecodes["EV_SYN"]: collections.defaultdict(int),
            evdev.ecodes.ecodes["EV_ABS"]: collections.defaultdict(int),
            evdev.ecodes.ecodes["EV_KEY"]: collections.defaultdict(int),
        }
        self.mouse = MagicMock()
        self.rgb_lighting = MagicMock()
        self.wooting_mouse = wooting_mouse.gamepad(
            FakeInputDevice(self.events),
            self.state,
            self.mouse,
            self.rgb_lighting,
            CONFIG
        )


    async def send_event(self, type, code, value):
        await self.events.put(
            evdev.events.InputEvent(
                sec=0,
                usec=0,
                type=evdev.ecodes.ecodes[type],
                code=evdev.ecodes.ecodes[code],
                value=value,
            )
        )


    async def test_gamepad(self):
        async def _tests():
            await self.send_event("EV_KEY", "BTN_SOUTH", 1)
            await self.send_event("EV_KEY", "BTN_SOUTH", 0)
            await self.send_event("EV_ABS", "ABS_HAT0X", 1)
            await self.send_event("EV_ABS", "ABS_HAT0X", 0)
            while not self.events.empty():
                await asyncio.sleep(0.1)
            assert self.mouse.mock_calls == [
                call.enable(),
                call.write(1, evdev.ecodes.ecodes["KEY_CAPSLOCK"], 1),
                call.write(1, evdev.ecodes.ecodes["KEY_CAPSLOCK"], 0),
                call.enable(),
                call.write(1, evdev.ecodes.ecodes["BTN_FORWARD"], 1),
                call.write(1, evdev.ecodes.ecodes["BTN_FORWARD"], 0),
            ]

            tasks.cancel()

        tasks = asyncio.gather(self.wooting_mouse, _tests())
        try:
            await tasks
        except asyncio.exceptions.CancelledError:
            pass
