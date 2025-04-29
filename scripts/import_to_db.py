## 1

import pandas as pd
import sqlite3
# Read Excel file
excel_file = "D:/university/sem 8/Data/Final Project/Project_P2_810100207_810100247_810102480/database/dog_images_data_table.xls"  # Update with the path to your Excel file
df = pd.read_excel(excel_file)

# Replace spaces and special characters in column names for SQL compatibility
df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Connect to SQLite database (creates DogImages.db if it doesn't exist)
conn = sqlite3.connect('DogImages.db')

# Write the DataFrame to SQLite
df.to_sql('DogImages', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Data imported successfully into DogImages.db")

# Verify the data
conn = sqlite3.connect('DogImages.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM DogImages LIMIT 5")
print("\nFirst 5 rows of DogImages table:")
for row in cursor.fetchall():
    print(row)
conn.close()