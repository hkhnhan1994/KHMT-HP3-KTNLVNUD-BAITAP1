from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Read the contents of the text file
file_path = Path('dataset.txt')  # Replace with the actual file path
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content into a list of paragraphs using one or more occurrences of double newline as a delimiter
paragraphs = re.split("\n\n+", content)

def get_github_link(query):
    url = f"https://www.google.com/search?q={query}&num=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all("a")
        for link in results:
            url = link.get("href")
            print(url)
            if 'github.com' in url:
                return url.split("/url?q=")[1].split("&sa=U&")[0]
    else: print(f"{response.status_code} too many requests please wait")
    return "not found"
# Search for GitHub links for each paragraph
github_links = []
for p in paragraphs:
    result=get_github_link("git hub " +p)
    # print(result)
    github_links.append(p)
data = {"Content": paragraphs, "Result": github_links}
df = pd.DataFrame(data)
# Save the DataFrame to a CSV file
csv_file_path =  Path('result.csv')  # Replace with the desired CSV file path
df.to_csv(csv_file_path, index=False)

print("Data saved to CSV successfully.")