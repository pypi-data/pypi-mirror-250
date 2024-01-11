"""
    The basic functions of the package
"""
__all__ = ["FloatArray"]

from ._gamda import _malloc_float, _free_float #pylint: disable=import-error

class FloatArray:
    """
        The 1D GPU backend array

        :param name: name of the array
        :param input_array: the numpy array to be wrapped as a GPU FloatArray
    """
    names = set()
    def __init__(self, name, input_array):
        if not isinstance(name, str):
            raise TypeError(f"The name of an array should be a str, but a {type(name)} got")
        if name in self.names:
            raise ValueError(f"There is already a FloatArray named {name}")
        self.name = name
        self.names.add(name)
        self._array = _malloc_float(name, input_array)

    def __repr__(self):
        return repr(self._array)

    def __del__(self):
        if hasattr(self.name):
            _free_float(self.name)
            self.names.remove(self.name)
