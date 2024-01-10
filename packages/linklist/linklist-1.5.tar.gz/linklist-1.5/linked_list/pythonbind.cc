#include <Python.h>
#include "ost.hh"

namespace port { 

    struct DefaultAllocator {
        template <typename T> 
        T *operator() () {
            return (T *) malloc(sizeof (T)); 
        }
    }; 
    struct DefaultDeallocator {
        void operator() (auto ptr) {
            free(ptr); 
        }
    }; 

    const char *out_of_range = "list index out of range";
    const char *aout_of_range = "list assignment index out of range"; 

    struct LinkedList {
        PyObject_HEAD
        ost::WBT<PyObject *> list; 
    }; 

    int init(LinkedList *self, PyObject *args, PyObject *kwds) {
        self->list.root = nullptr; 
        return 0; 
    }
    void destruct(LinkedList *self) {
        ost::destroy(&self -> list, [](auto node) {
            PyObject *obj = node -> value; 
            Py_DECREF(obj); 
            free(node); 
        });
    }

    PyObject *getitem(LinkedList *self, Py_ssize_t index) {
        // handle as reversed.. 
        Py_ssize_t list_size = ost::size(&self->list); 
        PyObject *rst; 
        if (index >= list_size || index < 0) {
            PyErr_SetString(PyExc_IndexError, out_of_range); 
            return nullptr; 
        } 
        rst = ost::query(&self -> list, (size_t ) index); 
        Py_INCREF(rst);
        return rst; 
    }
    int setitem(LinkedList *self, Py_ssize_t index, PyObject *val) {
        Py_ssize_t list_size = ost::size(&self->list);
        if (index >= list_size || index < 0) {
            PyErr_SetString(PyExc_IndexError, aout_of_range); 
            return -1; 
        } 
        auto tmp = ost::query_impl(&self -> list, self->list.root, (size_t ) index); 
        Py_DECREF(tmp -> value); 
        if (val != nullptr) {
            Py_INCREF(val);
            tmp -> value = val;  
        } else {
            ost::delete_impl(&self->list, tmp, (PyObject **) nullptr, DefaultDeallocator {}); 
        }
        return 0; 
    }

    PyTypeObject LinkedListType = {
        PyVarObject_HEAD_INIT(nullptr, 0)
        "linked_list.linked_list",
        sizeof (LinkedList),
        0, 
    }; 

    PyObject *append(LinkedList *self, PyObject *args) {
        PyObject *obj; 
        if (!PyArg_ParseTuple(args, "O", &obj)) {
            return nullptr; 
        }
        Py_INCREF(obj); 
        // ost::insert(&self -> list, obj); 
        ost::insert_last(&self -> list, obj, DefaultAllocator {}); 
        Py_RETURN_NONE; 
    } 
    PyObject *append_left(LinkedList *self, PyObject *args) {
        PyObject *obj; 
        if (!PyArg_ParseTuple(args, "O", &obj)) {
            return nullptr; 
        }
        Py_INCREF(obj); 
        ost::insert_first(&self -> list, obj, DefaultAllocator {}); 
        Py_RETURN_NONE; 
    }
    PyObject *insert(LinkedList *self, PyObject *args) {
        PyObject *obj; 
        Py_ssize_t index, len; 
        if (!PyArg_ParseTuple(args, "nO", &index, &obj)) {
            return nullptr; 
        }
        len = ost::size(&self -> list);
        if (index < 0) {
            index += len + 1; 
        }
        if (index < 0 || index > len) {
            PyErr_SetString(PyExc_IndexError, out_of_range); 
            return nullptr; 
        }
        Py_INCREF(obj); 
        ost::insert(&self -> list, (size_t ) index, obj, DefaultAllocator {}); 
        Py_RETURN_NONE; 
    }

    const char *pop_error = "pop from empty list"; 
    PyObject *pop(LinkedList *self, PyObject *args) {
        size_t len = ost::size(&self->list); 
        if (len == 0) {
            PyErr_SetString(PyExc_IndexError, pop_error); 
            return nullptr; 
        }
        PyObject *rst; 
        ost::delete_last(&self -> list, &rst, DefaultDeallocator {}); 
        return rst; 
    }
    PyObject *pop_left(LinkedList *self, PyObject *args) {
        size_t len = ost::size(&self->list); 
        if (len == 0) {
            PyErr_SetString(PyExc_IndexError, pop_error); 
            return nullptr; 
        }
        PyObject *rst; 
        ost::delete_first(&self -> list, &rst, DefaultDeallocator {}); 
        return rst; 
    }

    PyMethodDef methods[] = {
        // {"__get_item__", (PyCFunction ) getitem, METH_VARARGS, nullptr }, 
        { "append", (PyCFunction ) append, METH_VARARGS, nullptr }, 
        { "appendleft", (PyCFunction ) append_left, METH_VARARGS, nullptr }, 
        { "insert", (PyCFunction ) insert, METH_VARARGS, nullptr }, 
        { "pop", (PyCFunction ) pop, METH_VARARGS, nullptr }, 
        { "popleft", (PyCFunction ) pop_left, METH_VARARGS, nullptr }, 
        { nullptr } 
    }; 
    Py_ssize_t len(LinkedList *self) {
        return ost::size(&self -> list);  
    }
    PySequenceMethods list_methods = {
        (lenfunc ) len, 
        0, 
        0, 
        (ssizeargfunc ) getitem, 
        0, 
        // (objobjargproc ) setitem, 
        (ssizeobjargproc ) setitem, 
        0, 
        0, 
        0, 
        0, 
    }; 
    PyModuleDef this_module = {
        PyModuleDef_HEAD_INIT,
        "linked_list", 
        nullptr, 
        -1, 
        nullptr, 
        nullptr, 
        nullptr, 
        nullptr,
        nullptr,
    }; 
}

extern "C" {

    PyMODINIT_FUNC PyInit_linked_list() {
        // return PyModule_Create(&examplemodule); 
        PyObject *m; 
        port::LinkedListType.tp_new = PyType_GenericNew; 
        port::LinkedListType.tp_init = (initproc ) port::init; 
        port::LinkedListType.tp_dealloc = (destructor ) port::destruct; 
        port::LinkedListType.tp_as_sequence = &port::list_methods; 
        port::LinkedListType.tp_methods = port::methods; 
        if (PyType_Ready(&port::LinkedListType) < 0) {
            return nullptr; 
        }
        m = PyModule_Create(&port::this_module); 
        if (m == nullptr) return m; 
        Py_INCREF(&port::LinkedListType); 
        PyModule_AddObject(m, "linked_list", (PyObject *) &port::LinkedListType);
        return m; 
    }

}