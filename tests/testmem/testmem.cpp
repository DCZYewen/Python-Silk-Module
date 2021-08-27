#include <iostream>
#include <cstdio>
using namespace std;
#include <cstdlib>
#include <cstring>

struct dataItem
{
public:
    int buffer_size;
    int current_pos;
    unsigned char* data;
    dataItem(){
        data = (unsigned char*)malloc(1<<12);
        buffer_size = 1<<12;
        current_pos = 0;
        cout << "excuted" << endl;
    }
    ~dataItem(){
        free(data);
    }
    void extendData(int n){
        printf("Before %p\n" , data);
        auto ndata = (unsigned char*)malloc(buffer_size + n + (1<<12));
        printf("data %p ndata %p\n" , data , ndata);
        memcpy_s(ndata , current_pos , data , current_pos);
        free(data);
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

int main(void){
    dataItem di = dataItem();
    for (int i = 0 ; i < 100 ; i++){
        di.extendData(200);
        cout << di << endl;
    }
    return 0;
}