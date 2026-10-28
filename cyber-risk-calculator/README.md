# Cyber Risk Calculator

A simple Python tool that helps small businesses estimate the yearly financial
cost of cyber risks such as ransomware or phishing, and rank which risks to fix first.

## Features
- Menu-driven command-line interface
- Input validation (wrong entries never crash the program)
- Calculates Single Loss Expectancy (SLE) and Annual Loss Expectancy (ALE)
- Rates each risk as LOW, MEDIUM or HIGH
- Ranked report with total expected yearly loss
- Saves the report to `report.csv`
- Sample data included
- Automated tests

## How it works
- SLE = asset value x exposure % (loss from one incident)
- ALE = SLE x incidents per year (expected loss per year)
- HIGH: ALE >= 100,000 | MEDIUM: ALE >= 20,000 | LOW: below that

## Requirements
Python 3.8 or newer. No extra libraries needed.

## Setup and run
```
git clone https://github.com/YOUR-USERNAME/cyber-risk-calculator.git
cd cyber-risk-calculator
python risk_calculator.py
```
On Mac/Linux use `python3` instead of `python`.

Quick demo: choose **2** (load sample data), then **3** (view report), then **4** (save report).

## Run the tests
```
python -m unittest -v
```

## Project files
| File | Purpose |
|------|---------|
| `risk_calculator.py` | The program |
| `test_risk_calculator.py` | Automated tests |
| `sample_risks.csv` | Example data |
| `requirements.txt` | Dependencies (none yet) |

## Roadmap
Charts, recommended security controls, and a web interface.

## Author
Your Name
