# ⚡ AWS Lambda vs Docker on EC2
## The Cost Impact of INIT Phase Billing on Serverless Deployment Decisions

> **TL;DR:** AWS changed how they bill Lambda in August 2025. Nobody has studied what this means for cost decisions. I did. The answer: Lambda becomes more expensive than Docker at ~38,760 requests/day — a threshold that every prior cost model completely missed.

---

## 📄 Research Paper
**Title:** The Cost Impact of AWS Lambda's INIT Phase Billing on Serverless vs Container Deployment Decisions: An Empirical Analysis

**Author:** Muhammad Moazzam Hafeez — FAST NUCES Islamabad, Pakistan

**Status:** 🔄 Submitted 2026

---

## 🧠 The Problem In Plain English

When you use AWS Lambda, sometimes it "wakes up cold" — this delay is called a **cold start** or **INIT phase.**

For years, this was just a speed problem. Annoying, but free.

**On August 1, 2025, AWS started charging for it.**

Every paper ever written about Lambda costs missed this. Every cost model, every comparison, every benchmark — all assumed INIT phase = free.

**This research fixes that.**

---

## 🔬 What I Actually Did

Built the **same REST API twice:**

| | Deployment A | Deployment B |
|---|---|---|
| **Platform** | AWS Lambda | Docker on EC2 t3.micro |
| **Language** | Python 3.11 | Python 3.11 + Flask |
| **Billing** | Per request + INIT phase | Fixed $0.0104/hour |
| **Cold Start** | Yes — every idle invocation | Never |

Then fired **100 automated requests** (50 each) and measured everything.

---

## 📊 Experiment Results

### Live Benchmark Running — 100 Automated Requests
![Experiment Running](experiment_result_1.png)
*Real-time output of the benchmark script running 50 requests against each deployment*

### Final Summary Output
![Experiment Summary](experiment_result_2.png)
*Lambda avg 1463ms vs Docker avg 495ms — Docker is 2.96x faster*

---

## 📈 Performance Analysis

![Performance Analysis](performance_analysis.png)

| Metric | Lambda | Docker EC2 |
|---|---|---|
| **Mean** | 1,463 ms | 495 ms |
| **Median** | 1,297 ms | 491 ms |
| **Std Deviation** | 384 ms 😬 | 34 ms ✅ |
| **Min** | 1,095 ms | 448 ms |
| **Max** | 2,345 ms | 637 ms |
| **INIT Phase Mean** | 1,462 ms | 0 ms |

> Lambda's variance is **125x higher** than Docker — cold starts make it unpredictable

---

## 💰 Cost Analysis

![Cost Analysis](cost_analysis.png)

| Requests/Day | Lambda Cost | Docker Cost | Winner |
|---|---|---|---|
| 10 | $0.000064 | $0.2496 | ✅ Lambda |
| 100 | $0.000644 | $0.2496 | ✅ Lambda |
| 1,000 | $0.006442 | $0.2496 | ✅ Lambda |
| 5,000 | $0.032208 | $0.2496 | ✅ Lambda |
| 10,000 | $0.064415 | $0.2496 | ✅ Lambda |
| 50,000 | $0.322077 | $0.2496 | ✅ Docker EC2 |
| 100,000 | $0.644155 | $0.2496 | ✅ Docker EC2 |

---

## 🎯 The Key Finding

```
╔══════════════════════════════════════════════════════╗
║         COST CROSSOVER POINT: ~38,760 req/day        ║
║                                                      ║
║   Below 38,760/day  →  Lambda is cheaper  ✅         ║
║   Above 38,760/day  →  Docker EC2 cheaper ✅         ║
║                                                      ║
║   INIT phase = $3.12 per 1,000 requests              ║
║   (previously $0.00 in ALL prior research)           ║
╚══════════════════════════════════════════════════════╝
```

---

## 📁 Repository Structure

```
cloud-research/
│
├── lambda-api/
│   ├── app.py                  # Lambda function (Python 3.11)
│   └── function.zip            # Deployment package
│
├── docker-api/
│   ├── app.py                  # Flask API (identical logic)
│   ├── Dockerfile              # Container definition
│   └── requirements.txt        # Dependencies
│
├── results/
│   ├── experiment.py           # 100-run automated benchmark script
│   ├── cost_analysis.py        # Cost modeling + crossover calculation
│   └── benchmark_results.csv   # Raw data — all 100 runs
│
└── README.md
```

---

## 🚀 Reproduce This Experiment

### Prerequisites
- AWS account (Free Tier works)
- Python 3.11
- Docker Desktop

### Step 1 — Deploy Lambda
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
```

### Step 2 — Deploy Docker on EC2
```bash
# Launch EC2 t3.micro on AWS Console
# SSH in, then:
cd docker-api
docker build -t research-api .
docker run -d -p 5000:5000 research-api
```

### Step 3 — Run the Benchmark
```bash
cd results
pip install requests
python experiment.py      # runs 100 requests, saves CSV
python cost_analysis.py   # calculates crossover point
```

---

## 🔑 Why This Matters

**For developers:**
Lambda saves you ~$88/month vs EC2 at 1,000 req/day. But at 50,000+ req/day, EC2 is cheaper — and no tool was telling you this before August 2025.

**For DevOps engineers:**
Every cost calculator, every AWS blog post, every comparison article still uses the old billing model. This gives you updated numbers with real data.

**For researchers:**
This is the first empirical study to incorporate AWS Lambda's August 2025 INIT phase billing change into a cost crossover analysis. 15 papers reviewed — zero accounted for it.

---

## 🛠 Tech Stack

![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=flat&logo=awslambda&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon_EC2-FF9900?style=flat&logo=amazonec2&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)

---

## 📬 Contact

**Muhammad Moazzam Hafeez**
FAST NUCES — Department of Computer Science, Islamabad, Pakistan
📧 i221093@nu.edu.pk
🔗 [GitHub](https://github.com/MoazzamHafeez1093)

---

*Research conducted March 2026*