import csv
from statistics import mean, median, stdev

LAMBDA_PRICE_PER_REQUEST = 0.0000002
LAMBDA_PRICE_PER_GB_SEC = 0.0000166667
LAMBDA_PRICE_PER_GB_SEC_INIT = 0.0000166667
LAMBDA_MEMORY_GB = 0.128
EC2_HOURLY_RATE = 0.0104
EC2_HOURS_PER_DAY = 24

results = []
with open("benchmark_results_v2.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        results.append(row)

workloads = ['light', 'medium', 'heavy']
frequencies = [10, 100, 1000, 5000, 10000, 50000, 100000]

print("=" * 70)
print("PERFORMANCE ANALYSIS — V2 (600 RUNS)")
print("=" * 70)

for workload in workloads:
    lambda_data = [r for r in results if r["deployment"] == "Lambda" 
                   and r["workload"] == workload 
                   and float(r["total_response_ms"]) > 0]
    docker_data = [r for r in results if r["deployment"] == "Docker-EC2" 
                   and r["workload"] == workload 
                   and float(r["total_response_ms"]) > 0]

    lambda_times = [float(r["total_response_ms"]) for r in lambda_data]
    docker_times = [float(r["total_response_ms"]) for r in docker_data]
    lambda_startup = [float(r["startup_ms"]) for r in lambda_data]

    print(f"\n--- {workload.upper()} WORKLOAD ---")
    print(f"Lambda  | Mean: {mean(lambda_times):.2f}ms | Median: {median(lambda_times):.2f}ms | StdDev: {stdev(lambda_times):.2f}ms | Min: {min(lambda_times):.2f}ms | Max: {max(lambda_times):.2f}ms")
    print(f"Docker  | Mean: {mean(docker_times):.2f}ms | Median: {median(docker_times):.2f}ms | StdDev: {stdev(docker_times):.2f}ms | Min: {min(docker_times):.2f}ms | Max: {max(docker_times):.2f}ms")
    print(f"INIT    | Mean: {mean(lambda_startup):.2f}ms | Max: {max(lambda_startup):.2f}ms")

print("\n" + "=" * 70)
print("COST ANALYSIS — DAILY REQUEST FREQUENCY")
print("=" * 70)

for workload in workloads:
    lambda_data = [r for r in results if r["deployment"] == "Lambda"
                   and r["workload"] == workload
                   and float(r["total_response_ms"]) > 0]

    avg_exec_sec = mean([float(r["computation_ms"]) for r in lambda_data]) / 1000
    avg_init_sec = mean([float(r["startup_ms"]) for r in lambda_data]) / 1000

    print(f"\n--- {workload.upper()} WORKLOAD ---")
    print(f"{'Requests/Day':<15} {'Lambda Cost':<20} {'Docker Cost':<20} {'Cheaper'}")
    print("-" * 65)

    crossover = None
    for freq in frequencies:
        exec_cost = freq * LAMBDA_PRICE_PER_REQUEST
        exec_cost += freq * (avg_exec_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC)
        init_cost = freq * (avg_init_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC_INIT)
        lambda_daily = exec_cost + init_cost
        docker_daily = EC2_HOURLY_RATE * EC2_HOURS_PER_DAY
        cheaper = "Lambda" if lambda_daily < docker_daily else "Docker EC2"

        if lambda_daily >= docker_daily and crossover is None:
            crossover = freq

        print(f"{freq:<15} ${lambda_daily:<19.6f} ${docker_daily:<19.4f} {cheaper}")

    print(f"\n>>> CROSSOVER POINT: ~{crossover} requests/day")
    init_cost_per_1000 = 1000 * (avg_init_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC_INIT)
    print(f">>> INIT phase cost: ${init_cost_per_1000:.4f} per 1,000 requests")
