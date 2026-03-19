import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud import storage
from google.adk.agents import LlmAgent

# CRITICAL FIX: Robustly load the .env file from the exact directory this script lives in
current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(current_dir, ".env"))

# ==========================================
# 1. DYNAMIC BIGQUERY TOOL (Structured Data)
# ==========================================
def get_customer_metrics(company_identifier: str) -> str:
    """
    Retrieves structured billing and usage metrics for a specific customer from BigQuery.
    
    Args:
        company_identifier: The exact identifier/name of the company.
    """
    client = bigquery.Client(project=os.environ.get("BQ_PROJECT_ID"))
    
    dataset = os.environ.get("BQ_DATASET_ID")
    table = os.environ.get("BQ_TABLE_ID")
    id_col = os.environ.get("BQ_IDENTIFIER_COLUMN")
    metrics = os.environ.get("BQ_METRIC_COLUMNS")
    
    query = f"""
        SELECT {metrics}
        FROM `{os.environ.get('BQ_PROJECT_ID')}.{dataset}.{table}`
        WHERE {id_col} = @identifier
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("identifier", "STRING", company_identifier)]
    )
    
    try:
        results = client.query(query, job_config=job_config).result()
        records = [dict(row) for row in results]
        
        if not records:
            return json.dumps({"error": f"No data found for: {company_identifier}"})
            
        for k, v in records[0].items():
            if hasattr(v, 'isoformat'):
                records[0][k] = v.isoformat()
                
        return json.dumps(records[0]) 
    except Exception as e:
        return json.dumps({"error": str(e)})

# ==========================================
# 2. GCS SEARCH TOOL (Unstructured Data)
# ==========================================
def search_support_tickets(company_name: str) -> str:
    """
    Searches the customer support ticket repository for recent complaints or issues 
    related to the specified company.
    
    Args:
        company_name: The exact name of the company to search for.
    """
    client = storage.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    bucket = client.bucket(os.environ.get("GCS_TICKETS_BUCKET"))
    blobs = bucket.list_blobs(prefix="support_tickets/")
    results = []
    
    for blob in blobs:
        content = blob.download_as_text()
        if company_name.lower() in content.lower():
            results.append(content)
            
    if not results:
        return "No recent support tickets found."
    return "\n---\n".join(results)

# ==========================================
# 3. GENERIC SWEEP TOOL (Text-to-SQL)
# ==========================================
def find_accounts_by_condition(sql_where_clause: str, limit: int = 5) -> str:
    """
    Searches the customer database using a custom SQL WHERE clause.
    
    Args:
        sql_where_clause: A valid BigQuery SQL condition using ONLY the available metric columns.
        limit: The maximum number of results to return (default 5).
    """
    client = bigquery.Client(project=os.environ.get("BQ_PROJECT_ID"))
    
    dataset = os.environ.get("BQ_DATASET_ID")
    table = os.environ.get("BQ_TABLE_ID")
    id_col = os.environ.get("BQ_IDENTIFIER_COLUMN")
    metrics = os.environ.get("BQ_METRIC_COLUMNS")
    
    query = f"""
        SELECT {id_col}, {metrics}
        FROM `{os.environ.get('BQ_PROJECT_ID')}.{dataset}.{table}`
        WHERE {sql_where_clause}
        LIMIT {limit}
    """
    
    try:
        results = client.query(query).result()
        records = [dict(row) for row in results]
        
        if not records:
            return json.dumps({"message": "No accounts found matching those conditions."})
            
        for row in records:
            for k, v in row.items():
                if hasattr(v, 'isoformat'):
                    row[k] = v.isoformat()
        return json.dumps(records)
        
    except Exception as e:
        return json.dumps({"error": f"Invalid SQL condition: {str(e)}"})

# ==========================================
# 4. AGENT ASSEMBLY 
# ==========================================
dynamic_instruction = f"""
{os.environ.get('AGENT_ROLE')} {os.environ.get('AGENT_OBJECTIVE')}

You have access to a database with the following structure:
- Identifier Column: {os.environ.get('BQ_IDENTIFIER_COLUMN')}
- Available Metric Columns: {os.environ.get('BQ_METRIC_COLUMNS')}

Follow these rules:
1. If a user asks to find or list accounts based on conditions, use the `find_accounts_by_condition` tool. Write a valid SQL WHERE clause using ONLY the Available Metric Columns listed above.
2. If a user asks to analyze a specific account, use `get_customer_metrics` and then `search_support_tickets`.
3. Synthesize the data you gather to determine if they are a churn risk and draft personalized outreach.
"""

# CRITICAL FIX: The ADK runner specifically looks for an instance assigned to the variable 'agent'
agent = LlmAgent(
    name="GenericChurnAgent",
    model="gemini-2.5-pro", 
    instruction=dynamic_instruction, 
    tools=[get_customer_metrics, search_support_tickets, find_accounts_by_condition]
)
