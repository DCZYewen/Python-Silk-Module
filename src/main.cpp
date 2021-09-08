#include <pybind11/pybind11.h>
#define NO_ASM
#include "codec.h"
#include <cstdlib>
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
#include <iostream>
#include <cstdio>

class dataItem
{
public:
    std::vector<unsigned char> v_data;
    dataItem() {
    }
    ~dataItem() {
    }

    void writeData(void* p, int len) {
        for (int i = 0; i < len; i++){
            v_data.push_back( ((unsigned char*)p)[i] );
        }
        return;
    }
};


void* codecCallback(void* userdata, unsigned char* p, int len){
    auto ud = (dataItem*)userdata;
    ud->writeData(userdata , len);
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
        unsigned char* data = (unsigned char*)malloc(buf_size);
        memcpy(data , s_data.c_str() , buf_size);
        dataItem di = dataItem();
        int ret = silkDecode(data , buf_size, sampleRate, codecCallback, (void*)&di);
        free(data);
        if(!ret) {
            char error[1];
            error[0] = '\0';
            return py::bytes(error);
        }else{
            auto p = di.v_data.data();
            std::string ret_val( (char *)p , di.v_data.size() );
            return py::bytes(ret_val);
        }

    },py::arg("Stream") , py::arg("SampleRate") , R"pbdoc(
        To call this function, the first param should be a bytes, which
        refers to the data stream to be Decoded. The second should be
        the samplerate of demand.
    )pbdoc");

    m.def("silkEncode",[](py::bytes rdata , int sampleRate){
        std::string s_data(rdata);
        int buf_size = s_data.length()*sizeof(unsigned char);
        unsigned char* data = (unsigned char*)malloc(buf_size);
        memcpy(data , s_data.c_str() , buf_size);
        dataItem di = dataItem();
        int ret = silkEncode(data , buf_size, sampleRate, codecCallback, (void*)&di);
        free(data);
        if(!ret) {
            char error[1];
            error[0] = '\0';
            return py::bytes();
        }else{
            auto p = di.v_data.data();
            std::string ret_val( (char *)p , di.v_data.size() );
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