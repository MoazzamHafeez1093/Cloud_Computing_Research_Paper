import requests
import time
import csv
import json
from datetime import datetime

LAMBDA_URL = "https://gq3rbfxjwjsqhchbse5rvkcbja0vyfdm.lambda-url.us-east-1.on.aws/"
DOCKER_URL = "http://44.210.151.116:5000"
TOTAL_RUNS = 50
OUTPUT_FILE = "benchmark_results.csv"

def send_request(url, run_number, deployment_type):
    try:
        start = time.time()
        response = requests.get(url, timeout=30)
        end = time.time()
        
        total_ms = round((end - start) * 1000, 2)
        body = response.json()
        compute_ms = body.get("computation_ms", 0)
        startup_ms = round(total_ms - compute_ms, 2)
        
        return {
            "run": run_number,
            "deployment": deployment_type,
            "total_response_ms": total_ms,
            "computation_ms": compute_ms,
            "startup_ms": startup_ms,
            "status": response.status_code,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "run": run_number,
            "deployment": deployment_type,
            "total_response_ms": -1,
            "computation_ms": -1,
            "startup_ms": -1,
            "status": "ERROR",
            "timestamp": datetime.now().isoformat()
        }

results = []

print("=" * 50)
print("CLOUD RESEARCH BENCHMARK EXPERIMENT")
print("=" * 50)

# Run Lambda requests
print(f"\nTesting Lambda ({TOTAL_RUNS} runs)...")
for i in range(1, TOTAL_RUNS + 1):
    result = send_request(LAMBDA_URL, i, "Lambda")
    results.append(result)
    print(f"  Run {i:02d}: {result['total_response_ms']}ms total | {result['startup_ms']}ms startup")
    time.sleep(2)  # 2 second gap to capture cold starts

# Run Docker requests  
print(f"\nTesting Docker on EC2 ({TOTAL_RUNS} runs)...")
for i in range(1, TOTAL_RUNS + 1):
    result = send_request(DOCKER_URL, i, "Docker-EC2")
    results.append(result)
    print(f"  Run {i:02d}: {result['total_response_ms']}ms total | {result['startup_ms']}ms startup")
    time.sleep(2)

# Save to CSV
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n" + "=" * 50)
print(f"DONE. Results saved to {OUTPUT_FILE}")
print("=" * 50)

# Print quick summary
lambda_times = [r["total_response_ms"] for r in results if r["deployment"] == "Lambda" and r["total_response_ms"] > 0]
docker_times = [r["total_response_ms"] for r in results if r["deployment"] == "Docker-EC2" and r["total_response_ms"] > 0]

print(f"\nLambda  — avg: {round(sum(lambda_times)/len(lambda_times))}ms | min: {min(lambda_times)}ms | max: {max(lambda_times)}ms")
print(f"Docker  — avg: {round(sum(docker_times)/len(docker_times))}ms | min: {min(docker_times)}ms | max: {max(docker_times)}ms")
