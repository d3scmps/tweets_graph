import csv
import networkx as nx 
import datetime
from tqdm import tqdm
from math import sqrt, log
from collections import Counter


def filtrage_text(tweet):
    c=0
    for x in tweet:
        if x != "#":
            c +=1
        else:
            return tweet[c:]
            break

def processing_file(file):
    with open(file) as f, open("fichier_filtrepetit.csv","w") as f2:
        file_content = csv.DictReader(f)
        #îd, retweeted_id, from__user_followercount
        headers = file_content.fieldnames
        print(type(headers))
        headers.append("sum_Rtfollowers")
        writer = csv.DictWriter(f2, fieldnames = headers)
        writer.writeheader()
        tweets_o = []
        rt_o = []
        for row in file_content:
            if row["retweeted_id"]:
                rt_o.append(row)
            else:
                tweets_o.append(row)
        for tweet in tweets_o:
            S = 1
            for rt in rt_o:
                if rt["retweeted_id"] == tweet["links"]:
                    print("ok")
                    S += int(rt["from__user_followercount"])
            tweet.update({"sum_Rtfollowers":S})
            writer.writerow(tweet)

a = processing_file("/home/ptl7123/Bureau/lancet_smallfile2.csv")



def get_bin_time(fichier):
    n = 0 
    maxi = 0.0
    mini = 90000000000000
    with open(fichier, "r+") as f1:
        file_content = csv.DictReader(f1)
        for row in file_content:
            n +=1
            if float(row["lang"])> maxi:
                maxi = float(row["lang"])
            if float(row["lang"])< mini:
                mini = float(row["lang"])
        return ((maxi - mini)/n, mini, maxi, n)  

tempo = get_bin_time("fichier_filtrepetit.csv")
Total_time = tempo[2]
pace = tempo[0]*0.9
t = tempo[1]

def get_stats(fichier):
    mini = 99
    maxi = 0
    with open(fichier, "r+") as f1:
        file_content = csv.DictReader(f1)
        for row in file_content:
            if float(row["sum_Rtfollowers"])> maxi:
                maxi = float(row["sum_Rtfollowers"])
            if float(row["sum_Rtfollowers"])< mini:
                mini = float(row["sum_Rtfollowers"])
    return (mini, maxi)  

arg = get_stats("fichier_filtrepetit.csv")
minc = arg[0]
maxc = arg[1]


time_partitions = dict() 
Y = 4000
while t < Total_time:
    time_partitions.update({t : [Y,0]})
    Y -= 100
    t += pace

G = nx.DiGraph()
time_part = dict()
Z = 4000
with open("fichier_filtrepetit.csv") as f:
    file_content = csv.DictReader(f)
    a = 0
    d = Counter()
    for row in file_content:
        tem = float(row["lang"])
        for x in time_partitions.keys():
            if not (tem > x and tem < x + pace):
                continue
            d[x] += 1
    c = 0
    for x in time_partitions.keys():
        if x in d:
            if c < 200:
                c = c + 5
            time_part.update({x :[Z,0,c]})
            Z -= 10

with open("fichier_filtrepetit.csv") as f:
    file_content = csv.DictReader(f)
    for row in file_content:
        tweet_id = row["links"]
        author = row["from__user_name"]
        text_tweet = row["lang"]
        total_followers = row["sum_Rtfollowers"]
        G.add_node(tweet_id, author = author, text_tweet = text_tweet) #, author = author, text = text_tweet, nb_of_followers = total_followers)
        G.nodes[tweet_id]["viz"] = {"size" : log((float(total_followers)**(1/2)))} 
        tem = float(row["lang"])
        for x in time_part.keys():
            ############## HANDLING THE ONLY EXCEPTION FOR TwEET_ID = 1262750127770333188)
            if tweet_id == str(1262750127770333188):
                id1 = 1593540750.8541856
                position = time_part[id1][1]
                hauteur = time_part[id1][0]
                G.nodes[tweet_id]["viz"]["color"] = {"r": int(time_part[id1][2]) , "g": 0 ,"b" : 0, "a" : 1.0}
                pas = 20
                if position == 0:
                    G.nodes[tweet_id]["viz"]["position"] = {"x": 0, "y": float(hauteur), "z" : 0.0} 
                elif position == 1:
                    G.nodes[tweet_id]["viz"]["position"] = {"x": pas, "y": float(hauteur), "z" : 0.0} 
                elif position % 2 == 0:
                    G.nodes[tweet_id]["viz"]["position"] = {"x": -float((position//2)*pas), "y": float(hauteur), "z" : 0.0} 
                else: 
                    G.nodes[tweet_id]["viz"]["position"] = {"x": float((position//2)*pas) + pas, "y": float(hauteur), "z" : 0.0}
                time_part[x][1] += 1
            if not (tem > x and tem < x + pace):
                continue
            G.nodes[tweet_id]["viz"]["color"] = {"r": int(time_part[x][2]) , "g": 0 ,"b" : 0, "a" : 1.0}
            position = time_part[x][1]
            hauteur = time_part[x][0]
            pas = 20
            #G.nodes[tweet_id]["viz"]["color"] = {"r": time_part[x][2], "g": 0 ,"b" : 0, "a" : 1.0}
            if position == 0:
                G.nodes[tweet_id]["viz"]["position"] = {"x": 0, "y": float(hauteur), "z" : 0.0} 
            elif position == 1:
                G.nodes[tweet_id]["viz"]["position"] = {"x": pas, "y": float(hauteur), "z" : 0.0} 
            elif position % 2 == 0:
                G.nodes[tweet_id]["viz"]["position"] = {"x": -float((position//2)*pas), "y": float(hauteur), "z" : 0.0} 
            else: 
                G.nodes[tweet_id]["viz"]["position"] = {"x": float((position//2)*pas) + pas, "y": float(hauteur), "z" : 0.0}
            time_part[x][1] += 1

nx.write_gexf(G, "graphe_petit.gexf")
