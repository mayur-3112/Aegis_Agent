# 🛡️ Aegis Core Engine

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


