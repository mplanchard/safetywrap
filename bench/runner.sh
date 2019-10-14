# Must have hyperfine installed.

echo "Overall execution time, including interpreter spinup"
echo

hyperfine 'python sample.py classical'

hyperfine 'python sample.py monadic'

echo "Average execution time in seconds within python, excluding interpreter spinup, over 1e6 iterations"
echo

echo "Classical"
python sample.py classical timeit

echo "Monadic"
python sample.py monadic timeit
