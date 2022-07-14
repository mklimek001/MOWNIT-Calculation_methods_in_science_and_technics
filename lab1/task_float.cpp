#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;


float exponentMinus1(float x){
    return expf(x) - 1;
}

float logExp(float x){
    return logf(expf(x));
}


float y1(float x){
    return exponentMinus1(x)/x;
}


float y2(float x){
    return exponentMinus1(x)/logExp(x);
}



int main()
{
    float curr_x;
    
    for(int i = 1; i <= 15; i++){
        curr_x = powf(10,-i);
        cout<<setprecision(6)<<curr_x<<" "<<logExp(curr_x)<<" "<<exponentMinus1(curr_x)<<" "<<y1(curr_x)<<" "<<y2(curr_x)<<endl;
    }
    

    return 0;
}
