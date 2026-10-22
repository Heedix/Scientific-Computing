#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    int local = rank + 1, total = 0;
    MPI_Reduce(&local, &total, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    printf("Hallo von Rang %d von %d\n", rank, size);
    if (rank == 0) {
        printf("Summe der Raenge plus eins: %d\n", total);
    }
    MPI_Finalize();
    return 0;
}
