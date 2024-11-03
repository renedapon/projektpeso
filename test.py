import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the webpage
url = 'https://www.tarturehv.ee/hinnakiri/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 2: Find the table in the HTML
table = soup.find('table')  # Locate the table; add specificity if necessary

# Step 3: Parse the table's rows and columns
data = []
for row in table.find_all('tr'):
    columns = row.find_all(['td', 'th'])
    data.append([col.get_text(strip=True) for col in columns])

# Step 4: Convert to DataFrame and select the first 3 rows
df = pd.DataFrame(data[1:], columns=data[0])  # First row as header
df_first_two_rows = df.head(2)  # Only first 3 rows


# Convert the DataFrame of the first 3 rows to a matrix (NumPy array)
matrix = df_first_two_rows.to_numpy()
#hinnad_plekkvelg = list(map(int, matrix[0][1:].strip(),split().replace('€', '')))
#hinnad_valuvelg = list(map(int, matrix[1][1:].strip().split().replace('€', '')))

# Display the matrix
print(matrix)
#print(hinnad_plekkvelg)
#print(hinnad_valuvelg)

[['Rehvivahetus plekkvelg 4tk(linnamaastur/maastur +5€)' '45€' '45€' ''
  '' '' '']
 ['Rehvivahetus valuvelg 4tk(linnamaastur/maastur +5€)' '48€' '53€' '58€'
  '63€' '68€' '73€']]