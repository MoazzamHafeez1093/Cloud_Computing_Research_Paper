import csv
from statistics import mean, median, stdev

# AWS Pricing (as of August 2025 with INIT phase billing)
LAMBDA_PRICE_PER_REQUEST = 0.0000002        # $0.20 per 1M requests
LAMBDA_PRICE_PER_GB_SEC = 0.0000166667      # per GB-second of execution
LAMBDA_PRICE_PER_GB_SEC_INIT = 0.0000166667 # INIT phase now billed same rate
LAMBDA_MEMORY_GB = 0.128                    # 128MB = 0.128 GB

EC2_HOURLY_RATE = 0.0104                    # t3.micro us-east-1
EC2_HOURS_PER_DAY = 24

# Load results
results = []
with open("benchmark_results.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        results.append(row)

lambda_data = [r for r in results if r["deployment"] == "Lambda" and float(r["total_response_ms"]) > 0]
docker_data = [r for r in results if r["deployment"] == "Docker-EC2" and float(r["total_response_ms"]) > 0]

# Response time stats
lambda_times = [float(r["total_response_ms"]) for r in lambda_data]
docker_times = [float(r["total_response_ms"]) for r in docker_data]
lambda_startup = [float(r["startup_ms"]) for r in lambda_data]

print("=" * 60)
print("PERFORMANCE ANALYSIS")
print("=" * 60)
print(f"\nLambda Response Time:")
print(f"  Mean:    {mean(lambda_times):.2f} ms")
print(f"  Median:  {median(lambda_times):.2f} ms")
print(f"  Std Dev: {stdev(lambda_times):.2f} ms")
print(f"  Min:     {min(lambda_times):.2f} ms")
print(f"  Max:     {max(lambda_times):.2f} ms")

print(f"\nDocker EC2 Response Time:")
print(f"  Mean:    {mean(docker_times):.2f} ms")
print(f"  Median:  {median(docker_times):.2f} ms")
print(f"  Std Dev: {stdev(docker_times):.2f} ms")
print(f"  Min:     {min(docker_times):.2f} ms")
print(f"  Max:     {max(docker_times):.2f} ms")

print(f"\nLambda INIT Phase (Startup) Time:")
print(f"  Mean:    {mean(lambda_startup):.2f} ms")
print(f"  Max:     {max(lambda_startup):.2f} ms")

# Cost analysis per build frequency
print("\n" + "=" * 60)
print("COST ANALYSIS — DAILY REQUEST FREQUENCY")
print("=" * 60)
print(f"\n{'Requests/Day':<15} {'Lambda Cost':<20} {'Docker Cost':<20} {'Cheaper'}")
print("-" * 60)

frequencies = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]

crossover = None
for freq in frequencies:
    # Lambda cost per day
    avg_exec_sec = mean(lambda_times) / 1000
    avg_init_sec = mean(lambda_startup) / 1000
    
    exec_cost = freq * LAMBDA_PRICE_PER_REQUEST
    exec_cost += freq * (avg_exec_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC)
    init_cost = freq * (avg_init_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC_INIT)
    lambda_daily = exec_cost + init_cost

    # Docker cost per day (fixed regardless of requests)
    docker_daily = EC2_HOURLY_RATE * EC2_HOURS_PER_DAY

    cheaper = "Lambda" if lambda_daily < docker_daily else "Docker EC2"
    
    if lambda_daily >= docker_daily and crossover is None:
        crossover = freq

    print(f"{freq:<15} ${lambda_daily:<19.6f} ${docker_daily:<19.4f} {cheaper}")

print("\n" + "=" * 60)
print("KEY FINDING")
print("=" * 60)
if crossover:
    print(f"\nCost Crossover Point: ~{crossover} requests/day")
    print(f"Below {crossover} req/day → Lambda is cheaper")
    print(f"Above {crossover} req/day → Docker EC2 is cheaper")
print(f"\nINIT phase adds ${mean(lambda_startup)/1000 * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC_INIT * 1000000:.4f} per 1000 requests")
print("=" * 60)

