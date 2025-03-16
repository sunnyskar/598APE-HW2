import subprocess
import time
import matplotlib.pyplot as plt
from statistics import mean, stdev

def run_benchmark(num_runs, dataset):
    runtimes = []

    for _ in range(num_runs):
        start_time = time.time()
        subprocess.run(["./genetic_benchmark", dataset], check=True)
        end_time = time.time()
        runtimes.append(end_time - start_time)

    average_runtime = mean(runtimes)
    runtime_stdev = stdev(runtimes)
    min_runtime = min(runtimes)
    max_runtime = max(runtimes)
    print(f"Average runtime over {num_runs} runs for {dataset}: {average_runtime:.10f} seconds")
    print(f"Standard deviation of runtimes for {dataset}: {runtime_stdev:.10f} seconds")
    print(f"Minimum runtime for {dataset}: {min_runtime:.10f} seconds")
    print(f"Maximum runtime for {dataset}: {max_runtime:.10f} seconds")

    return runtimes, average_runtime, runtime_stdev, min_runtime, max_runtime

def plot_histograms(num_runs):
    datasets = ["diabetes", "cancer", "housing"]
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    for i, dataset in enumerate(datasets):
        runtimes, average_runtime, runtime_stdev, min_runtime, max_runtime = run_benchmark(num_runs, dataset)
        axs[i].hist(runtimes, bins=20, edgecolor='black')
        axs[i].set_title(f'Distribution of Runtimes for {dataset}')
        axs[i].set_xlabel('Runtime (seconds)')
        axs[i].set_ylabel('Frequency')
        axs[i].text(0.99, 0.99, f"Average runtime: {average_runtime:.10f} seconds\nStandard deviation: {runtime_stdev:.10f} seconds\nMinimum runtime: {min_runtime:.10f} seconds\nMaximum runtime: {max_runtime:.10f} seconds", horizontalalignment='right', verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5), transform=axs[i].transAxes)

    plt.tight_layout()
    plt.savefig('runtime_distribution_all.png')
    plt.show()

if __name__ == "__main__":
    num_runs = 50
    plot_histograms(num_runs)