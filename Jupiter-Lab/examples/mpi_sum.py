"""Run: mpiexec --oversubscribe -n 4 python examples/mpi_sum.py."""
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Broadcast: All processes receive the same upper bound.
n = comm.bcast(100 if rank == 0 else None, root=0)
# The strided partition covers 1..n once, including when n % size != 0.
local_sum = sum(range(rank + 1, n + 1, size))
parts = comm.gather(local_sum, root=0)
total = comm.reduce(local_sum, op=MPI.SUM, root=0)

if rank == 0:
    assert total == n * (n + 1) // 2
    print(f"Prozesse: {size}; Teilsummen: {parts}; Gesamtsumme: {total}")

# Point-to-point communication: rank 0 sends, rank 1 receives.
if size >= 2:
    if rank == 0:
        comm.send("Hallo von Prozess 0", dest=1, tag=7)
    elif rank == 1:
        message = comm.recv(source=0, tag=7)
        print(f"Prozess 1 empfaengt: {message}", flush=True)
