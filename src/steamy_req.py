import json
import distance_sensor as ds
from threading import Thread
import os.path
import random
import requests 
from dotenv import load_dotenv
import os

#const api-key%datapath
load_dotenv()
api_key = os.getenv("API")
data_path = os.getenv("DATA_PATH")

#requests game information
def game_info(appid): #get game information
    url = "https://store.steampowered.com/api/appdetails?appids={a}".format(a=api_key)
    res = standard_req(url)
    return json.loads(res)

#get 100top games
def top_100_games():
    url = "https://steamspy.com/api.php?request=top100in2weeks"
    res = standard_req(url)
    return json.loads(res)

def profile_information(p_id):
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={a}&steamids={p}".format(a=api_key,p=p_id)
    # print(url)
    res = standard_req(url)
    return json.loads(res)

#get players friends
def players_game_list(p_id):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={a}&steamid={p}&format=json&include_played_free_games=1&include_appinfo=1".format(a=api_key,p=p_id)
    res = standard_req(url)
    return json.loads(res)

def players_friend_list(p_id):
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={a}&steamid={p}&relationship=friend".format(a=api_key,p=p_id)
    res = standard_req(url)
    return json.loads(res)

#basic func_req
def standard_req(url): #basic api req
    res = requests.get(url) 
    return res.text

#returns logo url if given appid&hash
def game_logo(appid, img_hash): #return logo-url
    url = "http://media.steampowered.com/steamcommunity/public/images/apps/{a}/{h}.jpg".format(a=appid,h=img_hash)
    return url

#returns steamID if given steamurl
def resolve_vanity_url(name): #change url to steamid|64bit
    name = parse_url(name).strip()
    if name.isdigit():
        return name
    else:
        url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={a}&vanityurl={n}".format(a=api_key,n=name) 
        res = standard_req(url)
        return(json.loads(res)["response"]["steamid"])

def read_gamedata(data_path):
    if os.path.exists(data_path):
        with open( data_path) as f:
            data = f.read()
            return json.loads(data)
    else:
        data = top_100_games()
        print(data)
        print(type(data))
        save("./data/games.data", data, False, jsn=True)

#helper funcs
def save(file_path,data,log=True,jsn=False): #quick&dirty save
    if log:
        name_rand = file_path + str(random.randint(0, 100))
        with open( str("./../logs/"+name_rand) , "w") as f:
            if jsn:
                json.dump(data, f)
            else:
                f.write(str(data))
    else:
        with open(file_path , "w") as f:
            if jsn:
                json.dump(data, f)
            else:
                f.write(str(data))
def first(x):
    return x[0]
def last(x):
    return x[-1]
def the_first(a, x):
    return x[:a]
def the_last(a, x):
    return x[-1-a:]
def parse_url(u): 
    id = last(u.split("/"))
    # print(id)
    return id

def busy_bee(x):


def return_gamedata():
    data_json = read_gamedata(data_path)
    return data_json

return_gamedata()

Thread(target=ds.mainloop, args=(20)).start()