# QA Automation & Performance Testing Framework

This repository contains my personal **QA portfolio project**, where I am building both **API performance tests** and a **UI automation framework**.

## 🚀 Features
- **API Performance Testing** with [Locust](https://locust.io/)  
- **API Automation** using **Python + PyTest** (modular tests & reusable fixtures)  
- **UI Automation** *(planned)* with **Playwright + PyTest**  
- Configurable via `.env` file (see `.env.example`)  
- Easy to integrate into CI/CD pipelines  

## 📂 Structure
*(project folders will be updated as framework grows)*  

## ▶️ Running Tests
- Run **PyTest**  
  ```bash
  pytest -v

Run Locust load test


locust -f performance/locustfile.py --host=https://your-environment-url.com

