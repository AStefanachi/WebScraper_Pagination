# Web Scraping a website with Pagination
# Library Used BeautifulSoup4, Requests, Styleframe, Pandas, OS
# Andrea Stefanachi, Developer

# General Import
import pandas as pd
from functions import *
from styleframe import StyleFrame
from tqdm import tqdm
from configurations import *

# Get maximum page range
pages = get_max_pagination()

result = []

# Looping through pages and extracting data
for i in tqdm(range(1, pages + 1), desc="Scraping..."):
    url = "https://scrapethissite.com/pages/forms/?page_num=" + str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    t_rows = soup.find_all("tr", class_="team")
    for element in t_rows:
        team_name = element.find("td", class_="name")
        team_name = team_name.text
        team_name = team_name.strip()
        year = element.find("td", class_="year")
        year = year.text
        year = year.strip()
        wins = element.find("td", class_="wins")
        wins = wins.text
        wins = wins.strip()
        losses = element.find("td", class_="losses")
        losses = losses.text
        losses = losses.strip()
        ot_losses = element.find("td", class_="ot-losses")
        ot_losses = ot_losses.text
        ot_losses = ot_losses.strip()
        if len(ot_losses) == 0:
            ot_losses = str(np.NaN)
        try:
            win_pct = element.find("td", class_="pct text-success")
            win_pct = win_pct.text
            win_pct = win_pct.strip()
        except AttributeError as e:
            win_pct = element.find("td", class_="pct text-danger")
            win_pct = win_pct.text
            win_pct = win_pct.strip()
        goals_for = element.find("td", class_="gf")
        goals_for = goals_for.text
        goals_for = goals_for.strip()
        goals_against = element.find("td", class_="ga")
        goals_against = goals_against.text
        goals_against = goals_against.strip()
        try:
            diff_success = element.find("td", class_="diff text-success")
            diff_success = diff_success.text
            diff_success = diff_success.strip()
        except AttributeError as e:
            diff_success = element.find("td", class_="diff text-danger")
            diff_success = diff_success.text
            diff_success = diff_success.strip()

        result.append((team_name, year, wins, losses, ot_losses, win_pct, goals_for, goals_against, diff_success))

columns = get_columns_name()

df = pd.DataFrame(result, columns=columns)

entries = len(df.index)

print("[+] Scraping completed: " + str(entries) + " entries found")

# building styled Excel file

print("[+] Building .xlsx output")

sf = StyleFrame(df)

file = os.path.join(default_path, "output.xlsx")

writer = sf.ExcelWriter(file)

sf.to_excel(excel_writer=writer, na_rep=np.NaN, sheet_name="teams", index=False, row_to_add_filters=0, best_fit=columns)

writer.save()

# csv output

print("[+] Building .csv output")

df.to_csv("output.csv", na_rep=np.NaN, index=False)
