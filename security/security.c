#include <stdio.h>
#include <stdlib.h>

#define i64 unsigned long long

i64 square(i64 x)
{
    return x * x;
}

i64 transform(i64 v, i64 seed, i64 min, i64 max)
{
    return min + (v * seed + 137) % (max - min);
};

i64 sumPowersModN(i64 x, i64 pow, i64 seed2)
{
    if (pow == 0)
    {
        return 1;
    }
    else if (pow % 2 == 0)
    {
        return (1 + (x + square(x) % seed2) * sumPowersModN(square(x) % seed2, (pow - 2) / 2, seed2)) % seed2;
    }
    else {
        return ((1 + x) * sumPowersModN(square(x) % seed2, pow / 2, seed2)) % seed2;
    }
};

i64 expModN(i64 base, i64 pow, i64 n)
{
    if (pow == 0)
    {
        return 1;
    }
    if (pow % 2 == 0)
    {
        return (square(expModN(base, pow / 2, n))) % n;
    }
    return base * expModN(base, pow - 1, n) % n;
};

i64 hashRound(i64 result, i64 seed1, i64 seed2, i64 i)
{
    i64 length = 65536ull + (result * i & 16383ull);
    i64 new_hash = sumPowersModN(seed1, length - 1, seed2);
    return (new_hash + result * expModN(seed1, length, seed2)) % seed2;
};

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        return 1;
    }

    // Convert arguments
    i64 seed1 = strtoull(argv[1], NULL, 10);
    i64 seed2 = strtoull(argv[2], NULL, 10);

    i64 result = 1ull;
    for (i64 i = 0; i <= 50; i++)
    {
        result = hashRound(result, seed1, seed2, i);
        seed1 = transform(seed1, result, 16384ull, 65536ull);
        seed2 = transform(seed2, result, 1ull << 18, 1ull << 20);   
    }

    result = (result - 1ul) & 65535ull;

    printf("%llu", result);

    return 0;
}