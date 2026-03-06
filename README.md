# ⚡ AWS Lambda vs Docker on EC2
## The Cost Impact of INIT Phase Billing on Serverless Deployment Decisions

> **TL;DR:** AWS changed how they bill Lambda in August 2025. Nobody has studied what this means for cost decisions. I did. The answer: Lambda becomes more expensive than Docker at ~38,760 requests/day — a threshold that prior models completely missed.

---

## 📄 Research Paper
**Title:** The Cost Impact of AWS Lambda's INIT Phase Billing on Serverless vs Container Deployment Decisions: An Empirical Analysis

**Author:** Muhammad Moazzam Hafeez — FAST NUCES Islamabad

**Status:** 🔄 Under Review — IEEE 2026

---

## 🧠 The Problem In Plain English

When you use AWS Lambda, sometimes it "wakes up cold" — this delay is called a **cold start** or **INIT phase.**

For years, this was just a speed problem. Annoying, but free.

**On August 1, 2025, AWS started charging for it.**

Every paper ever written about Lambda costs missed this. Every cost model, every comparison, every benchmark — all of them assumed INIT phase = free.

This research fixes that.

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

## 📊 Results

### Response Time
| Metric | Lambda | Docker EC2 |
|---|---|---|
| **Mean** | 1,463 ms | 495 ms |
| **Median** | 1,297 ms | 491 ms |
| **Std Deviation** | 383 ms | 34 ms |
| **Min** | 1,095 ms | 448 ms |
| **Max** | 2,345 ms | 637 ms |

> Docker is **2.96x faster** and **125x more consistent** than Lambda

### 💰 Cost at Different Traffic Levels
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
│   ├── app.py              # Lambda function (Python 3.11)
│   └── function.zip        # Deployment package
│
├── docker-api/
│   ├── app.py              # Flask API (identical logic)
│   ├── Dockerfile          # Container definition
│   └── requirements.txt    # Dependencies
│
├── results/
│   ├── experiment.py       # 100-run automated benchmark script
│   ├── cost_analysis.py    # Cost modeling + crossover calculation
│   └── benchmark_results.csv  # Raw data from all 100 runs
│
└── README.md
```

---

## 🚀 Reproduce This Experiment

### Prerequisites
- AWS account with Lambda + EC2 access
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
cd docker-api
# Launch EC2 t3.micro, SSH in, then:
docker build -t research-api .
docker run -d -p 5000:5000 research-api
```

### Step 3 — Run Benchmark
```bash
cd results
pip install requests
python experiment.py
python cost_analysis.py
```

---

## 🔑 Why This Matters

**For developers:** If your app gets ~1,000 req/day, Lambda saves you $88/month vs EC2. But if you're at 50,000+ req/day, EC2 saves you money — and prior tools wouldn't have told you this.

**For DevOps engineers:** Every cost calculator, every AWS blog post, every comparison article still uses the old billing model. This research gives you the updated numbers.

**For researchers:** This is the first empirical study to incorporate AWS Lambda's August 2025 INIT phase billing change into a cost crossover analysis.

---

## 🛠 Tech Stack

![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=flat&logo=awslambda&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![EC2](https://img.shields.io/badge/Amazon_EC2-FF9900?style=flat&logo=amazonec2&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)

---

## 📬 Contact

**Muhammad Moazzam Hafeez**
FAST NUCES — Department of Computer Science, Islamabad
📧 i221093@nu.edu.pk
🔗 [GitHub](https://github.com/MoazzamHafeez1093)

---

*Research conducted March 2026 | Paper under IEEE review*