#include <stdio.h>
#include <stdlib.h>
#include <math.h>


int main(int argc, char* argv[])
{
    int i,j,k;
    int size = atoi(argv[1]);
    float factors[size][size];
    float x_vector[size];
    float result[size];
    float calculeted_x_vector[size];

    for(int i = 0; i < size; i++){
        x_vector[i] = 1.0;
        factors[0][i] = 1.0;
    }

    for(i = 1; i < size; i++){
        for(j = 0; j < size; j++){
            factors[i][j] = 1.0/(i+j+1);
        }
    }

    float curr_sum;

    for(i = 0; i < size; i++){
        curr_sum = 0.0;
        for(j = 0; j < size; j++){
            curr_sum += factors[i][j] * x_vector[j];
        }
        result[i] = curr_sum;
    }

    float operation_matrix[size][size+1];

    for(i = 0; i < size; i++){
        for(j = 0; j < size; j++){
            operation_matrix[i][j] = factors[i][j];
        }
        operation_matrix[i][size] = result[i];
    }

    int op_size = size+1;

    float multiplier, new_val;
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

    float errors_sum = 0.0;
    printf("[FLOAT] Uzyskany wynik dla %d zmiennych : ", size);
    for(i = 0; i < size; i++){
        printf("%f, ", calculeted_x_vector[i]);
        errors_sum += fabs(calculeted_x_vector[i] - x_vector[i]);
    }
    printf("\nLaczny blad : %f\n", errors_sum);




    return 0;
}
