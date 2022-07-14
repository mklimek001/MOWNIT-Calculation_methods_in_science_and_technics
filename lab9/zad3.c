#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <float.h>


#define BILLION  1000000000.0;
int Digs = FLT_DECIMAL_DIG;


int main(int argc, char* argv[])
{
    int i,j,k;
    int size = atoi(argv[1]);
    double factors[size][size];
    double x_vector[size];
    double result[size];
    double calculeted_x_vector[size];
    double operation_matrix[size][size+1];


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

    for(i = 0; i < size; i++){
        for(j = 0; j < size; j++){
            operation_matrix[i][j] = factors[i][j];
        }
        operation_matrix[i][size] = result[i];
    }

    int op_size = size+1;

    double multiplier, new_val;
    for(i = 0; i < size - 1; i++){
        for(j = i+1; j < size; j++){
            multiplier = operation_matrix[j][i]/operation_matrix[i][i];
            //printf("%d, %d, %f\n", j,i,multiplier);
            for(k = i; k<op_size; k++){
                new_val = operation_matrix[j][k] - (operation_matrix[i][k]*multiplier);
                operation_matrix[j][k] = new_val;
            }
        }
    }

    for(i = size-1; i >= 0; i--){
        curr_sum = operation_matrix[i][size];
        for(j = i+1; j < size; j++){
            curr_sum -= operation_matrix[i][j]*calculeted_x_vector[j];
        }
        calculeted_x_vector[i] = curr_sum/operation_matrix[i][i];
    }

    if(clock_gettime( CLOCK_REALTIME, &stop) == -1 ) {
        perror( "clock gettime" );
        exit( EXIT_FAILURE );
    }

    accum = ( stop.tv_sec - start.tv_sec ) + ( stop.tv_nsec - start.tv_nsec )/BILLION;

    double errors_sum = 0.0;
    double max_error = 0.0;
    for(i = 0; i < size; i++){
        errors_sum += fabs(calculeted_x_vector[i] - x_vector[i]);
        if(fabs(calculeted_x_vector[i] - x_vector[i]) > max_error){
            max_error = fabs(calculeted_x_vector[i] - x_vector[i]);
        }
    }

    printf("GAUSS\n");
    printf("Metryka 1 : %.*e\n", Digs, errors_sum);
    printf("Metryka 2 : %.*e\n", Digs, max_error);
    printf("Time : %f\n", accum);

    return 0;
}

