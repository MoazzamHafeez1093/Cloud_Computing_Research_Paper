import csv
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

# Load data
results = []
with open("benchmark_results_v2.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        results.append(row)

workloads = ['light', 'medium', 'heavy']
workload_labels = ['Light\n(500 primes)', 'Medium\n(5,000 primes)', 'Heavy\n(50,000 primes)']

# ============================================
# CHART 1 — Response Time Comparison Bar Chart
# ============================================
lambda_means = []
docker_means = []
lambda_stds = []
docker_stds = []

for workload in workloads:
    lt = [float(r["total_response_ms"]) for r in results
          if r["deployment"] == "Lambda" and r["workload"] == workload
          and float(r["total_response_ms"]) > 0]
    dt = [float(r["total_response_ms"]) for r in results
          if r["deployment"] == "Docker-EC2" and r["workload"] == workload
          and float(r["total_response_ms"]) > 0]
    lambda_means.append(mean(lt))
    docker_means.append(mean(dt))
    lambda_stds.append(np.std(lt))
    docker_stds.append(np.std(dt))

x = np.arange(len(workloads))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
bars1 = ax.bar(x - width/2, lambda_means, width, 
               yerr=lambda_stds, capsize=5,
               label='AWS Lambda', color='#FF9900', alpha=0.85)
bars2 = ax.bar(x + width/2, docker_means, width,
               yerr=docker_stds, capsize=5,
               label='Docker on EC2', color='#2496ED', alpha=0.85)

ax.set_xlabel('Workload Intensity', fontsize=12)
ax.set_ylabel('Mean Response Time (ms)', fontsize=12)
ax.set_title('Fig. 1: Mean Response Time — AWS Lambda vs Docker on EC2\nAcross Three Workload Intensities (N=100 per workload)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(workload_labels, fontsize=10)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

for bar in bars1:
    ax.annotate(f'{bar.get_height():.0f}ms',
                xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points",
                ha='center', fontsize=9)
for bar in bars2:
    ax.annotate(f'{bar.get_height():.0f}ms',
                xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points",
                ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('chart1_response_time.png', dpi=150, bbox_inches='tight')
print("Chart 1 saved: chart1_response_time.png")
plt.close()

# ============================================
# CHART 2 — Cost Crossover Line Chart
# ============================================
LAMBDA_PRICE_PER_REQUEST = 0.0000002
LAMBDA_PRICE_PER_GB_SEC = 0.0000166667
LAMBDA_MEMORY_GB = 0.128
EC2_HOURLY_RATE = 0.0104

frequencies = list(range(1000, 120000, 1000))
ec2_costs = [EC2_HOURLY_RATE * 24] * len(frequencies)

colors = ['#FF6B35', '#8B5CF6', '#EF4444']
crossover_points = {'light': 82000, 'medium': 76700, 'heavy': 50000}

fig, ax = plt.subplots(figsize=(10, 5))

for idx, workload in enumerate(workloads):
    lambda_data = [r for r in results if r["deployment"] == "Lambda"
                   and r["workload"] == workload
                   and float(r["total_response_ms"]) > 0]

    avg_exec_sec = mean([float(r["computation_ms"]) for r in lambda_data]) / 1000
    avg_init_sec = mean([float(r["startup_ms"]) for r in lambda_data]) / 1000

    lambda_costs = []
    for freq in frequencies:
        cost = freq * LAMBDA_PRICE_PER_REQUEST
        cost += freq * (avg_exec_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC)
        cost += freq * (avg_init_sec * LAMBDA_MEMORY_GB * LAMBDA_PRICE_PER_GB_SEC)
        lambda_costs.append(cost)

    ax.plot(frequencies, lambda_costs,
            color=colors[idx], linewidth=2,
            label=f'Lambda — {workload_labels[idx].replace(chr(10), " ")}')

ax.plot(frequencies, ec2_costs,
        color='#2496ED', linewidth=2.5,
        linestyle='--', label='Docker EC2 (fixed $0.2496/day)')

ax.axvline(x=50000, color='#EF4444', linestyle=':', alpha=0.7, linewidth=1.5)
ax.axvline(x=82000, color='#FF6B35', linestyle=':', alpha=0.7, linewidth=1.5)
ax.text(51000, 0.38, '50K\n(heavy)', fontsize=8, color='#EF4444')
ax.text(72000, 0.38, '82K\n(light)', fontsize=8, color='#FF6B35')

ax.set_xlabel('Daily Request Frequency', fontsize=12)
ax.set_ylabel('Estimated Daily Cost (USD)', fontsize=12)
ax.set_title('Fig. 2: Cost Crossover Analysis — Lambda vs Docker EC2\nUnder AWS Post-August 2025 INIT Phase Billing Model', fontsize=11)
ax.legend(fontsize=9, loc='upper left')
ax.grid(alpha=0.3)
ax.set_xlim(0, 115000)
ax.set_ylim(0, 0.55)

plt.tight_layout()
plt.savefig('chart2_cost_crossover.png', dpi=150, bbox_inches='tight')
print("Chart 2 saved: chart2_cost_crossover.png")
plt.close()

print("\nBoth charts created successfully!")
