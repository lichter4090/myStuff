#define NN_IMPL
#include "nn.h"



int main(void)
{
    Mat* m = matAlloc(2, 2);
    Mat* m1 = matAlloc(2, 1);
    Mat* output = matAlloc(2, 3);

    matFill(m, 0);
    matFill(m1, 0);
    matFill(output, 1);

    MAT_AT(output, 1, 2) = 2;

    MAT_PRINT(m);
    MAT_PRINT(m1);
    MAT_PRINT(output);

    matSplit(output, m, m1, 2);

    MAT_PRINT(m);
    MAT_PRINT(m1);
    MAT_PRINT(output);

    matFree(m);
    matFree(m1);
    matFree(output);
    getchar();
    return 0;
}