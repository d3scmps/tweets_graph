import csv
import networkx as nx 
import datetime
from tqdm import tqdm
from math import sqrt, log
from collections import Counter

import csv
import networkx as nx 
import datetime
from tqdm import tqdm
from math import sqrt, log
from collections import Counter, OrderedDict

def processing_file(file):
    with open(file) as f, open("fichier_filtrepetit.csv","w") as f2:
        file_content = csv.DictReader(f)
        headers = file_content.fieldnames
        headers.append("sum_Rtfollowers")
        writer = csv.DictWriter(f2, fieldnames = headers)
        writer.writeheader()
        tweets_o =  []
        rt_o = []
        c = 0
        # Here we split tweets between "primar" tweets and retweets
        for row in file_content:
            if row["retweeted_id"]:
                rt_o.append(row)
            else:
                tweets_o.append(row)
        # Here we check whether  
        # Complexity is quite bad ( The use of a Counter dict-container might me more effective)
        for tweet in tweets_o:
            S = 1
            for rt in rt_o:
                if rt["retweeted_id"] == tweet["links"]:
                    print("ok")
                    S += int(rt["hashtags"])
            tweet.update({"sum_Rtfollowers":S})
            writer.writerow(tweet)

a = processing_file("/home/ptl7123/Bureau/lancet_smallfile2.csv")


