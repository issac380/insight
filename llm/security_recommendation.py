# over a fixed interval (or triggered by user, or triggered when X amount is lost), parses through the stolen items database and 
# generate summary and recommendations for product placement, security level, etc.
# consider feeding in floorplan and item location

from test_acceptance.test_utils import view_exited_items
from openai import OpenAI
import os

# Only called by testing functions. Later will implement auto trigger once lost merchandise value exceeds preset
# or manually from the user.
def generate_security_recommendation(db_path='data/exited_items.db', model='gpt-4o-mini'):
    rows = view_exited_items(db_path)
    if not rows:
        return "✅ No stolen items found. No security changes are necessary."

    stats = {}
    for rfid, product, price, time, status, security in rows:
        key = (product.strip(), security.strip())
        stats[key] = stats.get(key, 0) + 1

    theft_summary = "\n".join(
        f"- {count} units of '{product}' stolen with current security: '{security}'"
        for (product, security), count in sorted(stats.items(), key=lambda x: x[1], reverse=True)
    )

    prompt = f"""
You are an AI security analyst for a retail chain.
Based on the list of stolen items and their current security levels, write a security assessment report that includes:

1. 🔼 Recommendations to UPGRADE security if theft is high for under-protected items.
2. 🔽 Suggestions to DOWNGRADE security if no or low theft occurs under strong security.
3. 🎯 Specific advice (e.g., locked display case, RFID tags, employee supervision).
4. Keep the response concise and use bullet points.

Stolen Item Summary:
{theft_summary}

Please begin your analysis below.
"""
    key = os.getenv("OPENAI_API_KEY")
    if key:
        print("✅ API key is set.")
    else:
        print("❌ API key is NOT set.")
        
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a helpful security advisor for retail loss prevention."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()