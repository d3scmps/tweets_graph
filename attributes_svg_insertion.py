import csv
from bs4 import BeautifulSoup

from lxml import etree


def attribut(fichiercsv, graphe1, graphe2):
    with open(fichiercsv) as f1, open(graphe1, "r+") as f2, open(graphe2, "w") as f3:
        file_content = csv.DictReader(f1)
        soup = BeautifulSoup(f2,'xml')
        articles = soup.g
        l = []
        #articles.find('circle')['author'] = "test"
        for x in articles:
            if type(x)==type(articles):
                l.append(x)
        #### l contains 
        for row in file_content:
            for x in l:
                if row["id"] == x["class"][3:]:
                    x["author"] = row["from__user_name"]
                    x["text"] = row["text"]
                    x["sum_Rtfollowers"] = row["sum_Rtfollowers"]
        print(soup)
        f3.write(str(soup))

attribut("fichier_filtre5.csv", "grand_graphe.svg", "grand_graphe2.svg")
attribut("fichier_filtrepetit.csv", "petit_graphe.svg", "petit_graphe2.svg")