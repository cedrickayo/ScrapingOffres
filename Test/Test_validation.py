
import pandas as pd
from bs4 import BeautifulSoup

file_path="Data/jobs.csv"
file="public/index.html"

def test_count_line():
    data = pd.read_csv(file_path)
    print(data)
    assert len(data) > 2


def test_verif_table_in_html():

    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")

    tables = soup.find_all('table')

    assert  len(tables) > 0


