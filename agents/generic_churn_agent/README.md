# 📊 Generic Churn Analysis Agent

This repository contains a production-ready Google Cloud agent built with the **Agent Development Kit (ADK)**. It dynamically analyzes structured data (BigQuery) and unstructured data (Cloud Storage) to identify customer health and churn risk patterns, without requiring you to write custom SQL.

## ⚙️ Architecture (Bring Your Own Data)
This agent is 100% data-agnostic. It does not contain hardcoded database columns. Instead, it reads your database schema from a `.env` configuration file. You can point this agent at any BigQuery dataset simply by mapping your column names.

---

## 🚀 Step 1: Clone the Repository to Google Cloud Shell
To ensure you have the proper authenticated environment, we recommend deploying this directly from Google Cloud Shell.

1. Open the [Google Cloud Console](https://console.cloud.google.com/).

2. Click the **Activate Cloud Shell** icon (the terminal symbol) in the top right corner.
3. In the terminal, clone this repository and navigate to the agent folder:
   ```bash
   git clone https://github.com/YOUR-GITHUB-USERNAME/gemini-enterprise-agent-repository.git

   cd gemini-enterprise-agent-repository/agents/generic_churn_agent


## 🛠️ Step 2: Configure Your Data Schema
You must tell the agent where your data lives and what the columns are named.

1. Create your active configuration file by copying the template:

```Bash
cp .env.template .env
```
2. Open the file in the Cloud Shell Editor:

```Bash
edit .env
```
3. **CRITICAL**: Update the GOOGLE_CLOUD_PROJECT, BQ_DATASET_ID, BQ_TABLE_ID, BQ_IDENTIFIER_COLUMN, and BQ_METRIC_COLUMNS variables to perfectly match your Google Cloud environment.

## 🧪 Step 3: Test Locally with the ADK UI
Before deploying to production, verify the agent is working correctly using the local ADK Developer Server.

1. Install the required dependencies:

```Bash
pip install -r requirements.txt
```
2. Start the local ADK interface:

```Bash
cd..

adk web
```
3. Cloud Shell will provide a "Web Preview" link. Click it to open the ADK UI in your browser. You can now chat with your agent and visually inspect its tool calls and reasoning process in real-time.

## ☁️ Step 4: Deploy to Vertex AI Agent Engine
Once you are satisfied with the local testing, deploy the agent to Google Cloud's managed Vertex AI Agent Engine for production scaling.

Press Ctrl+C in your terminal to stop the local web server.

1. Ensure your Google Cloud Project has the required APIs enabled (Vertex AI API, Cloud Build API, Cloud Run API).

2. Run the ADK deployment command:

```Bash
adk deploy agent_engine --project=$GOOGLE_CLOUD_PROJECT --region=$GOOGLE_CLOUD_LOCATION ./generic_churn_agent
```

3. The CLI will package your agent, containerize it, and deploy it to Vertex AI. It will output a secure endpoint URL once the deployment is successful.


*(Note: Make sure to replace `YOUR_GITHUB_USERNAME` in the README clone URL with your actual username before committing).*

# 💡 Customization Examples
Because this agent separates the code from the configuration, you can easily adapt it to entirely different business use cases just by modifying the .env file. You do not need to rewrite the Python code.

1. Example 1: Retail & E-Commerce (Cart Abandonment)

* BQ_TABLE_ID=ecommerce_users

* BQ_IDENTIFIER_COLUMN=user_account_id

* BQ_METRIC_COLUMNS=items_in_cart, days_since_last_purchase, lifetime_value_usd

* AGENT_OBJECTIVE="Your goal is to identify users likely to abandon their shopping carts and draft targeted discount emails."

2. Example 2: Gaming & Entertainment (Player Drop-off)

* BQ_TABLE_ID=player_statistics

* BQ_IDENTIFIER_COLUMN=gamer_tag

* BQ_METRIC_COLUMNS=hours_played_weekly, current_level, premium_currency_balance

* AGENT_OBJECTIVE="Your goal is to identify players who are losing engagement and suggest in-game rewards to retain them."

3. Example 3: Logistics & Supply Chain (Vendor Risk)

* BQ_TABLE_ID=supplier_metrics

* BQ_IDENTIFIER_COLUMN=vendor_name

* BQ_METRIC_COLUMNS=average_delay_days, defective_parts_ratio, contract_value

* AGENT_OBJECTIVE="Your goal is to assess supplier reliability, synthesize their performance data with recent email complaints, and draft vendor review notices."


*(Don't forget to swap out the `YOUR_GITHUB_USERNAME` placeholder in the clone URL!)*
