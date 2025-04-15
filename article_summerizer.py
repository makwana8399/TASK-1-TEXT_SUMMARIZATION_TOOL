from transformers import pipeline
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
import subprocess
import sys

# Install required libraries (only installs if not present)
def install_packages():
    packages = ["transformers", "torch", "nltk"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages()

# Import after installation
from transformers import pipeline
import nltk
nltk.download('punkt')

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Sample article input (you can replace this or use file input)
article = """
Harshad Mehta was a prominent stockbroker who became a household name in India during the early 1990s. 
Often referred to as the “Big Bull” of Dalal Street, he played a central role in one of the biggest financial scandals in Indian history. 
His story is one of ambition, innovation, and ultimately, controversy.
Mehta started his career in humble surroundings, working various odd jobs before entering the stock market. 
His deep understanding of the market and his confident demeanor helped him gain trust and build a large network of clients.
"""
# Optional: load article from a text file
# with open("your_article.txt", "r", encoding="utf-8") as file:
#     article = file.read()

# Summarize
print("\n🔍 Summarizing article...\n")
summary = summarizer(article, max_length=97, min_length=50, do_sample=False)

# Output summary
print("📝 Summary:\n")
print(summary[0]['summary_text'])
