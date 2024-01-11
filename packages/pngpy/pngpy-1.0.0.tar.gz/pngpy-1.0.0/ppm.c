#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <png.h>
#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include <python3.11/structmember.h>

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} PNGPixel;

typedef struct {
    PyObject_HEAD
    PyObject* width;
    PyObject* height;
    PNGPixel** pixels;
} PNGImage;

static void PNGImage_dealloc(PNGImage* self) {
    if(self->pixels) {
        size_t h = PyLong_AsSize_t(self->height);
        for(size_t y=0; y<h; y++)
            PyMem_Free(self->pixels[y]);
        PyMem_Free(self->pixels);
    }
    Py_XDECREF(self->width);
    Py_XDECREF(self->height);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* PNGImage_new(PyTypeObject* type, PyObject* args) {
    PNGImage* self;
    self = (PNGImage*)type->tp_alloc(type, 0);
    if(self) {
        self->width = PyLong_FromSize_t(0);
        if(!self->width) {
            Py_DECREF(self);
            return NULL;
        }
        self->height = PyLong_FromSize_t(0);
        if(!self->height) {
            Py_DECREF(self);
            return NULL;
        }
        self->pixels = NULL;
    }
    return (PyObject*)self;
}

static int PNGImage_init(PNGImage* self, PyObject* args) {
    PyObject* w = NULL, *h = NULL;

    if(!PyArg_ParseTuple(args, "OO", &w, &h))
        return -1;

    if(w&&h) {
        size_t _w = PyLong_AsSize_t(w);
        size_t _h = PyLong_AsSize_t(h);
        self->pixels = PyMem_Calloc(_h,sizeof(PNGPixel*));
        if(!self->pixels) return -1;
        for(size_t y=0; y<_h; y++) {
            self->pixels[y] = PyMem_Calloc(_w,sizeof(PNGPixel));
            if(!self->pixels[y]) return -1;
        }
        Py_XSETREF(self->width, Py_NewRef(w));
        Py_XSETREF(self->height, Py_NewRef(h));
    }

    return 0;
}

static struct PyMemberDef PNGImage_members [] = {
    {"width",  T_OBJECT_EX, offsetof(PNGImage, width), 0, "width"},
    {"height", T_OBJECT_EX, offsetof(PNGImage, height), 0, "height"},
    {NULL}
};

static PyObject* PNGImage_set(PNGImage* self, PyObject* args) {
    unsigned long x, y;
    unsigned long r, g, b;

    if(!PyArg_ParseTuple(args, "IIIkk", &r, &g, &b, &x, &y))
        return NULL;

    size_t w = PyLong_AsSize_t(self->width);
    size_t h = PyLong_AsSize_t(self->height);
    if(x >= w || y >= h) return NULL;

    self->pixels[y][x].r = r;
    self->pixels[y][x].g = g;
    self->pixels[y][x].b = b;

    Py_RETURN_NONE;
}

static PyObject* PNGImage_write_png(PNGImage* self, PyObject* args) {
    char* filename;

    if(!PyArg_ParseTuple(args, "s", &filename))
        return NULL;
    
    FILE* fp = fopen(filename, "wb");
    if(!fp) return NULL;

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if(!png) return NULL;

    png_infop info = png_create_info_struct(png);
    if(!info) Py_RETURN_NONE;

    if(setjmp(png_jmpbuf(png))) Py_RETURN_NONE;

    png_init_io(png, fp);

    size_t w = PyLong_AsSize_t(self->width);
    size_t h = PyLong_AsSize_t(self->height);

    png_set_IHDR(png, info, w, h, 8, PNG_COLOR_TYPE_RGB, PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT); 
    png_write_info(png, info);

    png_bytep* row = NULL;
    row = PyMem_Calloc(h, sizeof(png_bytep));
    for(size_t y=0; y<h; y++)
        row[y] = PyMem_Malloc(png_get_rowbytes(png,info));

    for(size_t y=0; y<h; y++) {
        png_bytep row_ = row[y];
        for(size_t x=0; x<w; x++) {
            png_bytep px = &(row_[x*3]);
            px[0] = self->pixels[y][x].r;
            px[1] = self->pixels[y][x].g;
            px[2] = self->pixels[y][x].b;
        }
    }

    png_write_image(png, row);
    png_write_end(png, NULL);

    for(size_t y=0; y<h; y++)
        PyMem_Free(row[y]);
    PyMem_Free(row);

    fclose(fp);
    png_destroy_write_struct(&png, &info);

    Py_RETURN_NONE;
}

static PyMethodDef PNGImage_methods[] = {
    {"set", (PyCFunction)PNGImage_set, METH_VARARGS, "Set pixel RGB at X, Y"},
    {"write_png", (PyCFunction)PNGImage_write_png, METH_VARARGS, "Write image to PNG"},
    {NULL}
};

static PyTypeObject PNGImageType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "png.Image",
    .tp_doc = PyDoc_STR("Image Data"),
    .tp_basicsize = sizeof(PNGImage),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = (newfunc)PNGImage_new,
    .tp_init = (initproc)PNGImage_init,
    .tp_dealloc = (destructor)PNGImage_dealloc,
    .tp_members = PNGImage_members,
    .tp_methods = PNGImage_methods,
};

static PyModuleDef png_module = {
    PyModuleDef_HEAD_INIT,
    "png",
    "Simple libpng image writing interface",
    -1,
};

PyMODINIT_FUNC PyInit_png(void) {
    PyObject* m;
    if(PyType_Ready(&PNGImageType) < 0) return NULL;
    m = PyModule_Create(&png_module);
    if(!m) return NULL;
    if(PyModule_AddObjectRef(m, "Image", (PyObject*)&PNGImageType) < 0) {
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
