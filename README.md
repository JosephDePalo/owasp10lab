# OWASP Top 10 Lab

This project contains intentionally vulnerable code that demonstrates examples
of the OWASP Top 10 web application security risks. Each section of the app
highlights a specific vulnerability with minimal code to clearly showcase
the core issue.

## Features

- 🔓 Broken Access Control  
- 🔐 Cryptographic Failures  
- 💉 Injection  
- ⚠️ Insecure Design  
- ⚙️ Security Misconfiguration

## Usage

This app is meant for **local testing and educational use only**. Do **not**
deploy it in a production environment.

### Requirements

- Python 3.x
- Flask
- SQLite3

### Setup

```bash
git clone https://github.com/josephdepalo/owasp10lab.git
cd owasp10lab
pip install -r requirements.txt
python bootstrap.py
```


### Usage

```bash
python app.py
```
```
