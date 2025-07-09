import sys, csv, sqlite3, re

filename = sys.argv[1]
input_code = sys.argv[2].lower().replace(" ", "").replace("_", "")
input_desc = sys.argv[3].lower().replace(" ", "").replace("_", "")

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS icd_codes (
    code TEXT PRIMARY KEY,
    description TEXT
)
""")

# Load CSV header
with open(filename, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    normalized_headers = {re.sub(r'[\s_]', '', h.lower()): h for h in headers}

    code_col = normalized_headers.get(input_code)
    desc_col = normalized_headers.get(input_desc)

    if not code_col or not desc_col:
        print("❌ Column names not matched in CSV.")
        print("🧠 Available headers:", headers)
        exit(1)

    count = 0
    for row in reader:
        code = row.get(code_col, "").strip()
        desc = row.get(desc_col, "").strip()
        if code and desc:
            cursor.execute("INSERT OR IGNORE INTO icd_codes VALUES (?, ?)", (code, desc))
            count += 1

conn.commit()
conn.close()
print(f"✅ Imported {count} ICD entries from {filename} using columns: {code_col}, {desc_col}")
