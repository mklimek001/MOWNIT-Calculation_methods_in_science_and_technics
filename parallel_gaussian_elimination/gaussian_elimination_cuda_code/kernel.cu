// Eliminacja Gaussa z wykorzystaniem CUDA 


#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <string.h>


void gaussianEliminationWithCuda(double* matrix, int size);
double* readMatrix(char* file_addr);
int readLength(char* file_addr);
void findSolution(double* matrix, int size);



__global__ void operationA(double* matrix, double* multipliers, int round_number, int height)
{
    int i = threadIdx.x;
    int j = height - 1 - i;
    int len = height + 1;

    multipliers[j] = matrix[j * len + round_number] / matrix[round_number * len + round_number];
}


__global__ void operationB(double* matrix, double* multipliers, double* substractors, int round_number, int height)
{
    int i = threadIdx.x;
    int j = height - 1 - i;
    int len = height + 1;

    for (int pos = 0; pos < len; pos++) {
        substractors[j * len + pos] = matrix[round_number * len + pos] * multipliers[j];
    }
}


__global__ void operationC(double* matrix, double* substractors, int round_number, int height)
{
    int i = threadIdx.x;
    int j = height - 1 - i;
    int len = height + 1;

    for (int pos = 0; pos < len; pos++) {
        matrix[j * len + pos] = matrix[j * len + pos] - substractors[j * len + pos];
    }
}



int main()
{
    printf("___Gaussian elimination with CUDA___\n");

    char* file_link = "file1.txt";
    int size = readLength(file_link);
    double* matrix = readMatrix(file_link);

    printf("\nGiven matrix:\n");
    for (int i = 0; i < size; i++) {
        for (int j = 0; j <= size; j++) {
            printf("%f ", matrix[i * (size + 1) + j]);
        }
        printf("\n");
    }

    gaussianEliminationWithCuda(matrix, size);

    printf("\nMatrix after Gaussian elimination:\n");
    for (int i = 0; i < size; i++) {
        for (int j = 0; j <= size; j++) {
            printf("%f ", matrix[i * (size + 1) + j]);
        }
        printf("\n");
    }

    findSolution(matrix, size);

    printf("\nFound solution:\n");
    for (int i = 0; i < size; i++) {
        for (int j = 0; j <= size; j++) {
            printf("%f ", matrix[i * (size + 1) + j]);
        }
        printf("\n");
    }


    char* result_file_link = "file2.txt";
    double* matrix_exp = readMatrix(result_file_link);


    printf("\nExpected solution:\n");
    for (int i = 0; i < size; i++) {
        for (int j = 0; j <= size; j++) {
            printf("%f ", matrix_exp[i * (size + 1) + j]);
        }
        printf("\n");
    }

    return 0;
}

