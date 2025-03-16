# 598APE-HW2

This repository contains code for homework 2 of 598APE.

In particular, this repository is an implementation of Symbolic Regression and Classification.

To compile the program run:
```bash
make -j
```

To clean existing build artifacts run:
```bash
make clean
```

This program assumes the following are installed on your machine:
* A working C++ compiler (g++ is assumed in the Makefile)
* make

Running make builds a sample benchmarking binary(`genetic_benchmark`) which you will use for perf engineering. However, note that the symbolic regression routines exposed in `genetic.h` are general, and can be used as a sub-routine in any data science pipeline (pending a Cython wrapper to Python/Torch).

Once compiled, one can run the benchmark code on the diabetes dataset as follows:
```bash
./genetic_benchmark diabetes
# Prints the following

#===== Symbolic Regression Benchmark =====

#Loading dataset...
#Dataset dimensions: 442 samples x 10 features
#Training symbolic regressor with 512 population size and 16 generations
#Best program 1 details:
#- Length: 47 nodes
#- Depth: 10
#- Raw fitness: 4702.25
#- Test MSE: 3434.51
#- Program: ( add( fdim( exp( exp( exp( X2) ) ) , fdim( cos( abs( cos( X3) ) ) , abs( mult( X7, X0) ) ) ) , add( fdim( exp( exp( exp( X2) ) ) , fdim( abs( X3) , abs( mult( X7, X0) ) ) ) , exp( log( fdim( exp( add( exp( exp( add( X8, X0) ) ) , add( exp( X0) , exp( abs( X3) ) ) ) ) , cos( cos( X4) ) ) ) ) ) ) )
#Best program 2 details:
#- Length: 74 nodes
#- Depth: 13
#- Raw fitness: 4994.76
#- Test MSE: 3914.01
#- Program: ( add( sub( 0.004944, X0) , add( fdim( exp( add( add( fdim( cos( abs( cos( X3) ) ) , sin( exp( X8) ) ) , exp( mult( cos( fdim( X0, X3) ) , cos( cos( sin( mult( exp( X0) , sin( X3) ) ) ) ) ) ) ) , add( cos( mult( X7, X0) ) , exp( mult( sub( sin( X3) , mult( X0, X8) ) , cos( X7) ) ) ) ) ) , fdim( abs( sub( X5, X0) ) , abs( mult( X7, X0) ) ) ) , exp( log( fdim( exp( add( exp( exp( add( X8, X0) ) ) , add( exp( X0) , exp( abs( X3) ) ) ) ) , cos( exp( X0) ) ) ) ) ) ) )
#Time(Symbolic Regression (End-to-End)) = <SOME TIME ON YOUR SYSTEM>
```
`Xi` corresponds to the `i`th feature of your dataset.

While currently hardcoded to only handle the 3 CSV datasets provided, `genetic_benchmark.cpp` in the `benchmarks` folder exposes training code for end to end symbolic regression/binary classification, starting from converting the input data to a columnar format, before dispatching it to `genetic::symFit`. 

The behaviour of the training run can be tuned through the `param` struct, which controls paramenters like the population size, functions being considered, subtree depth and so on.  

```bash
./genetic_benchmark diabetes
```

As we run the program, we see the time taken for a end to end run of symbolic regression. We have placed a timer around both the sybolic regression driver code as well as the code for binary classification. Similar to HW1, your goal is to reduce this runtime as much as possible, while maintining/increasing complexity. 

## Input Datasets
This project contains three input datasets for you to optimize. All 3 are standard scikit-learn datasets. 

### Diabetes

```bash
./genetic_benchmark diabetes
```

### Cancer

```bash
./genetic_benchmark cancer
```

### California Housing Prices

```bash
./genetic_benchmark housing
```

## Important Commits

### Compiler Flag Commit
- Commit Hash: 87b04c0
- Description: Added compiler flags.

### Parallelize Execute Kernel
- Commit Hash: 2afe4af
- Description: Parallelized `execute_kernel` and added `-ffast-math` and `-fopenmp` flags to speed up to 0.77 sec.

### Cache Friendly cpp_evolve
- Commit Hash: 6a4541e
- Description: Made `cpp_evolve` more cache friendly. Added parallelization



## Benchmark Runner

To include the visualizations from the `benchmark_runner.py`, you will need to install `matplotlib`. You can do this by running the following command:

```bash
sudo apt-get update && sudo apt-get install python3-matplotlib
```

Alternatively, you can add these dependencies to the Dockerfile before creating the Docker image.

## Code Overview

There are multiple core functions

`cpp_evolve`

`cpp_evolve` is the central evolution driver. It takes a population of candidate programs and produces a new generation by first selecting parents through tournament selection and then applying various mutation strategies (crossover, subtree mutation, hoist mutation, and point mutation) or direct reproduction. After mutation, it updates the fitness of the new generation.

`build_program`

`build_program` constructs an initial candidate program (represented as a syntax tree) using a randomized process. It chooses function nodes and terminal nodes based on specified initialization methods (grow, full, or half-and-half) and ensures that the generated program adheres to a maximum depth constraint.

`tournament_kernel` 

`tournament_kernel` implements the tournament selection process. It randomly samples subsets of the population, evaluates their fitness (including a parsimony penalty for program length), and selects the best candidates to serve as parents for the next generation.

`execute_kernel`

Given a bunch of programs(symbolic formulae), `execute_kernel` evaluates those formulae on the given input dataset and outputs predicted values. We evaluate all programs on all dataset rows. 

`compute_metric`

As the name suggests, we compute the loss/accuracy values according to the metric specified in `params`. There are 5 different metrics supported - logLoss (for classification), mean square error and root mean square error(for regression) and correlation coefficients for transformation (both Karl Pearson and Spearman's rank correlation are implemented). 

## Docker

For ease of use and installation, we provide a docker image capable of running and building code here. The source docker file is in /docker (which is essentially a list of commands to build an OS state from scratch). It contains the dependent compilers, and some other nice things.

You can build this yourself manually by running `cd docker && docker build -t <myusername>/598ape`. Alternatively we have pushed a pre-built version to `wsmoses/598ape` on Dockerhub.

You can then use the Docker container to build and run your code. If you run `./dockerrun.sh` you will enter an interactive bash session with all the packages from docker installed (that script by default uses `wsmoses/598ape`, feel free to replace it with whatever location you like if you built from scratch). The current directory (aka this folder) is mounted within `/host`. Any files you create on your personal machine will be available there, and anything you make in the container in that folder will be available on your personal machine.

