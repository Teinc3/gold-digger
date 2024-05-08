#include <stdio.h>
#include <stdlib.h>

#define i64 unsigned long long

i64 transform(i64 v, i64 seed, i64 min, i64 max)
{
    return min + (v * seed + 137) % (max - min);
};

int main(int argc, char *argv[]) {

    if (argc != 3) {
        return 1;
    }

    // Convert arguments
    i64 seed1 = strtoull(argv[1], NULL, 10);
    i64 seed2 = strtoull(argv[2], NULL, 10);

    i64 result = 1ull;
    for (i64 i = 0; i <= 50; i++)
    {   
        i64 loopCount = 65536ull + (result * i & 16383ull);
        for (int j = 0; j < loopCount; j++)
        {
            result = 1ull + (result * seed1) % seed2;
        }
        seed1 = transform(seed1, result, 16384ull, 65536ull);
        seed2 = transform(seed2, result, 1ull << 18, 1ull << 20);
    }

    result = (result - 1ul) & 65535ull;

    printf("%llu", result);

    return 0;
};