void gaussianEliminationWithCuda(double* matrix, int size)
{
    cudaSetDevice(0);

    int len = size + 1;
    int i, j, to_change;
    double copied;
    double* substractors = (double*)calloc(size * (size + 1), sizeof(double));
    double* multipliers = (double*)calloc(size, sizeof(double));

    double* gpu_matrix = 0;
    double* gpu_A_mulitpliers = 0;
    double* gpu_B_substractor = 0;

    cudaMalloc((void**)&gpu_matrix, size * len * sizeof(double));
    cudaMalloc((void**)&gpu_A_mulitpliers, size * sizeof(double));
    cudaMalloc((void**)&gpu_B_substractor, size * len * sizeof(double));


    cudaMemcpy(gpu_matrix, matrix, size * (size + 1) * sizeof(double), cudaMemcpyHostToDevice);
    cudaMemcpy(gpu_A_mulitpliers, multipliers, size * sizeof(double), cudaMemcpyHostToDevice);
    cudaMemcpy(gpu_B_substractor, substractors, size * (size + 1) * sizeof(double), cudaMemcpyHostToDevice);

    for (int round = 1; round < size; round++) {
        operationA << <1, (size - round) >> > (gpu_matrix, gpu_A_mulitpliers, round - 1, size);
        cudaDeviceSynchronize();
        operationB << <1, (size - round) >> > (gpu_matrix, gpu_A_mulitpliers, gpu_B_substractor, round - 1, size);
        cudaDeviceSynchronize();
        operationC << <1, (size - round) >> > (gpu_matrix, gpu_B_substractor, round - 1, size);
        cudaDeviceSynchronize();


        cudaMemcpy(matrix, gpu_matrix, size * (size + 1) * sizeof(double), cudaMemcpyDeviceToHost);

        i = round - 1;
        if (matrix[len * i + i] == 0.0) {
            to_change = i;
            for (j = i + 1; j < size; j++) {
                if (matrix[len * j + i] != 0.0) {
                    to_change = j;
                    break;
                }

            }

            for (j = 0; j < len; j++) {
                matrix[len * i + j], matrix[len * to_change + j] = matrix[len * to_change + j], matrix[len * i + j];
            }

        }

        cudaMemcpy(gpu_matrix, matrix, size * (size + 1) * sizeof(double), cudaMemcpyHostToDevice);




    }

    cudaMemcpy(matrix, gpu_matrix, size * (size + 1) * sizeof(double), cudaMemcpyDeviceToHost);

    cudaFree(gpu_matrix);
    cudaFree(gpu_A_mulitpliers);
    cudaFree(gpu_B_substractor);

    free(substractors);
    free(multipliers);

    cudaDeviceReset();

    return;
}



double* readMatrix(char* file_addr)
{
    double* matrix = 0;
    int pos_in_matrix = 0;

    int max_len = 20;
    FILE* ptr;
    char ch;

    double curr_val;
    int size = -1;
    int position = 0;
    int row_counter = 0;
    int last_col_counter = 0;

    char* buffer = (char*)calloc(max_len, sizeof(char));

    ptr = fopen(file_addr, "r");

    if (NULL == ptr) {
        printf("FILE ERROR \n");
    }

    do {
        ch = fgetc(ptr);
        if (ch != ' ' && ch != '\n' && ch != EOF) {
            buffer[position] = ch;
            position++;
        }
        else {
            if (size == -1) {
                size = atoi(buffer);
                matrix = (double*)calloc(size * (size + 1), sizeof(double));
            }
            else {
                curr_val = atof(buffer);
                if (row_counter < size) {
                    matrix[pos_in_matrix] = curr_val;
                    pos_in_matrix++;
                    if (pos_in_matrix % (size + 1) == size) {
                        pos_in_matrix++;
                    }
                }
                else {
                    matrix[last_col_counter * (size + 1) + size] = curr_val;
                    last_col_counter++;
                }

                if (ch == '\n') {
                    row_counter++;
                }
            }
            position = 0;
            memset(buffer, '0', max_len);
        }
    } while (ch != EOF);

    fclose(ptr);

    return matrix;
}


int readLength(char* file_addr)
{
    int max_len = 10;
    FILE* ptr;
    char ch;

    int size = -1;

    char* buffer = (char*)calloc(max_len, sizeof(char));
    int position = 0;

    ptr = fopen(file_addr, "r");

    if (NULL == ptr) {
        printf("FILE ERROR \n");
    }

    do {
        ch = fgetc(ptr);
        if (ch != ' ' && ch != '\n' && ch != EOF) {
            buffer[position] = ch;
            position++;
        }
        else {
            if (size == -1) {
                size = atoi(buffer);
                return size;
            }
        }
    } while (ch != EOF);
    return 0;
}


void findSolution(double* matrix, int size) {
    int len = size + 1;
    double curr_sum;

    for (int i = size - 1; i >= 0; i--) {
        curr_sum = matrix[len * i + size];
        for (int j = i + 1; j < size; j++) {
            curr_sum -= matrix[len * i + j] * matrix[len * j + size];
            matrix[len * i + j] = 0.0;
        }
        matrix[len * i + size] = curr_sum / matrix[len * i + i];
        matrix[len * i + i] = 1.0;
    }

    return;
}