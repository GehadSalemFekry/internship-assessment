# Coding Assessment Implementation Guide

This repository provides an overview of the coding assessment and instructions for running each component.

## Setup

1. **Create and activate virtual environment**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## Task 1: Unique Timestamp Generator

**Location:** `task_1/generator.py` and `timestamps_tasks.ipynb`

### Approach

- Generate unique random integers using **exponential gap distribution**
- Mathematical property: for uniformly distributed points, gaps follow exponential distribution with rate λ = n / max_value
- O(n) time complexity with no collision checking needed
- Results are sorted by construction (cumulative sum)
- Configurable number of timestamps and range
- CSV output for generated timestamps

### Run

The notebook contains multiple use cases for generating different timestamp datasets:

```bash
# Open the notebook
jupyter notebook timestamps_tasks.ipynb
# or in VS Code, just open timestamps_tasks.ipynb
```

Run the cells to generate datasets. Filenames include a short random suffix to avoid collisions:

- **100k timestamps** in 1 second (1e12 ps) → `data/timestamps_100k_max1e12_<rand>.csv`
- **1M timestamps** in 1 second → `data/timestamps_1000k_max1e12_<rand>.csv`
- **50k timestamps** in 1 second → `data/timestamps_50k_max1e12_<rand>.csv`

### Output Format

CSV files with single column `timestamp`, containing sorted unique integers.

---

## Task 2: Statistical Analysis & Visualization

**Location:** `task_2/analysis.py`

### Approach

Analyze timestamps from CSV files with four complementary statistical views:

1. **Histogram** - Verifies uniform distribution
   - All bins should have similar heights
   - Confirms randomness and even coverage

2. **CDF (Cumulative Distribution Function)** - Verifies ordering
   - Must be monotonically increasing from 0 to 1
   - Confirms all values are unique and sorted
   - Smooth curve indicates uniform distribution

3. **Gap Distribution** - Analyzes spacing between consecutive values
   - Exponential gaps are used during generation to create uniform data
   - Demonstrates the mathematical property underlying uniform distribution

4. **Q-Q Plot** - Compares empirical quantiles to a theoretical uniform distribution
   - Points close to the diagonal indicate a good uniform fit

### Run

Analysis is done inside the notebook using functions in `task_2/analysis.py`.
Each use case loads its CSV file and generates separate plots via:
`plot_histogram`, `plot_cdf`, `plot_gap_distribution`, and `plot_qq`.

### Output

- **Files:** Separate plot images saved to `plots/` with dataset-specific names

---

## Task 3: Stateful Calculator API

**Location:** `task_3/calculator.py`

### Approach

- Build Flask REST API with expression evaluation
- Validate operators before evaluation
- Maintain in-memory history of last 5 calculations
- Handle errors gracefully with clear messages

### Features

✅ Evaluate arithmetic expressions (+ - \* /)  
✅ Operator validation with helpful error messages  
✅ History tracking (last 5 calculations)  
✅ Graceful error handling (division by zero, invalid syntax)  
✅ Rejects any non-digit/operator/space characters (no parentheses)

### Endpoints

**POST /calculate** - Evaluate expression

```bash
curl -X POST http://127.0.0.1:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "10 + 10 + 3 - 5"}'
```

Response (success):

```json
{ "result": "18" }
```

Response (unsupported operator):

```json
{ "error": "Unsupported operators: ^\nSupported operators: + - * /" }
```

**GET /history** - Get last 5 successful calculations

```bash
curl http://127.0.0.1:5000/history
```

Response:

```json
{ "history": ["10 + 10 + 3 - 5 = 18", "5 * 2 = 10"] }
```

**POST /clear-history** - Clear history

```bash
curl -X POST http://127.0.0.1:5000/clear-history
```

**GET /health** - Health check

```bash
curl http://127.0.0.1:5000/health
```

### Run

**Terminal 1 - Start server:**

```bash
python task_3/calculator.py
```

**Terminal 2 - Run tests:**

```bash
python task_3/test_calculator.py
```

### Test Cases Covered

✓ Basic arithmetic (addition, subtraction, multiplication, division)  
✓ Multiple operations in one expression  
✓ Unsupported operators (^, etc.)  
✓ Invalid syntax (incomplete expressions)  
✓ Parentheses are rejected as invalid input  
✓ Division by zero

---

## Summary of Files

```
.
├── task_1/
│   └── generator.py          # Timestamp generation function (exponential gaps)
├── task_2/
│   └── analysis.py           # Statistical analysis & visualization (CSV input)
├── task_3/
│   ├── calculator.py         # Flask API server
│   └── test_calculator.py    # API test suite
├── data/                     # Generated timestamp CSV files (created by notebook)
│   ├── timestamps_100k_max1e12_<rand>.csv
│   ├── timestamps_1000k_max1e12_<rand>.csv
│   └── timestamps_50k_max1e12_<rand>.csv
├── plots/                    # Generated plot images
├── timestamps_tasks.ipynb    # Interactive timestamp generation and analysis
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```
