# D-Wave Tuner

`dwave-tuner` simplifies the process of tuning annealing parameters, allowing
you to concentrate on your model and specific problem. Simply specify the
number of embeddings, chain strengths, and annealing times, and watch as
dwave-tuner tailors the tuning experience to your needs.

## Features
- **Effortless parameter tuning**: Grid scan chain strengths and annealing
  times with a given number of embeddings.
- **Caching for efficiency**: D-Wave responses are cached by default, enhancing 
  performance by utilizing cached results unless you modify the scan or alter
  the parameters.
- **User-Friendly**: Minimal configuration; just specify your preferences in a
  dictionary, and let `dwave-tuner` handle the details.

## Example Usage
```python
import dwavetuner
```

Specify the scan parameters:
```python
parameters = {
    'num_embeddings': 10,
    'num_chain_strengths': 1,
    'num_reads': 1000,
    'num_reps': 1
}
```

Create a `Scanner` to schedule the `Job`s:
```python
scanner = dwavetuner.Scanner(my_model.bqm, label='my_model', **parameters)
```

Perform a grid scan
```python
scanner.grid_scan()
```

The grid scan stores the results in `scanner.results`. It returns a response
that can also be accessed via
```python
print(scanner.response)
```

The verbose tuning data can be accessed via
```python
x, ys, yerrs = scanner.scan_results('chain_strength')
```

For annealing time scans, replace `chain_strength` with `annealing_time`.

Note that `x` is one list, while `ys` an `yerrs` contain
`scanner.num_embeddings` lists - one for each embedding.

Alternatively, use these self-explanatory `parameters`:
```python
# Scan chain strengths
parameters = {
    'num_embeddings': 10,
    'chain_strengths_start': 0.24,
    'chain_strengths_end': 0.44,
    'num_chain_strengths': 10,
    'num_reads': 100,
    'num_reps': 1
}

# Scan annealing times
parameters = {
    'chain_strength': 0.28,
    'num_annealing_times': 10,
    'num_reads': 100,
    'num_reps': 5
}
```

## Author

Orkun Şensebat

git@senseb.at
