## 2


import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('DogImages.db')

# Define the 5 SQL queries
queries = [
    {
        "name": "Query 1: Dominant Color Distribution Across All Images",
        "sql": """
            SELECT Dominant_Color, 
                   COUNT(*) AS color_count, 
                   GROUP_CONCAT(DISTINCT Breed) AS breeds
            FROM DogImages
            GROUP BY Dominant_Color
            HAVING COUNT(*) > 1
            ORDER BY color_count DESC
            LIMIT 10;
        """
    },
    {
        "name": "Query 2: Top 3 Dominant Colors by Breed",
        "sql": """
            SELECT Breed, 
                   Dominant_Color, 
                   color_count
            FROM (
                SELECT Breed, 
                       Dominant_Color, 
                       COUNT(*) AS color_count,
                       ROW_NUMBER() OVER (PARTITION BY Breed ORDER BY COUNT(*) DESC) AS color_rank
                FROM DogImages
                GROUP BY Breed, Dominant_Color
                HAVING COUNT(*) >= 3
            ) ranked
            WHERE color_rank <= 3
            ORDER BY Breed, color_count DESC;
        """
    },
    {
        "name": "Query 3: Dominant Color and Resolution Patterns",
        "sql": """
            SELECT Dominant_Color, 
                   Resolution, 
                   COUNT(*) AS count,
                   GROUP_CONCAT(DISTINCT Breed) AS breeds
            FROM DogImages
            GROUP BY Dominant_Color, Resolution
            HAVING COUNT(*) >= 3
            ORDER BY count DESC
            LIMIT 15;
        """
    },
    {
        "name": "Query 4: Top 5 Largest Images by Size for Each Breed",
        "sql": """
            SELECT Breed, 
                   Image_File_Name, 
                   Image_Size_KB, 
                   Dominant_Color, 
                   Resolution
            FROM (
                SELECT Breed, 
                       Image_File_Name, 
                       Image_Size_KB, 
                       Dominant_Color, 
                       Resolution,
                       ROW_NUMBER() OVER (PARTITION BY Breed ORDER BY Image_Size_KB DESC) AS size_rank
                FROM DogImages
                WHERE Image_Size_KB IS NOT NULL
                AND Breed IN (
                    SELECT Breed 
                    FROM DogImages 
                    GROUP BY Breed 
                    HAVING COUNT(*) > 10
                )
            ) ranked
            WHERE size_rank <= 5
            ORDER BY Breed, Image_Size_KB DESC;
        """
    },
    {
        "name": "Query 5: Top 5 Images by Resolution for Each Breed",
        "sql": """
            SELECT Breed, 
                   Image_File_Name, 
                   Image_Size_KB, 
                   Dominant_Color, 
                   Resolution,
                   pixel_area
            FROM (
                SELECT Breed, 
                       Image_File_Name, 
                       Image_Size_KB, 
                       Dominant_Color, 
                       Resolution,
                       (CAST(SUBSTR(Resolution, 1, INSTR(Resolution, 'x') - 1) AS INTEGER) * 
                        CAST(SUBSTR(Resolution, INSTR(Resolution, 'x') + 1) AS INTEGER)) AS pixel_area,
                       ROW_NUMBER() OVER (PARTITION BY Breed ORDER BY 
                           (CAST(SUBSTR(Resolution, 1, INSTR(Resolution, 'x') - 1) AS INTEGER) * 
                            CAST(SUBSTR(Resolution, INSTR(Resolution, 'x') + 1) AS INTEGER)) DESC) AS resolution_rank
                FROM DogImages
                WHERE Resolution IS NOT NULL
                AND Breed IN (
                    SELECT Breed 
                    FROM DogImages 
                    GROUP BY Breed 
                    HAVING COUNT(*) > 10
                )
            ) ranked
            WHERE resolution_rank <= 5
            ORDER BY Breed, pixel_area DESC;
        """
    }
]

# File to save results
output_file = 'query_results.txt'

# Run each query and save results
with open(output_file, 'w', encoding='utf-8') as f:
    for i, query in enumerate(queries):

        f.write(f"\n{query['name']}\n")
        f.write(f"SQL:\n{query['sql']}\n\nResults:\n")

        try:
            # Execute query and fetch results as a DataFrame
            df = pd.read_sql_query(query['sql'], conn)

            # Print results to console
            print(df)

            # Save query results to CSV
            csv_file = f"query_{i+1}_results.csv"
            df.to_csv(csv_file, index=False)

            # Write results to file
            f.write(df.to_string(index=False))
            f.write("\n" + "="*80 + "\n")

        except Exception as e:
            print(f"Error running {query['name']}: {e}")
            f.write(f"Error: {e}\n" + "="*80 + "\n")

# Close the database connection
conn.close()

print(f"\nAll queries executed. Results saved to {output_file} and CSV files.")