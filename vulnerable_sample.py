import sqlite3

# --- STITCH TEST FILE ---
# HACKATHON TEST CASE: DO NOT DEPLOY 
# This file is used to demonstrate the "Stitch" Agentic Audit workflow.
# It contains intentional vulnerabilities (SQLi, PII leaks) for testing.

API_KEY = "AKIA-FAKE-STITCH-KEY-12345"  # Hardcoded Secret
USER_EMAIL = "test.user@joburg-fintech.co.za"  # PII (South African Domain)

def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SQL Injection Vulnerability (String formatting instead of parameters)
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    
    cursor.execute(query)
    return cursor.fetchone()

print("System initialized...")