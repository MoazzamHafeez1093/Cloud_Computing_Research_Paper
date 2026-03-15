import requests
import time
import csv
from datetime import datetime

LAMBDA_URL = "https://gq3rbfxjwjsqhchbse5rvkcbja0vyfdm.lambda-url.us-east-1.on.aws/"
DOCKER_URL = "http://98.92.65.232:5000"
RUNS_PER_WORKLOAD = 100
WORKLOADS = ['light', 'medium', 'heavy']
OUTPUT_FILE = "benchmark_results_v2.csv"

def send_request(url, run_number, deployment, workload):
    try:
        start = time.time()
        response = requests.get(f"{url}?workload={workload}", timeout=60)
        end = time.time()

        total_ms = round((end - start) * 1000, 2)
        body = response.json()
        compute_ms = body.get("computation_ms", 0)
        startup_ms = round(total_ms - compute_ms, 2)

        return {
            "run": run_number,
            "deployment": deployment,
            "workload": workload,
            "total_response_ms": total_ms,
            "computation_ms": compute_ms,
            "startup_ms": startup_ms,
            "primes_found": body.get("primes_found", 0),
            "status": response.status_code,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "run": run_number,
            "deployment": deployment,
            "workload": workload,
            "total_response_ms": -1,
            "computation_ms": -1,
            "startup_ms": -1,
            "primes_found": -1,
            "status": "ERROR",
            "timestamp": datetime.now().isoformat()
        }

results = []

print("=" * 60)
print("CLOUD RESEARCH BENCHMARK V2 — 600 TOTAL RUNS")
print("=" * 60)

for workload in WORKLOADS:
    print(f"\n--- WORKLOAD: {workload.upper()} ---")

    print(f"Testing Lambda ({RUNS_PER_WORKLOAD} runs)...")
    for i in range(1, RUNS_PER_WORKLOAD + 1):
        result = send_request(LAMBDA_URL, i, "Lambda", workload)
        results.append(result)
        print(f"  [{workload}] Lambda Run {i:03d}: {result['total_response_ms']}ms total | {result['startup_ms']}ms startup")
        time.sleep(3)

    print(f"Testing Docker ({RUNS_PER_WORKLOAD} runs)...")
    for i in range(1, RUNS_PER_WORKLOAD + 1):
        result = send_request(DOCKER_URL, i, "Docker-EC2", workload)
        results.append(result)
        print(f"  [{workload}] Docker Run {i:03d}: {result['total_response_ms']}ms total | {result['startup_ms']}ms startup")
        time.sleep(3)

# Save CSV
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n" + "=" * 60)
print(f"DONE. Results saved to {OUTPUT_FILE}")
print("=" * 60)

# Summary
for workload in WORKLOADS:
    lambda_times = [r["total_response_ms"] for r in results if r["deployment"] == "Lambda" and r["workload"] == workload and r["total_response_ms"] > 0]
    docker_times = [r["total_response_ms"] for r in results if r["deployment"] == "Docker-EC2" and r["workload"] == workload and r["total_response_ms"] > 0]
    print(f"\n{workload.upper()}:")
    print(f"  Lambda  — avg: {round(sum(lambda_times)/len(lambda_times))}ms | min: {min(lambda_times)}ms | max: {max(lambda_times)}ms")
    print(f"  Docker  — avg: {round(sum(docker_times)/len(docker_times))}ms | min: {min(docker_times)}ms | max: {max(docker_times)}ms")
