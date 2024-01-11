#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include "Python.h"
#include "numpy/arrayobject.h"
#include "map"
#include "string"

struct Array
{
    int size = 0;
    void* d_values = NULL;
    PyObject* np_array = NULL;
    void* h_values = NULL;
    int modified_status = 0;
};

static std::map<std::string, Array> FloatArrays;

static PyObject* _malloc_float(PyObject* self, PyObject* args)
{
    char* name;
    PyArrayObject* input_array;
    if (!PyArg_ParseTuple(args, "sO!", &name, &PyArray_Type, &input_array))
    {
        PyErr_SetString(PyExc_TypeError, "The input array should be a numpy array");
        return NULL;
    }
    if (PyArray_TYPE(input_array) != NPY_FLOAT)
    {
        PyErr_SetString(PyExc_TypeError, "Input array must be of type float.");
        return NULL;
    }
    float* in_data = static_cast<float*>(PyArray_DATA(input_array));
    npy_intp size = PyArray_SIZE(input_array);

    PyObject* output_array = PyArray_SimpleNew(1, &size, NPY_FLOAT);
    float* out_data = static_cast<float*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(output_array)));
    PyArray_CLEARFLAGS(reinterpret_cast<PyArrayObject*>(output_array), NPY_WRITEABLE);

    FloatArrays[name] = Array();
    Array* array = &FloatArrays[name];
    array->h_values = (void*)out_data;
    array->np_array = output_array;
    cudaMalloc(&array->d_values, sizeof(float) * size);
    cudaMemcpy(array->d_values, array->h_values, sizeof(float) * size, cudaMemcpyHostToDevice);

    return output_array;
}

static PyObject* _free_float(PyObject* self, PyObject* args)
{
    char* name;
    if (!PyArg_ParseTuple(args, "s", &name))
    {
        return NULL;
    }

    Array* array = &FloatArrays[name];
    Py_DECREF(array->np_array);
    cudaFree(array->d_values);

    return Py_BuildValue("");
}

static PyMethodDef GamdaMethod[] =
{
    {"_malloc_float",(PyCFunction)_malloc_float, METH_VARARGS, ""},
    {"_free_float",(PyCFunction)_free_float, METH_VARARGS, ""},
    {NULL,NULL,0,NULL}
};

static PyModuleDef GamdaModule = 
{
    PyModuleDef_HEAD_INIT, "_gamda", NULL, -1, GamdaMethod,
    NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__gamda(void)
{
    import_array();
    return PyModule_Create(&GamdaModule);
}