#include <pari/pari.h>

int main(void) {
    pari_init(8000000, 500000);
    GEN n = stoi(360);
    GEN factors = factorint(n, 0);
    pari_printf("Primfaktorzerlegung von %Ps: %Ps\n", n, factors);
    pari_close();
    return 0;
}
