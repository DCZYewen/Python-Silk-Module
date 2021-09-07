#include <iostream>
#include <cstdio>
using namespace std;
#include <cstdlib>
#include <vector>
#include <cstring>
class dataItem
{
public:
    int buffer_size;
    int current_pos;
    unsigned char* data;
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

    friend std::ostream& operator<<(std::ostream& os, const dataItem& di);
};

std::ostream& operator<<(std::ostream& os, const dataItem& di) {
    os << "Buffer Size:" << di.buffer_size << " Current Pos:" << di.current_pos <<
        " Data Pointer:" << reinterpret_cast<const void*>(di.data);
    return os;
};

int main(void) {
    dataItem di = dataItem();
    char* p = (char*)malloc(sizeof(char) * 4096);
    srand(123213);
    for (int i = 0; i < 4096 / sizeof(int); i++) {
        auto t = (int*)p;
        t[i] = rand();
    }
    for (int i = 0; i < 100; i++) {
        auto t = rand()%4000;
        printf("current_eof:%d new random:%d\n", di.current_pos, t);
        di.writeData(p, t);
        cout << di << endl;
    }
    return 0;
}