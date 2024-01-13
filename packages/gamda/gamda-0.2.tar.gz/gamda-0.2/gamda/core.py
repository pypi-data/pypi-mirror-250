"""
    The basic functions of the package
"""
__all__ = ["gamda_logger", "Universe", "Argument", "FramewiseExecutor"]

import logging
import MDAnalysis as mda
import numpy as np
import cupy as cp

logging.basicConfig(level=logging.INFO, format='[%(asctime)s - gamda - %(levelname)s]\n%(message)s')
gamda_logger = logging.getLogger("gamda")

class Universe(mda.Universe):
    """
        a subclass of mda.Universe
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_map = {atom.id: i for i, atom in enumerate(self.atoms)}

    def get_dag(self, name, ag):
        """
            get the atom index of an mda.AtomGroup

            :param name: name of the AtomGroup in device
            :param ag: the mda.AtomGroup in host
        """
        if not isinstance(ag, mda.AtomGroup):
            raise TypeError(f"the type of the input should be mda.AtomGroup, but {type(ag)} got")
        array = cp.array([self._id_map.get(atom.id, -1) for atom in ag], dtype=cp.int32)
        return Argument(name, array)

class Argument:
    """
        The basic wrapper of arguments (input, output or medium) for others

        :param name: name of the argument
        :param var: the variable to be wrapped
    """
    names = set()
    def __init__(self, name, var):
        if name in self.names:
            raise ValueError(f"There have been an argument named {name}")
        if name.startswith("local") or name.startswith("temp"):
            raise ValueError(f"The name is not allowed to start with 'local' or 'temp' ({name})")
        self.name = name
        self.prefix_bold = None
        if isinstance(var, cp.ndarray):
            self.dim = len(var.shape)
            if var.dtype == cp.float32:
                self.prefix = "float*"
                self.prefix_bold = "float"
            elif var.dtype == cp.int32:
                self.prefix = "int*"
                self.prefix_bold = "int"
            else:
                raise TypeError(f"The data type of the input cupy array should be either \
cp.float32 or cp.int32, but {var.dtype} got")
            self.is_ptr = True
        elif isinstance(var, np.generic):
            self.dim = 0
            if var.dtype == np.float32:
                self.prefix = "float"
            elif var.dtype == np.int32:
                self.prefix = "int"
            else:
                raise TypeError(f"The data type of the input numpy scalar should be either \
np.float32 or np.float32, but {var.dtype} got")
        else:
            raise TypeError(f"The input var should be either \
a cupy array or a numpy generic, but {type(var)} got")
        self.names.add(name)
        self._var = var

    @property
    def var(self):
        """
            The variable to be wrapped
        """
        return self._var

    def declare(self):
        """
            Get the declaration string
        """
        return f"{self.prefix} {self.name}"

    def use(self):
        """
            Get the usage string
        """
        if self.prefix_bold:
            return f"local_{self.name}"
        return self.name

    def declare_local(self, index):
        """
            Get the local declaration string of the pointer

            :param index: the index for the pointer
        """
        if self.dim == 1:
            return f"{self.prefix_bold} local_{self.name} = {self.name}[{index}];"
        if self.dim == 2:
            return f"{self.prefix} local_{self.name} = {self.name} + {index}"
        return ""

    def __del__(self):
        if hasattr(self, "name"):
            self.names.discard(self.name)


class FramewiseExecutor:
    """
        The basic class of framewise excutor

        :param u: the gamda.Universe object
        :param dag: the length of main AtomGroup in device
        :param n_frame: the number of frame to be used for paralleling, 32 for default
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, u, dag, n_frame=32):
        if not isinstance(u, Universe):
            raise TypeError(f"The universe should be an gamda.Universe, but a {type(u)} got")
        self.u = u
        self.n_frame = Argument("n_frame", np.int32(n_frame))
        self.n_atom = Argument("n_atom", np.int32(len(u.atoms)))
        self._h_position = np.zeros((n_frame, len(u.atoms), 3), dtype=cp.float32)
        self._d_position = Argument("position", cp.array(self._h_position))
        self._h_weight = np.ones(n_frame, dtype=np.float32)
        self._d_weight = Argument("weight", cp.array(self._h_weight))
        self._tid = Argument("tid", np.int32(0))
        self._frame = Argument("frame", np.int32(0))
        self.weight_sum = cp.zeros(1, dtype=cp.float32)
        self._frame = 0
        self.dag = dag
        self._n_tid = Argument("n_tid", np.int32(len(dag.var)))
        self._analyzer = []
        self._input = []
        self._input_name = {}
        self._output = []
        self._output_name = {}
        self._midium = []
        self._midium_name = {}
        self.kernel = None

    def _compile(self):
        self.kernel = cp.RawKernel(self.source_code, "framewise_analyze")
        return self.kernel

    @property
    def readable_source_code(self):
        """
            The human-readable source code
        """
        src = ""
        for n_line, line in enumerate(self.source_code.split("\n")):
            src += f"{n_line + 1: >4d}| "
            temp_line = []
            for i in range(0, len(line), 120):
                temp_line.append(line[i: i + 120])
            src += "\n    | ".join(temp_line) + "\n"
        return src

    @property
    def source_code(self):
        """
            The source code
        """
        return r"""extern "C" __global__
void framewise_analyze(const int n_frame, const int n_tid, const int n_atom, const float* position, const float* weight%s%s)
{
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    int frame = threadIdx.y;
    if (tid < n_tid && frame < n_frame)
    {
        const float local_weight = weight[frame];
        const float* local_position = position + frame * n_atom * 3;
        %s%s
    }
}
""" %(self._get_inputs(), self._get_outputs(), self._get_declartions(), self._get_calculations())

    def _get_inputs(self):
        """ get input string """
        if self._input:
            return ", " + ", ".join([inp.declare() for inp in self._input])
        return ""

    def _get_outputs(self):
        """ get output string """
        if self._output:
            return ", " + ", ".join([out.declare() for out in self._output])
        return ""

    def _get_declartions(self):
        """ get declaration string """
        declarations = []
        max_temp_int = 0
        max_temp_float = 0
        if self._input:
            declarations += [inp.declare_local("tid") for inp in self._input if inp.dim > 0]
        if self._midium:
            declarations += [mid.declare() + ";" for mid in self._midium]
        for ana in self._analyzer:
            if ana.temp_int > max_temp_int:
                max_temp_int = ana.temp_int
            if ana.temp_float > max_temp_float:
                max_temp_float = ana.temp_float
        declarations += [f"int temp_int_{i};" for i in range(max_temp_int)]
        declarations += [f"float temp_float_{i};" for i in range(max_temp_float)]

        if declarations:
            return "\n        " + "\n        ".join(declarations) + "\n        "
        return ""

    def _get_calculations(self):
        """ get calculation string """
        src = []
        for ana in self._analyzer:
            src += ana.source_code
        if src:
            return "\n        " + "\n        ".join(src)
        return ""

    def add_analyzer(self, analyzer):
        """
            add an analyzer to the excutor

            :param analyzer: gamda.analyzer.Analyzer
        """
        self._analyzer.append(analyzer)
        for inp in analyzer.input:
            if inp.name not in self._input_name:
                self._input_name[inp.name] = len(self._input)
                self._input.append(inp)
        for out in analyzer.output:
            if out.name not in self._output_name:
                self._output_name[out.name] = len(self._output)
                self._output.append(out)
        for mid in analyzer.midium:
            if mid.name not in self._midium_name:
                self._midium_name[mid.name] = len(self._midium)
                self._midium.append(mid)

    def add_frame(self, positions, weight):
        """
            add a frame to the excutor

            :param positions: ts.positions
            :param weight: a float
        """
        self._h_position[self._frame, :, :] = positions
        self._h_weight[self._frame] = weight
        self._frame += 1
        if self._frame == self.n_frame.var:
            self.do_calculation()

    def do_calculation(self):
        """
            do calculation
        """
        if not self.kernel:
            self._compile()
        self._d_position.var.set(self._h_position)
        self._h_position[:] = 0
        self._d_weight.var.set(self._h_weight)
        self._h_weight[:] = 1
        block_x = 1024 // self.n_frame.var
        grid_x = (self._n_tid.var + block_x - 1) // block_x
        args = [self._frame, self._n_tid.var, self.n_atom.var,
                self._d_position.var, self._d_weight.var]
        args += [inp.var for inp in self._input]
        args += [out.var for out in self._output]
        try:
            self.kernel((grid_x,), (block_x, self.n_frame.var), args)
        except cp.cuda.compiler.CompileException as e:
            e.add_note(self.readable_source_code)
            raise e
        self._frame = 0
