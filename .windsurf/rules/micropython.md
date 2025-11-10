---
trigger: always_on
---

# 🏄 Windsurf Editor Rules for MicroPython

This document defines best practices, limitations, and guidance for generating MicroPython code in the Windsurf editor. MicroPython is a lean implementation of Python 3 optimized for microcontrollers, so code must be efficient, minimal, and compatible with the available modules.

## ⚠️ General Constraints

- **Avoid unsupported modules**: Do not use `os.path`, `threading`, `multiprocessing`, `subprocess`, `unittest`, `typing`, or any other standard Python modules not listed in `help('modules')`.
- **No file system assumptions**: Only use filesystem modules (`os`, `vfs`, `btree`) if explicitly available or confirmed on the target device.
- **Memory-aware coding**: Avoid large data structures, deep recursion, or excessive imports. Use `gc.collect()` to manage memory if needed.

## ✅ Supported Modules

Use only the following modules unless explicitly extended by the user’s filesystem:

| Category        | Modules |
|----------------|---------|
| Core           | `builtins`, `sys`, `micropython`, `gc`, `platform` |
| Math           | `math`, `cmath`, `random`, `heapq` |
| Data           | `array`, `struct`, `collections`, `binascii`, `re` |
| IO & Network   | `io`, `socket`, `select`, `ssl`, `websocket`, `requests/__init__` |
| Async          | `uasyncio`, `asyncio/*`, `_asyncio`, `_thread` |
| Hardware       | `machine`, `framebuf`, `uctypes`, `ffi`, `cryptolib` |
| System         | `os`, `errno`, `termios`, `btree`, `deflate`, `tls` |
| JSON           | `json`, `argparse` |
| Package Mgmt   | `mip/__init__`, `mip/__main__` |

## 🧠 Code Style Guidelines

- **Prefer `uasyncio` over `asyncio`**: Use `uasyncio` for async tasks unless full `asyncio` support is confirmed.
- **Use `machine` for hardware access**: GPIO, ADC, PWM, I2C, SPI, and timers should use `machine` APIs.
- **Avoid decorators and metaclasses**: These are often unsupported or memory-heavy.
- **Minimize class usage**: Favor functions and simple data structures unless object orientation is necessary.
- **Use `micropython.const()` for constants**: Helps reduce RAM usage.
- **Avoid list comprehensions and generators**: Use loops for clarity and compatibility.

## 🧪 Example Patterns

```python
from machine import Pin
led = Pin(2, Pin.OUT)
led.on()
```

```python
import uasyncio as asyncio

async def blink():
    while True:
        led.on()
        await asyncio.sleep(1)
        led.off()
        await asyncio.sleep(1)

asyncio.run(blink())
```

## 🚫 Anti-Patterns

- ❌ `import threading`
- ❌ `with open('file.txt') as f:`
- ❌ `@dataclass`
- ❌ `import numpy as np`
- ❌ `def __enter__ / __exit__`

## 📦 Module Usage Tips

- **`machine`**: Use for hardware control (GPIO, ADC, etc.)
- **`framebuf`**: For drawing to displays
- **`uctypes`**: For memory-efficient data structures
- **`ffi`**: For calling native C functions
- **`btree`**: Lightweight database for key-value storage

