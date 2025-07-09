import sqlite3
import re

db_path = "instance/icdcodes.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all ICD codes
cursor.execute("SELECT id, code FROM icd_code")
icd_codes = cursor.fetchall()

medical_count = 0
rvs_count = 0

for icd_id, code in icd_codes:
    if re.match(r"^[a-zA-Z]", code):
        cursor.execute("UPDATE icd_code SET category = ? WHERE id = ?", ("Medical", icd_id))
        medical_count += 1
    elif re.match(r"^[0-9]", code):
        cursor.execute("UPDATE icd_code SET category = ? WHERE id = ?", ("RVS", icd_id))
        rvs_count += 1

conn.commit()
conn.close()

print(f"Updated {medical_count} codes to category 'Medical'.")
print(f"Updated {rvs_count} codes to category 'RVS'.")
print("Database categories updated successfully.")