#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <iomanip>


int main(){
    std::string coin;
    double initial_price, latest_price;


    while (std::cin >> coin >> initial_price >> latest_price) {
        double change = latest_price - initial_price;
        double change_percent = (change / initial_price) * 100.0;

        
        int precision;
        if (initial_price < 0.01) {
            precision = 8;
        } else if (initial_price < 0.1) {
            precision = 6;
        } else if (initial_price < 10) {
            precision = 4;
        } else {
            precision = 2;
        }

        

        std::cout << std::setprecision(precision) << std::fixed 
                << "Name: " << coin 
                << ", Last Price: $" << initial_price 
                << ", Latest Price: $" << latest_price 
                << ", Change: $" << change 
                << std::setprecision(3)
                << ", Change (%): " << change_percent << "%" 
            << std::endl;
    }

    return 0;
}