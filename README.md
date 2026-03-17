<div align="center">

# ⚡ AWS Lambda vs Docker on EC2

### The Cost Impact of INIT Phase Billing on Serverless Deployment Decisions

<br>

[![Research](https://img.shields.io/badge/Research-2026-blueviolet?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Submitted-orange?style=for-the-badge)](.)
[![Experiments](https://img.shields.io/badge/Experiments-600_Runs-success?style=for-the-badge)](.)
[![Workloads](https://img.shields.io/badge/Workloads-3_Levels-blue?style=for-the-badge)](.)

<br>

<img src="https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white" alt="AWS Lambda"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/Amazon_EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white" alt="Amazon EC2"/>
<img src="https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>

<br><br>

> **TL;DR:** AWS changed how they bill Lambda in August 2025. Nobody has studied what this means for cost decisions. I did. The crossover point is not a single number — it shifts from 82,000 to 50,000 requests/day depending on workload intensity. Every prior cost model missed this entirely.

<br>

---

</div>

## 📄 Research Paper

<table>
<tr>
<td><b>Title</b></td>
<td>The Cost Impact of AWS Lambda's INIT Phase Billing on Serverless vs Container Deployment Decisions: An Empirical Analysis</td>
</tr>
<tr>
<td><b>Author</b></td>
<td>Muhammad Moazzam Hafeez — FAST NUCES Islamabad, Pakistan</td>
</tr>
<tr>
<td><b>Status</b></td>
<td>🔄 Submitted 2026</td>
</tr>
</table>

<br>

---

## 🧠 The Problem In Plain English

<table>
<tr>
<td width="60">
<h1>💡</h1>
</td>
<td>

When you use AWS Lambda, sometimes it "wakes up cold" — this delay is called a **cold start** or **INIT phase.**

For years, this was just a speed problem. Annoying, but free.

**On August 1, 2025, AWS started charging for it.**

Every paper ever written about Lambda costs missed this. Every cost model, every comparison, every benchmark — all assumed INIT phase = free.

**This research fixes that — and shows the crossover point shifts with workload complexity.**

</td>
</tr>
</table>

<br>

---

## 🔬 What I Actually Did

Built the **same REST API twice** and tested at **3 workload levels:**

<br>

<div align="center">

### 🖥️ Deployment Comparison

| | **Deployment A** | **Deployment B** |
|:---:|:---:|:---:|
| **Platform** | <img src="https://img.shields.io/badge/AWS_Lambda-FF9900?style=flat-square&logo=awslambda&logoColor=white"/> | <img src="https://img.shields.io/badge/Docker_on_EC2-2496ED?style=flat-square&logo=docker&logoColor=white"/> |
| **Language** | Python 3.11 | Python 3.11 + Flask |
| **Billing** | Per request + INIT phase | Fixed $0.0104/hour |
| **Cold Start** | Yes — every idle invocation | Never |

<br>

### 🔥 Workload Levels

| Workload | Computation | Runs |
|:---:|:---:|:---:|
| 🟢 **Light** | Primes up to 500 | 100 runs each |
| 🟡 **Medium** | Primes up to 5,000 | 100 runs each |
| 🔴 **Heavy** | Primes up to 50,000 | 100 runs each |

</div>

<br>

<div align="center">
<img src="https://img.shields.io/badge/Total-600_Automated_Benchmark_Runs-success?style=for-the-badge"/>
</div>

<br>

---

## 📊 Experiment Results

<details>
<summary><b>🖼️ Live Benchmark Running — 600 Automated Requests</b> (Click to expand)</summary>
<br>

![Experiment Running](experiment_result_1.png)

*Real-time output of the benchmark script — 100 runs per workload per deployment*

</details>

<br>

<details>
<summary><b>📋 Final Summary Output</b> (Click to expand)</summary>
<br>

![Experiment Summary](experiment_result_2.png)

*Lambda avg 1,327ms–2,375ms vs Docker avg 498ms–545ms across workloads*

</details>

<br>

---

## 📈 Performance Analysis

<div align="center">

![Performance Analysis](results/chart1_response_time.png)

</div>

<br>

<div align="center">

### ⏱️ Response Time Comparison

| Workload | Lambda Mean | Docker Mean | Lambda Slower By |
|:---:|:---:|:---:|:---:|
| 🟢 **Light** | 1,327 ms | 498 ms | **2.7x** 📉 |
| 🟡 **Medium** | 1,432 ms | 527 ms | **2.7x** 📉 |
| 🔴 **Heavy** | 2,375 ms | 545 ms | **4.4x** 📉 |

<br>

### 📊 Statistical Deep Dive (Light Workload)

| Metric | Lambda | Docker |
|:---:|:---:|:---:|
| **Mean** | 1,327 ms | 498 ms |
| **Median** | 1,267 ms | 486 ms |
| **Std Deviation** | 306 ms 😬 | 109.09 ms ✅ |
| **INIT Phase** | 1,327 ms (99.97%) | 0 ms |

</div>

<br>

> [!IMPORTANT]
> As workload gets heavier, Lambda gets dramatically slower while Docker stays stable

<br>

---

## 💰 Cost Analysis

<div align="center">

![Cost Analysis](results/chart2_cost_crossover.png)

<br>

### 🔴 Heavy Workload Cost Table

| Requests/Day | Lambda Cost | Docker Cost | Winner |
|:---:|:---:|:---:|:---:|
| 10 | $0.000053 | $0.2496 | ✅ **Lambda** |
| 100 | $0.000527 | $0.2496 | ✅ **Lambda** |
| 1,000 | $0.005266 | $0.2496 | ✅ **Lambda** |
| 5,000 | $0.026330 | $0.2496 | ✅ **Lambda** |
| 10,000 | $0.052661 | $0.2496 | ✅ **Lambda** |
| 50,000 | $0.263304 | $0.2496 | ✅ **Docker EC2** |
| 100,000 | $0.526607 | $0.2496 | ✅ **Docker EC2** |

</div>

<br>

---

## 🎯 The Key Finding

<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           🎯  COST CROSSOVER POINT IS WORKLOAD-DEPENDENT  🎯                 ║
║                                                                              ║
║  ╭─────────────────────────────────────────────────────────────────────────╮ ║
║  │                                                                         │ ║
║  │   🟢 Light workload   →   crossover at   ~82,000  req/day   ✅         │ ║
║  │   🟡 Medium workload  →   crossover at   ~76,700  req/day   ✅         │ ║
║  │   🔴 Heavy workload   →   crossover at   ~50,000  req/day   ✅         │ ║
║  │                                                                         │ ║
║  ╰─────────────────────────────────────────────────────────────────────────╯ ║
║                                                                              ║
║         📊 39% shift driven entirely by INIT phase billing                   ║
║            (a cost that was $0.00 in ALL prior research)                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

</div>

<br>

> [!NOTE]
> **Provisioned Concurrency note:** Even with PC enabled ($0.0000041667/GB-s), Lambda stays above the Docker EC2 cost threshold at high volumes — PC eliminates latency but does not solve the cost disadvantage.

<br>

---

## 📁 Repository Structure

```
cloud-research/
│
├── 📂 lambda-api/
│   ├── 📄 app.py                   # Lambda function — 3 workload levels
│   └── 📦 function.zip             # Deployment package
│
├── 📂 docker-api/
│   ├── 📄 app.py                   # Flask API — identical logic
│   ├── 🐳 Dockerfile               # Container definition
│   └── 📄 requirements.txt         # Dependencies
│
├── 📂 results/
│   ├── 🧪 experiment.py            # Original 100-run benchmark script
│   ├── 🧪 experiment_v2.py         # 600-run multi-workload script
│   ├── 💵 cost_analysis.py         # Original cost model
│   ├── 💵 cost_analysis_v2.py      # Multi-workload cost + crossover
│   ├── 📊 create_charts.py         # Chart generation script
│   ├── 📋 benchmark_results.csv    # Original 100-run raw data
│   └── 📋 benchmark_results_v2.csv # Full 600-run raw data
│
└── 📖 README.md
```

<br>

---

## 🚀 Reproduce This Experiment

<details>
<summary><b>📋 Prerequisites</b></summary>
<br>

- ☁️ AWS account (Free Tier works)
- 🐍 Python 3.11
- 🐳 Docker Desktop

</details>

<br>

<details>
<summary><b>Step 1 — Deploy Lambda</b></summary>
<br>

```bash
cd lambda-api
pip install awscli
aws configure
powershell Compress-Archive -Path app.py -DestinationPath function.zip
aws lambda create-function --function-name cloud-research-api \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-research-role \
  --handler app.lambda_handler \
  --zip-file fileb://function.zip
aws lambda create-function-url-config --function-name cloud-research-api --auth-type NONE
```

</details>

<br>

<details>
<summary><b>Step 2 — Deploy Docker on EC2</b></summary>
<br>

```bash
# Launch EC2 t3.micro on AWS Console, SSH in, then:
docker build -t research-api .
docker run -d -p 5000:5000 research-api
```

</details>

<br>

<details>
<summary><b>Step 3 — Run the Full Benchmark</b></summary>
<br>

```bash
cd results
pip install requests matplotlib
python experiment_v2.py     # 600 runs across 3 workloads
python cost_analysis_v2.py  # crossover points per workload
python create_charts.py     # generates Fig 1 and Fig 2
```

</details>

<br>

---

## 🔑 Why This Matters

<table>
<tr>
<td align="center" width="33%">
<h3>👨‍💻 For Developers</h3>
</td>
<td align="center" width="33%">
<h3>⚙️ For DevOps Engineers</h3>
</td>
<td align="center" width="33%">
<h3>🔬 For Researchers</h3>
</td>
</tr>
<tr>
<td valign="top">

The crossover point is not a fixed number. A lightweight webhook handler has a different threshold than a data-processing API. This research gives you **workload-specific guidance** for the first time.

</td>
<td valign="top">

Every cost calculator, every AWS blog post, every comparison article still uses the old pre-August 2025 billing model. This gives you **updated, empirically validated numbers**.

</td>
<td valign="top">

This is the **first empirical study** to incorporate AWS Lambda's August 2025 INIT phase billing change into a crossover analysis across multiple workload intensities. 13 papers reviewed — zero accounted for it.

</td>
</tr>
</table>

<br>

---

## 🛠️ Tech Stack

<div align="center">

<br>

| Category | Technologies |
|:---:|:---|
| **Cloud** | ![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white) ![Amazon EC2](https://img.shields.io/badge/Amazon_EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white) |
| **Container** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| **Backend** | ![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) |
| **Version Control** | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) |

</div>

<br>

---

## 📬 Contact

<div align="center">

<br>

**Muhammad Moazzam Hafeez**

FAST NUCES — Department of Computer Science, Islamabad, Pakistan

<br>

[![Email](https://img.shields.io/badge/Email-i221093@nu.edu.pk-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:i221093@nu.edu.pk)
[![GitHub](https://img.shields.io/badge/GitHub-MoazzamHafeez1093-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MoazzamHafeez1093)

<br>

---

<br>

<sub>Research conducted March 2026 | 600 experimental runs | 3 workload levels | AWS us-east-1</sub>

<br>

<img src="https://img.shields.io/badge/Made_with-❤️-red?style=flat-square"/> <img src="https://img.shields.io/badge/Powered_by-☕-brown?style=flat-square"/>

</div>
