import os.path
import pymem
import pymem.process
import pymem.pattern

# TODO: Create Documentation
# TODO: What Kind of Errors from pymem?
# TODO: Clean File
# TODO: Type hinting, some might return None?

def read_memory(_process: str, _address: int) -> int:
    """
    Reads the long long in _process at _address

    Args:
        _process: the process name
        _address: the address in memory

    Returns:
        int: the long long value at that location
    """
    pm = pymem.Pymem(_process)
    memory_value = pm.read_longlong(_address)
    return memory_value

def read_memory_int(_process: str, _address: int) -> int:
    """
    Reads the int in _process at _address

    Args:
        _process: the process name
        _address: the address in memory

    Returns:
        int: the int value at that location
    """
    pm = pymem.Pymem(_process)
    memory_value = pm.read_int(_address)
    return memory_value

def read_memory_short(_process: str, _address: int) -> int:
    """
    Reads the short in _process at _address

    Args:
        _process: the process name
        _address: the address in memory

    Returns:
        int: the short value at that location
    """
    pm = pymem.Pymem(_process)
    memory_value = pm.read_short(_address)
    return memory_value

def read_memory_float(_process: str, _address: int) -> float:
    """
    Reads the float in _process at _address

    Args:
        _process: the process name
        _address: the address in memory

    Returns:
        float: the float value at that location
    """
    pm = pymem.Pymem(_process)
    memory_value = pm.read_float(_address)
    return memory_value

def read_memory_double(_process: str, _address: int) -> float:
    """
    Reads the double in _process at _address

    Args:
        _process: the process name
        _address: the address in memory

    Returns:
        float: the double value at that location
    """
    pm = pymem.Pymem(_process)
    memory_value = pm.read_double(_address)
    return memory_value

def read_memory_bytes(_process: str, _address: int, _len: int) -> bytes:
    """
    Reads the bytes in _process at _address

    Args:
        _process: the process name
        _address: the address in memory
        _len: the number of bytes to read

    Returns:
        bytes: the bytes at that location
    """
    pm = pymem.Pymem(_process)
    memory_value = pm.read_bytes(_address, _len)
    return memory_value

def write_memory(_process: str, _address: int, _value: int) -> None:
    """
    Writes the long long _value at _address in _process

    Args:
        _process: the process name
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    pm = pymem.Pymem(_process)
    pm.write_longlong(_address, _value)

def write_memory_int(_process: str, _address: int, _value: int) -> None:
    """
    Writes the int _value at _address in _process

    Args:
        _process: the process name
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    pm = pymem.Pymem(_process)
    pm.write_int(_address, _value)

def write_memory_short(_process: str, _address: int, _value: int) -> None:
    """
    Writes the short _value at _address in _process

    Args:
        _process: the process name
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    pm = pymem.Pymem(_process)
    pm.write_short(_address, _value)

def write_memory_float(_process: str, _address: int, _value: float) -> None:
    """
    Writes the float _value at _address in _process

    Args:
        _process: the process name
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    pm = pymem.Pymem(_process)
    pm.write_float(_address, _value)

def write_byte(_process: str, _address: int, _byte: bytes) -> None:
    """
    Writes the byte _value at _address in _process

    Args:
        _process: the process name
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    pm = pymem.Pymem(_process)
    pm.write_bytes(_address, bytes(_byte), len(bytes(_byte)))

def read_cheat_engine_file(_filename: str) -> int:
    """
    Reads the file that is provided and returns the address from the file

    Args:
        _filename: the name of the file to read

    Returns:
        int: the address that was stored in the file
    """
    ret_val = None
    if os.path.isfile('place_cheat_table_here/' + _filename):
        with open('place_cheat_table_here/' + _filename, 'r') as file:
            fval = file.readline()
            if fval in ['nil', '0', '']:
                return None
            ret_val = int(fval)
    return ret_val

if __name__ == "__main__":
    ...