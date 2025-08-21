# Aegis Agent (MVP 1)

**A Host-based Intrusion Detection System (HIDS) for File Integrity Monitoring**

This repository contains the first Minimum Viable Product (MVP) of the Aegis Agent, a defensive security tool designed to monitor a server for unauthorized file changes. This project serves as a practical demonstration of skill in system internals, cryptographic principles, and defensive engineering.

### Key Features:

* **File Integrity Baseline:** The agent creates a secure cryptographic baseline of a monitored system's file hashes (SHA-256) and stores them in a `baseline.json` file.
* **Continuous Monitoring:** The agent runs a continuous loop that periodically re-scans the system and compares the current file hashes against the established baseline.
* **Real-time Alerting:** Upon detecting any unauthorized changes (additions, deletions, or modifications), the agent sends a real-time alert via a `POST` request to a central server.
* **Centralized Logging:** The project includes a simple Flask server with an `/alert` endpoint that receives, processes, and logs all incoming security alerts for centralized auditing.

### Project Components:

* `agent.py`: The core Python script that performs baseline generation and continuous file integrity monitoring.
* `server.py`: A lightweight Flask application that acts as the central alert-receiving and logging server.
* `requirements.txt`: A list of all necessary Python dependencies to run the project.

This project was developed as a team mini-project for the V Semester (2025-26) and aligns with the goal of building practical, impactful cybersecurity solutions.
