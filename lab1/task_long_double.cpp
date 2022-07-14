#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

long double exponentMinus1(long double x){ return exp(x) - 1;}

long double logExp(long double x){ return log(exp(x));}

long double y1(long double x){ return exponentMinus1(x)/x;}

long double y2(long double x){ return exponentMinus1(x)/logExp(x);}


int main()
{
    long double curr_x;
    
    for(int i = 1; i <= 15; i++){
        curr_x = pow(10,-i);
        cout<<setprecision(18)<<curr_x<<" "<<logExp(curr_x)<<" "<<exponentMinus1(curr_x)<<" "<<y1(curr_x)<<" "<<y2(curr_x)<<endl;
    }
    
    return 0;
}
