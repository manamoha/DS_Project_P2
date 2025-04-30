import pandas as pd
import sqlite3
import os

# Define paths
excel_file = "D:/university/sem 8/Data/Final Project/Project_P2_810100207_810100247_810102480/database/dog_images_data_table.xls"
db_path = "D:/university/sem 8/Data/Final Project/Project_P2_810100207_810100247_810102480/database/DogImages.db"

# Read Excel file
df = pd.read_excel(excel_file)

# Replace spaces and special characters in column names for SQL compatibility
df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Ensure the database directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to SQLite database (creates DogImages.db in the specified path)
conn = sqlite3.connect(db_path)

# Write the DataFrame to SQLite
df.to_sql('DogImages', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print(f"Data imported successfully into {db_path}")

# Verify the data
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM DogImages LIMIT 5")
print("\nFirst 5 rows of DogImages table:")
for row in cursor.fetchall():
    print(row)
conn.close()