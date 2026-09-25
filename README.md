# 🛡️ Spam-classifier - AI Message Security Analyzer
live demo - https://cybersift.streamlit.app/


An AI-powered spam and scam detection system that analyzes
messages and classifies them into three security levels:

- 🟢 SAFE
- 🟡 SUSPICIOUS
- 🔴 DANGEROUS

The system combines Machine Learning and cybersecurity
rule-based analysis to evaluate potentially harmful messages.

## Features

- Machine Learning spam detection
- Multinomial Naive Bayes
- TF-IDF text vectorization
- Cybersecurity rule engine
- Spam probability calculation
- Three-level risk classification
- Suspicious URL detection
- Credential/OTP detection
- Financial keyword detection
- Urgency detection
- Prize/reward scam detection
- Streamlit web interface

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- TF-IDF
- Multinomial Naive Bayes
- Regular Expressions

## How It Works

User Message
       ↓
Text Processing
       ↓
TF-IDF
       ↓
Naive Bayes
       ↓
Spam Probability
       ↓
Cybersecurity Rule Engine
       ↓
Risk Analysis
       ↓
SAFE / SUSPICIOUS / DANGEROUS

## Risk Levels

### 🟢 SAFE

The message has a low estimated spam/security risk.

### 🟡 SUSPICIOUS

The message contains characteristics that
may indicate spam, phishing or unwanted content.

### 🔴 DANGEROUS

The message has a high estimated risk.
Users should avoid clicking suspicious links
or sharing sensitive information.

## Machine Learning

The project uses:

TF-IDF
- Converts text into numerical features.
- Gives greater importance to informative words.

Multinomial Naive Bayes
- Learns patterns from spam and legitimate messages.
- Produces a spam probability.

## Cybersecurity Rule Engine

The rule engine checks for indicators such as:

- Urgent requests
- Suspicious URLs
- Password requests
- OTP requests
- PIN/CVV requests
- Financial keywords
- Prize/lottery messages
- Account verification requests
