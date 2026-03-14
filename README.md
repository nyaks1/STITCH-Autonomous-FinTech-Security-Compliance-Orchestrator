# Stitch: Autonomous Agentic Security for FinTech

> **Hackathon Submission:** Microsoft AI Agent Hackathon 2026
> **Category Focus:** Agentic DevOps, Best Enterprise Solution, Best Multi-Agent System

## The Problem
Building FinTech apps like *Street Ledger* requires rigorous security and compliance auditing. Manual reviews are slow, and traditional CI/CD tools only catch "dumb" bugs. Developers need an intelligent teammate that understands **POPIA/GDPR regulations** and can fix vulnerabilities before they reach production.

##  The Solution
**Stitch** is an AI-powered Security & Compliance team that lives in your "Inner Loop." It uses a multi-agent orchestration to find, justify, and fix security risks.

###  The Agents
- **The Scout (Red Team):** Uses **Azure MCP** to scan the codebase for PII leaks, SQL injections, and weak encryption.
- **The Judge (Governance):** Queries **Microsoft Foundry** to cross-reference Scout's findings against actual Financial Compliance Laws.
- **The Architect (DevOps):** Triggers **GitHub Copilot Agent Mode** to write the patch and open a Pull Request.

##  Hero Technologies Used
- **Microsoft Agent Framework:** Orchestrates the complex handoffs between the Scout, Judge, and Architect.
- **Azure MCP (Model Context Protocol):** Provides the agents with "hands" to read local files and Azure SQL schemas.
- **Microsoft Foundry:** Acts as the centralized "Law Book" for enterprise compliance data.
- **GitHub Copilot Agent Mode:** Automates the remediation of identified security flaws.

##  Architecture Diagram
[Insert Image Here - I can help you describe this for a diagram tool later]

##  Setup & Installation
1. `git clone git@github.com:nyaks1/STITCH-Autonomous-FinTech-Security-Compliance-Orchestrator.git`
2. `pip install -r requirements.txt`
3. `azd auth login` && `azd up` (Deploys the infrastructure to Azure)