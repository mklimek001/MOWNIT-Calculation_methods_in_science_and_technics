#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;


double exponentMinus1(double x){
    return exp(x) - 1;
}

double logExp(double x){
    return log(exp(x));
}


double y1(double x){
    return exponentMinus1(x)/x;
}


double y2(double x){
    return exponentMinus1(x)/logExp(x);
}



int main()
{
    double curr_x;
    
    for(int i = 1; i <= 15; i++){
        curr_x = pow(10,-i);
        cout<<setprecision(15)<<curr_x<<" "<<logExp(curr_x)<<" "<<exponentMinus1(curr_x)<<" "<<y1(curr_x)<<" "<<y2(curr_x)<<endl;
    }
    

    return 0;
}
