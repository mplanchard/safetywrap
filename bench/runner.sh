# Must have hyperfine installed.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Overall execution time, including interpreter spinup"
echo

hyperfine "python $DIR/sample.py classical" --min-runs 100 --warmup 50

hyperfine "python $DIR/sample.py monadic" --min-runs 100 --warmup 50

echo "Average execution time in seconds within python, excluding interpreter spinup, over 1e6 iterations"
echo

echo "Classical"
python "$DIR/sample.py" classical timeit

echo "Monadic"
python "$DIR/sample.py" monadic timeit
