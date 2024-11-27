import os.path
import pymem
import pymem.process
from typing import TypeAlias

# TODO: Create Documentation
# TODO: What Kind of Errors from pymem?
# TODO: Clean File
# TODO: Type hinting, some might return None?

def read_memory(_process: pymem.Pymem, _address: int) -> int:
    """
    Reads the long long in _process at _address

    Args:
        _process: the pymem process
        _address: the address in memory

    Returns:
        int: the long long value at that location
    """
    
    memory_value = _process.read_longlong(_address)
    return memory_value

def read_memory_int(_process: pymem.Pymem, _address: int) -> int:
    """
    Reads the int in _process at _address

    Args:
        _process: the pymem process
        _address: the address in memory

    Returns:
        int: the int value at that location
    """
    
    memory_value = _process.read_int(_address)
    return memory_value

def read_memory_short(_process: pymem.Pymem, _address: int) -> int:
    """
    Reads the short in _process at _address

    Args:
        _process: the pymem process
        _address: the address in memory

    Returns:
        int: the short value at that location
    """
    
    memory_value = _process.read_short(_address)
    return memory_value

def read_memory_float(_process: pymem.Pymem, _address: int) -> float:
    """
    Reads the float in _process at _address

    Args:
        _process: the pymem process
        _address: the address in memory

    Returns:
        float: the float value at that location
    """
    
    memory_value = _process.read_float(_address)
    return memory_value

def read_memory_double(_process: pymem.Pymem, _address: int) -> float:
    """
    Reads the double in _process at _address

    Args:
        _process: the pymem process
        _address: the address in memory

    Returns:
        float: the double value at that location
    """
    
    memory_value = _process.read_double(_address)
    return memory_value

def read_memory_bytes(_process: pymem.Pymem, _address: int, _len: int, _asInt: bool = False, _signed: bool = False) -> int | bytes:
    """
    Reads the bytes in _process at _address.

    Args:
        _process: the pymem process
        _address: the address in memory
        _len: the number of bytes to read
        _asInt: If the value is returned as an integer or raw bytes
        _signed: If the value is interpreted as a signed integer

    Returns:
        bytes or int at that location
    """
    
    memory_value = _process.read_bytes(_address, _len)
    if _asInt:
        memory_value = int.from_bytes(memory_value, signed=_signed)
    return memory_value

def write_memory(_process: pymem.Pymem, _address: int, _value: int) -> None:
    """
    Writes the long long _value at _address in _process

    Args:
        _process: the pymem process
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    
    _process.write_longlong(_address, _value)

def write_memory_int(_process: pymem.Pymem, _address: int, _value: int) -> None:
    """
    Writes the int _value at _address in _process

    Args:
        _process: the pymem process
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    
    _process.write_int(_address, _value)

def write_memory_short(_process: pymem.Pymem, _address: int, _value: int) -> None:
    """
    Writes the short _value at _address in _process

    Args:
        _process: the pymem process
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    
    _process.write_short(_address, _value)

def write_memory_float(_process: pymem.Pymem, _address: int, _value: float) -> None:
    """
    Writes the float _value at _address in _process

    Args:
        _process: the pymem process
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    
    _process.write_float(_address, _value)

def write_byte(_process: pymem.Pymem, _address: int, _byte: bytes) -> None:
    """
    Writes the byte _value at _address in _process

    Args:
        _process: the pymem process
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    
    _process.write_bytes(_address, bytes(_byte), len(bytes(_byte)))

if __name__ == "__main__":
    ...