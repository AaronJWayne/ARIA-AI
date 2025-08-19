import streamlit as st
import requests
import os

# Your API Key - REPLACE THIS LINE WITH YOUR REAL KEY
API_KEY = "a4dfb1653a3447d6a944e09b58552213"

# --- GPT-5 API Call Function: This is the "messenger" that sends our request ---
def call_gpt5_api(prompt):
    """Sends a prompt to the GPT-5 API and returns the response."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-5", # We're using the gpt-5 model
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://api.aimlapi.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status() # This checks for errors
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling GPT-5 API: {e}")
        return None
    except (KeyError, IndexError):
        st.error("Invalid response from GPT-5 API.")
        return None

# --- Mock Data for the Hackathon (Our fake list of non-profits) ---
NON_PROFITS_DB = [
    {"name": "Community Kitchen A", "needs": ["fresh produce", "meat", "dairy"], "location": "Downtown"},
    {"name": "Shelter B", "needs": ["ready-to-eat items", "pastries"], "location": "Uptown"},
    {"name": "Meals on Wheels C", "needs": ["bakery items", "prepared meals"], "location": "Downtown"}
]

# --- Streamlit UI: This is what builds our website page ---
st.title("AЯIA: Advanced Recovery, Impact Agent")
st.header("Your AI-Powered Partner for Food Waste Solutions")

# --- Feature 1: AI-Driven Predictive Insights Form ---
st.subheader("1. Proactive Waste Reduction")
st.write("Input your business data to get AI-driven insights on how to reduce waste.")

with st.form("waste_form"):
    item = st.text_input("Item (e.g., Bananas)", help="The type of food item.")
    sold = st.number_input("Sold (kg)", min_value=0, help="How much of this item was sold.")
    wasted = st.number_input("Wasted (kg)", min_value=0, help="How much was wasted.")
    submitted_waste = st.form_submit_button("Get AI Insights")

if submitted_waste: # This runs only when the button is clicked
    prompt = f"""
    Act as an Experienced Supply Chain and Inventory Analyst.
    Analyze the following perishable food waste data to identify patterns and provide actionable recommendations. Your output should be a single, concise paragraph with a clear heading.
    DATA:
    - Item: {item}
    - Sold: {sold} kg
    - Wasted: {wasted} kg
    - Historical data: (Simulate this by focusing on the current numbers)
    Instructions: Identify patterns and suggest a specific strategy to reduce waste (e.g., 'run a flash sale' or 'adjust tomorrow's order').
    """
    st.write("Generating insights with GPT-5...")
    insights = call_gpt5_api(prompt)
    if insights:
        st.success("Insights from GPT-5:")
        st.write(insights)

# --- Feature 2: Intelligent Matching Engine Form ---
st.subheader("2. Intelligent Surplus Matching")
st.write("List your surplus food, and AЯIA will find the best non-profit match.")

with st.form("surplus_form"):
    surplus_item = st.text_input("Surplus Item (e.g., Day-old pastries)", help="What food item is available.")
    quantity = st.number_input("Quantity", min_value=0, help="How many units are available.")
    expiry = st.text_input("Expiry Date (e.g., Tomorrow)", help="The date the item expires.")
    submitted_surplus = st.form_submit_button("Find Non-Profit Match")

if submitted_surplus: # This runs only when the button is clicked
    non_profits_string = "\n".join([
        f"- Name: {np['name']}, Needs: {', '.join(np['needs'])}, Location: {np['location']}"
        for np in NON_PROFITS_DB
    ])
    prompt = f"""
    Act as a Logistics and Matching Agent for a Food Recovery Platform.
    Find the single best non-profit match for the following surplus food listing. Your output should be the name of the top-matched non-profit and a brief one-sentence justification.
    SURPLUS LISTING:
    - Item: {surplus_item}
    - Quantity: {quantity} units
    - Expiry Date: {expiry}
    - Location: Downtown
    AVAILABLE NON-PROFITS:
    {non_profits_string}
    Instructions: Evaluate the non-profits based on item compatibility, pickup availability (assume all are available), and proximity.
    """
    st.write("Finding best match with GPT-5...")
    match = call_gpt5_api(prompt)
    if match:
        st.success("Match Result:")
        st.write(match)