#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <float.h>

#define BILLION  1000000000.0;
int Digs = FLT_DECIMAL_DIG;

int main(int argc, char* argv[])
{
    int i,j;
    int size = atoi(argv[1]);
    double factors[size][size];
    double x_vector[size];
    double result[size];
    double calculeted_x_vector[size];
    double beta[size];
    double gamma[size];
    double a,b,c,d;

    for(int i = 0; i < size; i++){
        x_vector[i] = 1.0;
    }

    for(i = 0; i < size; i++){
        for(j = 0; j < size; j++){
            if(j == i){
                factors[i][j] = 6;
            } else if (j == i+1){
                factors[i][j] = 1.0/(i+4);
            } else if (j == i - 1){
                factors[i][j] = 6.0/(i+5);
            } else {
                factors[i][j] = 0;
            }
        }
    }

    /*
    for(i = 0; i < size; i++){
        for(j = 0; j < size; j++){
            printf("%f ", factors[i][j]);
        }
        printf("\n");
    }
    */

    double curr_sum;

    for(i = 0; i < size; i++){
        curr_sum = 0.0;
        for(j = 0; j < size; j++){
            curr_sum += factors[i][j] * x_vector[j];
        }
        result[i] = curr_sum;
    }

    struct timespec start, stop;
    double accum;

    if(clock_gettime( CLOCK_REALTIME, &start) == -1) {
        perror( "clock gettime" );
        exit( EXIT_FAILURE );
    }

    b = factors[0][0];
    c = factors[0][1];
    d = result[0];

    beta[0] = -c/b;
    gamma[0] = d/b;

    for(i = 1; i<size - 1; i ++){
        a = factors[i][i-1];
        b = factors[i][i];
        c = factors[i][i+1];
        d = result[i];
        beta[i] = -c/(a*beta[i-1] + b);
        gamma[i] = (d - a*gamma[i-1])/(a*beta[i-1] + b);
    }

    beta[size-1] = 0;
    a = factors[size-1][size-2];
    b = factors[size-1][size-1];
    d = result[size-1];
    gamma[size-1] = (d - a*gamma[size-2])/(a*beta[size-2] + b);

    calculeted_x_vector[size-1] = gamma[size-1];

    for(i = size-2; i >= 0; i--){
        calculeted_x_vector[i] = beta[i]*calculeted_x_vector[i+1] + gamma[i];
    }

    if(clock_gettime( CLOCK_REALTIME, &stop) == -1 ) {
        perror( "clock gettime" );
        exit( EXIT_FAILURE );
    }

    accum = ( stop.tv_sec - start.tv_sec ) + ( stop.tv_nsec - start.tv_nsec )/BILLION;

    double errors_sum = 0.0;
    double max_error = 0.0;
    printf("%d\n", size);
    for(i = 0; i < size; i++){
        errors_sum += fabs(calculeted_x_vector[i] - x_vector[i]);
        if(fabs(calculeted_x_vector[i] - x_vector[i]) > max_error){
            max_error = fabs(calculeted_x_vector[i] - x_vector[i]);
        }
    }

    printf("THOMAS\n");
    printf("Metryka 1 : %.*e\n", Digs, errors_sum);
    printf("Metryka 2 : %.*e\n", Digs, max_error);
    printf("Time : %f\n", accum);

    return 0;
}

