#  Aegis Core Engine

A blazingly fast, command-line File Integrity Monitoring (FIM) tool built with Python and the state-of-the-art BLAKE3 cryptographic hash function.

---

## Overview

Aegis Core Engine is the foundational component of a multi-semester cybersecurity initiative. For the 5th semester, this project serves two primary purposes:

1.  **As a Product:** A powerful, standalone FIM utility for security professionals to detect unauthorized changes in critical files.
2.  **As an Instrument:** A scientific tool for conducting a comparative performance analysis of modern cryptographic hash functions, with the goal of publishing our findings in a peer-reviewed journal like IEEE.

This project prioritizes performance, professional software architecture, and robust error handling.

---

## Core Features

-   **High-Speed Hashing:** Utilizes the **BLAKE3** algorithm for exceptional performance, far exceeding older standards like SHA-256.
-   **Modular Architecture:** A clean, decoupled engine design (Discovery, Baseline, Integrity) that allows for robust testing and future scalability.
-   **Intelligent Discovery:** A configurable engine to precisely target files and directories for monitoring, with support for include/exclude rules.
-   **Professional CLI:** A clear and intuitive command-line interface for easy operation.

---

## Project Architecture

The engine is built on a professional, modular design that ensures each component is independent and testable.

```text
[ User runs `agent.py` ]
       │
       ├─> [ Cockpit (argparse) ] -> Interprets user commands (--init, --check)
       │
       ├─> [ Discovery Engine ] -> Reads config, returns list of files to scan
       │
       ├─> [ Baseline Engine ] -> Hashes file list, returns a baseline dictionary
       │
       └─> [ Integrity Engine ] -> Compares two baselines, returns a results dictionary
```

## Getting Started
### Prerequisites

- Python 3.9+
- pip and venv

## Installation
- Clone the repository:

```text

git clone [https://github.com/mayur-3112/Aegis_Agent.git](https://github.com/mayur-3112/Aegis_Agent.git)
cd Aegis_Agent
```

- Create and activate the virtual environment:

```text

python3 -m venv venv
source venv/bin/activate

```

- Install dependencies:

```text

pip install -r requirements.txt
```


## Usage

The Aegis Core Engine is operated via the command line from the project's root directory.

- Configure Your Scan:
First, create your personal configuration file by copying the template:
cp config.example.json config.json
Now, you can edit the config.json file to specify which directories to monitor and which patterns to exclude for your local machine.

- Initialize the Baseline:
This command scans the target files for the first time and creates the baseline.json source of truth.

```bash

python agent.py --init

```

- Perform an Integrity Check:
Run this command to scan the files again and compare them against the saved baseline.

```text

python agent.py --check

```

## Project Roadmap

This standalone tool is the foundation for a larger vision.

- Phase 1 (6th Sem): Evolve into a distributed client-server "Sentinel Network."

- Phase 2 (7th Sem): Add an "Active Response" module, upgrading the system to a full Intrusion Prevention System (IPS).

### Development Methodology & Use of AI as a Force Multiplier

The Aegis Core Engine was developed using a professional, agile, and test-driven methodology. A core component of our strategy was the disciplined use of AI-powered Large Language Models (LLMs) as a "force multiplier" to accelerate the development of boilerplate code and first-draft implementations.

Our team operated under a strict protocol for AI-assisted development, designated "The Cyborg Engineer's Protocol":

1.  **Human as Architect:** All architectural decisions, function contracts, and mission-critical logic were designed exclusively by the human engineers. The AI served as an implementation tool, not a strategic partner.
2.  **Mandatory Code Ownership:** No line of AI-generated code was committed until the responsible engineer could explain its function, logic, and necessity in detail.
3.  **Verification Through Testing:** All AI-assisted modules were subjected to rigorous, human-written unit tests to prove their correctness and resilience. The act of writing the test served as the final proof of the engineer's understanding and ownership.

This professional, transparent, and test-driven approach allowed our team to operate at a velocity and quality level that would be unattainable through purely manual methods, enabling us to focus our human intellect on the more complex challenges of system architecture, algorithmic analysis, and experimental design.


## Authors
- Mayur: Project Lead & System Architect

- Chetan: Lead Engineer (Integrity Engine)

- Harshit: Module Developer (Discovery Engine)

- Keshav: Module Developer (Baseline Engine)
