import csv
import networkx as nx 
import datetime
from tqdm import tqdm
from math import sqrt, log
from collections import Counter

def get_bin_time(fichier):
    """ This function allows us to get a suitable time pace which will be used later on when 
    drawing the graph"""
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



"""Creating a first dictionnary which keys are the time distribution previously defined. The values are 
coordinates"""
time_partitions = dict() 
Y = 4000
while t < Total_time:
    time_partitions.update({t : [Y,0]})
    Y -= 100
    t += pace

G = nx.DiGraph()
time_part = dict()
Z = 4000

### Filtrating no point land  
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
    # This c variable will be used to make a color gradient in order to see if the noverlap algo works fine
    c = 0
    for x in time_partitions.keys():
        #We only keep intervals that actually contains tweets
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
            ##### -------------------------------------- ######

            # For usual cases, we check whether the time of the tweet is in the current time interval
            if not (tem > x and tem < x + pace):
                continue
            G.nodes[tweet_id]["viz"]["color"] = {"r": int(time_part[x][2]) , "g": 0 ,"b" : 0, "a" : 1.0}
            position = time_part[x][1]
            hauteur = time_part[x][0]
            pas = 20
            # Here we distribute tweets that are in the same time bin on the x axis 
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
