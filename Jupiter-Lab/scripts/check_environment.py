"""Run inside the container: python scripts/check_environment.py."""
import importlib
import shutil
import subprocess
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]

for name in ['numpy', 'sympy', 'matplotlib', 'scipy', 'mpi4py.MPI']:
    importlib.import_module(name)
    print(f'Import OK: {name}', flush=True)

for tool in ['mpiexec', 'mpicc', 'gcc', 'maxima', 'gp']:
    assert shutil.which(tool), f'Werkzeug fehlt: {tool}'

kernels = KernelSpecManager().find_kernel_specs()
assert {'python3', 'bash'} <= kernels.keys(), f'Kernel fehlen: {kernels}'

# Also test an uneven partition and the single-process communication branch.
for processes in [1, 3]:
    output = subprocess.check_output(
        ['mpiexec', '--oversubscribe', '-n', str(processes), 'python',
         str(ROOT / 'examples' / 'mpi_sum.py')], text=True, timeout=60)
    assert 'Gesamtsumme: 5050' in output
    print(f'MPI mit {processes} Prozess(en) OK', flush=True)

for name in ['01_Scientific_Computing.ipynb', '02_Bash_und_Werkzeuge.ipynb']:
    path = ROOT / 'notebooks' / name
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    print(f'Führe {name} aus …', flush=True)
    NotebookClient(notebook, timeout=120, resources={'metadata': {'path': str(ROOT)}},
                   allow_errors=False).execute()
    executed = path.with_name(path.stem + '_executed.ipynb')
    nbformat.write(notebook, executed)
    print(f'OK: {executed.name}', flush=True)

print('Alle Umgebungs- und Notebook-Prüfungen erfolgreich.', flush=True)
