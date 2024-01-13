"""
    The subpackage to manage observables
"""

from .. import Argument

class Observable:
    """
        The class of the observable

        :param name: the name of the observable
    """
    names = set()
    def __init__(self, name):
        self.name = name
        self.input = []
        self.output = None
        self.names.add(name)

    @property
    def source_code(self):
        """
            The source code of the observable
        """
        raise NotImplementedError

    def __del__(self):
        if hasattr(self, "name"):
            self.names.discard(self.name)


#pylint: disable=too-few-public-methods
class SingleAtomObservable(Observable):
    """
        The subclass of the observable which only relies on one atom

        :param name: the name of the observable
        :param in_arg: the input argument (cp.array, which is mda.AtomGroup in device)
        :param out_arg: the output argument (np.float32)
    """
    def __init__(self, name, in_arg, out_arg):
        super().__init__(name)
        if not isinstance(in_arg, Argument):
            raise TypeError(f"in_arg should be a gamda.Argument, but a {type(in_arg)} got")
        if not isinstance(out_arg, Argument):
            raise TypeError(f"out_arg should be a gamda.Argument, but a {type(out_arg)} got")
        if in_arg.prefix not in ("int*",):
            raise TypeError("in_arg should be a cupy array of int32")
        if out_arg.prefix not in ("float"):
            raise TypeError("out_arg should be a numpy generic of float32")
        self.input.append(in_arg)
        self.output = out_arg
        self._definition = None

    @property
    def source_code(self):
        return [self._definition.format(OUTPUT=self.output.use(), INPUT=self.input[0].use())]


class PositionZ(SingleAtomObservable):
    """
        The coordinate of position Z
    """
    def __init__(self, name, in_arg, out_arg):
        super().__init__(name, in_arg, out_arg)
        self._definition = "{OUTPUT} = local_position[{INPUT} * 3 + 2];"


class PositionY(SingleAtomObservable):
    """
        The coordinate of position Y
    """
    def __init__(self, name, in_arg, out_arg):
        super().__init__(name, in_arg, out_arg)
        self._definition = "{OUTPUT} = local_position[{INPUT} * 3 + 1];"


class PositionX(SingleAtomObservable):
    """
        The coordinate of position X
    """
    def __init__(self, name, in_arg, out_arg):
        super().__init__(name, in_arg, out_arg)
        self._definition = "{OUTPUT} = local_position[{INPUT} * 3];"
