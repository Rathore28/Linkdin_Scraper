import matplotlib.pyplot as plt

def visualize_jobs(df, output="company_frequency.png"):
    counts = df["company"].value_counts().head(10)
    counts.plot(kind="bar", figsize=(10, 6))
    plt.title("Top Hiring Companies")
    plt.xlabel("Company")
    plt.ylabel("Number of Jobs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output)
    return output
