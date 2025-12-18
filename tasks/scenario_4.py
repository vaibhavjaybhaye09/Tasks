import pandas as pd
import re

# Sample DataFrame
df = pd.DataFrame({
    "text": [
        "Hello World!",
        "AI & ML are AMAZING!!!",
        "Text-Preprocessing @ Data Science"
    ]
})

# Step 1: Convert to lowercase
df["clean_text"] = df["text"].str.lower()

#Remove special characters
df["clean_text"] = df["clean_text"].str.replace(r"[^a-z0-9\s]", "", regex=True)

# Tokenize text
df["tokens"] = df["clean_text"].str.split()

print(df)
