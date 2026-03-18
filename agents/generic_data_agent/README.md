# 📊 Generic Data Insights & Orchestration Agent

This repository contains an enterprise-grade, code-first Gemini agent built with the **Google Agent Development Kit (ADK)**. 

This agent dynamically orchestrates queries across structured databases (Google BigQuery) and unstructured document stores (Google Cloud Storage) to answer complex, multi-step business questions. 

## 🏗️ Architecture Design
This agent strictly separates **Code** from **Configuration**. 
You do not need to modify the Python code to make this work. The agent reads your specific BigQuery schema and Agent Persona directly from the `.env` configuration file, dynamically generating its SQL and reasoning context at runtime.

---

## 🚀 Deployment & Testing Guide

Follow these exact steps to deploy and test this agent in your Google Cloud environment using Cloud Shell.

### Prerequisite: Enable APIs
Ensure the following APIs are enabled in your Google Cloud Project:
*   Vertex AI API (`aiplatform.googleapis.com`)
*   BigQuery API (`bigquery.googleapis.com`)
*   Cloud Storage API (`storage.googleapis.com`)

### Step 1: Clone the Repository
Open [Google Cloud Shell](https://shell.cloud.google.com/) in your target project and run:
```bash
git clone [https://github.com/](https://github.com/)[YOUR-GITHUB-USERNAME]/gemini-enterprise-agent-repository.git
cd gemini-enterprise-agent-repository/agents/generic_data_agent
```

## Step 2: Set Up Virtual Environment & Dependencies
It is best practice to isolate your Python environment.

```bash
python3 -m venv agent-env
source agent-env/bin/activate
pip install -r requirements.txt
```
## Step 3: Authenticate (Application Default Credentials)
The agent uses your secure IAM identity to interact with Vertex AI and BigQuery. Do not use API keys.

``` bash
gcloud auth application-default login
```
*(Follow the prompt to authenticate your user account via the browser link).*

## Step 4: Configure Your Data (The .env File)
Copy the template configuration file to create your active .env file:

```bash
cp .env.template .env
```
Open the .env file using the Cloud Shell editor or nano:

```Bash
nano .env
```
* **CRITICAL**: Update the variables to match your exact Google Cloud Project ID, BigQuery Dataset, BigQuery Table, and specific Column Names. Save and exit (Ctrl+O, Enter, Ctrl+X if using nano).

## Step 5: Execute the Agent
Run the execution script to trigger the agent's orchestration loop:

```bash
python run.py
```
Watch as the agent dynamically writes SQL based on your .env schema, queries BigQuery, searches Cloud Storage, and synthesizes the final business response.
