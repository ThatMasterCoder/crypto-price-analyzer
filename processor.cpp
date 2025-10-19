#include <iostream>
#include <string>
#include <vector>
#include <map>


int main(){
    std::string word;
    std::map<std::string, int> wordCount;

    while (std::cin >> word)
        wordCount[word]++;

    for (const auto& pair : wordCount){
        std::cout << pair.first << ": " << pair.second << std::endl;
    }

    return 0;

}