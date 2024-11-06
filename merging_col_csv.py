import pandas as pd

# Load the CSV file without headers, reading only the columns we need
df = pd.read_csv("HSK4.csv", encoding="utf-8", header=None, usecols=[0, 1, 2])

# Merge the first two columns (0 and 1) into a single 'Question' column
df["Question"] = df[1] + " - " + df[2]  # Change " - " to any separator you prefer

# Rename column 2 to "Answer" for clarity
df = df.rename(columns={0: "Answer"})

# Select only the merged 'Question' column and 'Answer' column for the final output
final_df = df[["Answer","Question"]]

# Save the result to a new CSV file
final_df.to_csv("cleaned_flashcards.csv", index=False, encoding="utf-8")
