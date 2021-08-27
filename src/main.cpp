#include <pybind11/pybind11.h>
#define NO_ASM
#include "codec.h"
#include <cstdlib>
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
#include <iostream>
#include <cstdio>

struct dataItem
{
public:
    int buffer_size;
    int current_pos;
    unsigned char* data;
    dataItem(){
        data = (unsigned char*)PyMem_Malloc(1<<12);
        buffer_size = 1<<12;
        current_pos = 0;
    }
    ~dataItem(){
        free(data);
    }
    void extendData(int n){
        printf("Before %p\n" , data);
        auto ndata = (unsigned char*)PyMem_Malloc(buffer_size + n + (1<<12));
        printf("data %p ndata %p\n" , data , ndata);
        memcpy_s(ndata , current_pos , data , current_pos);
        PyMem_Free(data);
        data = ndata;
        printf("After  %p\n" , data);

        buffer_size += (n+(1<<12));
    }

    friend std::ostream& operator<<(std::ostream& os, const dataItem& di);
};    

std::ostream& operator<<(std::ostream& os , const dataItem& di){
    os << "Buffer Size:" << di.buffer_size << " Current Pos:" << di.current_pos<<
    " Data Pointer:" << reinterpret_cast<const void *>(di.data);
    return os;
};


void* codecCallback(void* userdata, unsigned char* p, int len){
    auto ud = (dataItem*)userdata;
    if(ud->current_pos + len > ud->buffer_size){
        ud->extendData(len);
    }
    ud->current_pos += len;
    memcpy_s(ud->data + ud->current_pos, len , p , len);
    return userdata;
}//Debug flag: No errors

namespace py = pybind11;

PYBIND11_MODULE(pysilk, m) {
    m.doc() = R"pbdoc(
        Python silk decode/encoder bindings using pybind11
        -----------------------

        .. currentmodule:: pysilk

        .. autosummary::
           :toctree: _generate

        Many thanks to the silk SDK and libSilkCodec.
        I modified some of the code to make it compatible as python module.
        License is appended to the LICENSE file of the github repo.

        Author:  DCZYewen
        Contact: contact@basicws.net
    )pbdoc";

    m.def("silkDecode",[](py::bytes rdata , int sampleRate){
        std::string s_data(rdata);
        int buf_size = s_data.length()*sizeof(unsigned char);
        unsigned char* data = (unsigned char*)PyMem_RawMalloc(buf_size + 1);
        unsigned char* result = (unsigned char*)PyMem_RawMalloc(1<<4);
        memcpy_s(data , buf_size +1 , s_data.c_str() , buf_size );
        int ret = silkDecode(data , buf_size, sampleRate, codecCallback, result);
        PyMem_RawFree(data);
        if(!ret) {
            PyMem_RawFree(result);
            char error[1];
            error[0] = '\0';
            return py::bytes();
        }else{
            std::string ret_val( (char*)result );
            PyMem_RawFree(result);
            return py::bytes(ret_val);
        }

    } , py::arg("Stream") , py::arg("SampleRate") , R"pbdoc(
        To call this function, the first param should be a bytes, which
        refers to the data stream to be Decoded. The second should be
        the samplerate of demand.
    )pbdoc");

    m.def("silkEncode",[](py::bytes rdata , int sampleRate){
        std::string s_data(rdata);
        int buf_size = s_data.length()*sizeof(unsigned char);
        unsigned char* data = (unsigned char*)PyMem_Malloc(buf_size + 1);
        dataItem di = dataItem();
        memcpy_s(data , buf_size +1 , s_data.c_str() , buf_size );
        int ret = silkEncode(data , buf_size, sampleRate, codecCallback, (void*)&di);
        PyMem_Free(data);
        if(!ret) {
            char error[1];
            error[0] = '\0';
            return py::bytes();
        }else{
            std::string ret_val( (char*)(di.data) );
            return py::bytes(ret_val);
        }

    },py::arg("Stream") , py::arg("SampleRate") , R"pbdoc(
        To call this function, the first param should be a bytes, which
        refers to the data stream to be Decoded. The second should be
        the samplerate of demand.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}

/*
Legal issues and opensource licenses see LICENSE file.
*/