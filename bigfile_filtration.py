import csv


def processing_file(file):
    with open(file) as f, open("fichier_filtre5.csv","w") as f2:
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
                if rt["retweeted_id"] == tweet["id"]:
                    print("ok")
                    S += int(rt["from__user_followercount"])
            tweet.update({"sum_Rtfollowers":S})
            writer.writerow(tweet)

a = processing_file("/home/ptl7123/Bureau/Mention_Tweets_5.csv")

        
