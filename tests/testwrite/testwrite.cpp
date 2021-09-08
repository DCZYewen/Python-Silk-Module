#include <vector>
#include <iostream>
#include <stdio.h>
#include <string>
#include <stdlib.h>

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

    friend std::ostream& operator<<(std::ostream& os, const dataItem& di);
};

std::ostream& operator<<(std::ostream& os , const dataItem &di){
    for (auto iter = di.v_data.begin() ; iter < di.v_data.end() ; iter++){
        printf("%c" , *iter);
    }
    return os;
}

int main (void){
    auto data = dataItem();
    char *p = "This is very good.";
    std::string t_p(p ,19);
    for (std::size_t i = 0 ; i < 19 ; i++){
        data.writeData(p , 1);
        p += 1;
    }
    std::cout << data << std::endl;
    std::cout << t_p  << std::endl;
    std::string val((char*)data.v_data.data() , data.v_data.size());
    std::cout << val  << std::endl;
    return 0;
}