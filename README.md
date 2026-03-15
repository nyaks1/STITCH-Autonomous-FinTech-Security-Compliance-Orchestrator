# Stitch: Autonomous Agentic Security for FinTech

> **Hackathon Submission:** Microsoft AI Agent Hackathon 2026
> **Category Focus:** Agentic DevOps, Best Enterprise Solution, Best Multi-Agent System

---

## The Problem
FinTech innovation in South Africa moves at lightning speed, but **POPIA** compliance and security often lag behind. Traditional static analysis tools flag syntax errors but miss "contextual" risks—such as storing a South African ID number in an unencrypted Azure SQL table or exposing a database via a misconfigured Network Security Group. Manual audits are slow, expensive, and a bottleneck to enterprise scaling.

## The Solution
**Stitch** is an AI-powered Security & Compliance team that lives in your development "Inner Loop." It utilizes a multi-agent orchestration to find, justify, and fix security risks across both **Source Code** and **Live Azure Infrastructure** before they reach production.

### The Agents
* **The Scout (Red Team):** Performs deep Static Analysis on local code and Live Analysis on Azure. Using **Azure MCP**, it identifies PII leaks and audits live Network Security Groups (NSGs) for public exposure.
* **The Judge (Governance):** A RAG-powered agent connected to **Microsoft Foundry**. It queries official POPIA/GDPR documentation to provide a legal "Verdict," assigning risk levels and citing specific regulatory clauses.
* **The Architect (DevOps):** The "closer" that synthesizes the audit and verdict to draft a secure patch, following **GitHub Copilot Agent Mode** patterns to prepare a remediation Pull Request.

---

## Hero Technologies Used
* **Microsoft Agent Framework:** Orchestrates the complex sequential handoff and shared memory between the specialized agents.
* **Microsoft Foundry (Knowledge Base):** Serves as the centralized "Law Book," allowing agents to ground their reasoning in real-world regulatory PDFs.
* **Azure MCP (Model Context Protocol):** Provides the agents with "hands" to interact securely with the local filesystem and live Azure Management APIs.
* **Azure Developer CLI (azd):** Enables standardized, repeatable "one-click" deployment of the entire agentic infrastructure.

---

### Features
- **Stitch-Scout:** Performs static analysis on local Python files and audits live Azure NSG configurations.
- **Stitch-Judge:** Grounded in POPIA & GDPR standards to provide real-time compliance verdicts.
- **Stitch-Architect:** Generates production-ready, secure patches for identified vulnerabilities.

### Tech Stack
- **Azure AI Foundry:** Agent orchestration and model hosting.
- **GPT-4o:** The reasoning engine for security and legal analysis.
- **Python & Bash:** Core logic and infrastructure auditing tools.

---

## Architecture Diagram


---

## Setup & Installation

1.  **Clone the Repo:**
    ```bash
    git clone git@github.com:nyaks1/STITCH-Autonomous-FinTech-Security-Compliance-Orchestrator.git
    cd STITCH-Autonomous-FinTech-Security-Compliance-Orchestrator
    ```

2.  **Environment Setup:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure Secrets:**
    Create a `.env` file in the root directory:
    ```text
    AZURE_OPENAI_ENDPOINT="your-endpoint"
    PROJECT_CONNECTION_STRING="your-foundry-connection-string"
    AZURE_SUBSCRIPTION_ID="your-subscription-id"
    ```

4.  **Deploy Infrastructure:**
    ```bash
    azd auth login
    azd up
    ```
### 📦 Installation
1. Clone the repo.
2. Add your `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` and `PROJECT_CONNECTION_STRING` to `.env`.
3. Run `python main.py`.

## Running the Audit
To execute the end-to-end security lifecycle on a target file (e.g., your Street Ledger source):
```bash
python main.py