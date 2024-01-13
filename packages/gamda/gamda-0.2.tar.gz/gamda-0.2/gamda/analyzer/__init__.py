"""
    The analysis execute
"""

import numpy as np
import cupy as cp
from ..core import *
from ..observable import Observable


#pylint: disable=too-few-public-methods, line-too-long, too-many-arguments, too-few-public-methods
class Analyzer:
    """
        The class of general analyzer

        :param name: name of the analyzer
        :param in_arg: input arguments
        :param out_arg: output arguments
        :param mid_arg: medium arguments
        :param temp_float: the number of temporary floats
        :param temp_int: the number of temporary ints
    """
    def __init__(self, name, in_arg, out_arg, mid_arg, temp_float=0, temp_int=0):
        self.name = name
        self.input = in_arg
        self.output = out_arg
        self.midium = mid_arg
        self.temp_float = temp_float
        self.temp_int = temp_int

    @property
    def source_code(self):
        """
            The source code of the observable
        """
        raise NotImplementedError


class PDF(Analyzer):
    """
        Probability Density Function analyzed by the histogram method

        :param minimal: the minimal of the value
        :param maximum: the maximum of the value
        :param n_bin: the bin of the histogram
        :param observable: the observable to be analyzed
    """
    def __init__(self, name, minimal, maximum, n_bin, observable):
        self.min = Argument(name + "_min", np.float32(minimal))
        self.max = Argument(name + "_max", np.float32(maximum))
        self.n_bin = Argument(name + "_n_bin", np.int32(n_bin))
        self.value = Argument(name + "_value", cp.zeros(n_bin, dtype=cp.float32))
        self.observable = observable
        super().__init__(name, self.observable.input + [self.min, self.max, self.n_bin],
                         [self.value], [self.observable.output], temp_int = 1)

    @property
    def source_code(self):
        """
            The source code of the observable
        """
        return self.observable.source_code + [
            f"temp_int_0 = ({self.observable.output.name} - {self.min.use()}) / ({self.max.use()} - {self.min.use()}) * {self.n_bin.use()};",
            f"if (temp_int_0 >= 0 && temp_int_0 < {self.n_bin.use()})",
            r"{",
            f"    atomicAdd({self.value.name} + temp_int_0, local_weight);",
            r"}",
        ]
