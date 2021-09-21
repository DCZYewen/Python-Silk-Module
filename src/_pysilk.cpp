#include <pybind11/pybind11.h>
#include <cstdlib>
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
#include <iostream>
#include <vector>
#include <new.h>
#include "codec.h"
#include "../ThreadPool/ThreadPool.h"

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
            v_data.push_back( *((unsigned char*)p + i) );
        }
        return;
    }
    const void* getData(){
        const  void *p = v_data.data();
        return p;
    }
    const std::size_t getDataLen(){
        return v_data.size();
    }

    const void printVec(){
        for( auto iter :v_data){
            printf("%c" , iter);
        }
        return;
    }
};


void* codecCallback(void* userdata, unsigned char* p, int len){
    auto ud = (dataItem*)userdata;
    ud->writeData(p , len);
    return userdata;
}//Debug flag: No errors

namespace py = pybind11;

auto Decode_Lambda = [](py::bytes rdata , int sampleRate){
        py::gil_scoped_release release;
        std::string s_data(rdata);
        int buf_size = s_data.length()*sizeof(unsigned char);
        unsigned char* data = (unsigned char*)malloc(buf_size);
        memcpy(data , s_data.c_str() , buf_size);
        dataItem di = dataItem();
        int ret = silkDecode(data , buf_size, sampleRate, codecCallback, (void*)&di);
        free(data);
        py::gil_scoped_acquire acquire;
        if(!ret) {
            char error[1];
            error[0] = '\0';
            return py::bytes(error);
        }else{
            //std::string ret_val( (char*)di.getData() , di.getDataLen() );
            return py::bytes((char*)di.getData() , di.getDataLen());
        }

    };

auto Encode_Lambda = [](py::bytes rdata , int sampleRate){
        py::gil_scoped_release release;
        std::string s_data(rdata);
        int buf_size = s_data.length()*sizeof(unsigned char);
        unsigned char* data = (unsigned char*)malloc(buf_size);
        memcpy(data , s_data.c_str() , buf_size);
        dataItem di = dataItem();
        int ret = silkEncode(data , buf_size, sampleRate, codecCallback, (void*)&di);
        free(data);
        py::gil_scoped_acquire acquire;
        if(!ret) {
            char error[1];
            error[0] = '\0';
            return py::bytes();
        }else{
            return py::bytes((char*)di.getData() , di.getDataLen());
        }

    };

PYBIND11_MODULE(_pysilk, m) {
    m.doc() = R"pbdoc(
        Python silk decode/encoder bindings using pybind11
        -----------------------

        .. currentmodule:: _pysilk

        .. autosummary::
           :toctree: _generate

        Many thanks to the silk SDK and libSilkCodec.
        I modified some of the code to make it compatible as python module.
        License is appended to the LICENSE file of the github repo.

        Author:  DCZYewen
        Contact: contact@basicws.net
    )pbdoc";
    std::size_t threads;
    ThreadPool* pool = (ThreadPool*)malloc(sizeof(ThreadPool));

    m.def("silkAsyncConf", [&threads , &pool](int t_count){
    //capture variables to configure the library.
        threads = t_count;
        new(pool)ThreadPool(threads);//placement new
        return 0;
    } , py::arg("Configures threads in thread pool."), R"pbdoc(
        Call this fuction to configure the threads
        quantity used in the internal thread pool.
    )pbdoc");

    m.def("silkAsyncTerminate", [&pool](){
        pool->~ThreadPool();
        free(pool);
        return 0;
    } , R"pbdoc(
        Call this function to destruct everyting,
        if any async call is performed, the program
        will crash.
    )pbdoc");

    m.def("silkAsyncEncode", [&pool](py::bytes rdata , int sampleRate){
        py::gil_scoped_release release;
        auto result = pool->enqueue(Encode_Lambda(rdata , sampleRate));
        auto p_res = &result;
        py::gil_scoped_acquire acquire;
        return py::bytes((char*)p_res , sizeof(p_res));
    });

    m.def("silkAsnycDecode", [&pool](py::bytes rdata , int sampleRate){
        py::gil_scoped_release release;
        auto result = pool->enqueue(Decode_Lambda(rdata , sampleRate));
        auto p_res = &result;
        py::gil_scoped_acquire acquire;
        return py::bytes((char*)p_res , sizeof(p_res));
    });

    m.def("waitResult", [&pool](py::bytes result){
        std::string s_data(result);
        char* buf = (char*)malloc(sizeof(char) * s_data.length());
        memcpy_s(buf , sizeof(char) * s_data.length(),
        s_data.c_str() , sizeof(char) * s_data.length());
        auto p_res = (std::future<pybind11::object>*) buf;
        return p_res->get();
    });

    m.def("silkDecode", Decode_Lambda ,py::arg("Stream") , py::arg("SampleRate") , R"pbdoc(
        To call this function, the first param should be a bytes, which
        refers to the data stream to be Decoded. The second should be
        the samplerate of demand.
    )pbdoc");

    m.def("silkEncode", Encode_Lambda ,py::arg("Stream") , py::arg("SampleRate") , R"pbdoc(
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