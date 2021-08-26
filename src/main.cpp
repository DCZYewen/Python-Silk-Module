#include <pybind11/pybind11.h>
#define NO_ASM
#include "codec.h"
#include <cstdlib>
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

void codecCallback(void* userdata, unsigned char* p, int len){
    int datalen = sizeof(unsigned char)*len;
    userdata = (unsigned char *)PyMem_RawRealloc(userdata , datalen + sizeof(int));
    memcpy_s(userdata , datalen , p , datalen);
    auto t = (unsigned char*)userdata;
    t[datalen+1]='\0';
    return;
}

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

    } , R"pbdoc(
        To call this function, the first param should be a bytes, which
        refers to the data stream to be Decoded. The second should be
        the samplerate of demand.
    )pbdoc");

    m.def("silkEncode",[](py::bytes rdata , int sampleRate){
        std::string s_data(rdata);
        int buf_size = s_data.length()*sizeof(unsigned char);
        unsigned char* data = (unsigned char*)PyMem_RawMalloc(buf_size + 1);
        unsigned char* result = (unsigned char*)PyMem_RawMalloc(1<<4);
        memcpy_s(data , buf_size +1 , s_data.c_str() , buf_size );
        int ret = silkEncode(data , buf_size, sampleRate, codecCallback, result);
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

    } , R"pbdoc(
        To call this function, the first param should be a bytes, which
        refers to the data stream to be Decoded. The second should be
        the samplerate of demand.
    )pbdoc");
    
#define VERSION_INFO "0.0.1"

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}

/*
Legal issues and opensource licenses see LICENSE file.
*/