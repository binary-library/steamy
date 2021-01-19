from flask import Flask, render_template, request
app = Flask(__name__)
import steamy_req as sr
import functools
from gpiozero import Servo
from time import sleep

#parse top100 steam games
def parse_100(x):
    games = sr.return_gamedata()
    new_dict = {}
    i = 0
    for k, v in games.items():
        if i == x:
            return new_dict
        else:
            new_dict[k] = v
            i = i+1
    return new_dict
#return amount of people who have installed games from l
def get_owners(l):
    dictos = {}
    for k, v in l.items():
        dictos[v["name"]] = v["owners"].split("..")[0].replace(",", "")
    return dictos
#return positive and negative reviews of list of games
def get_posneg_reviews(l):
    dictos = {}
    for k, v in l.items():
        dictos[v["name"]] = [v["positive"] ,v["negative"]]
    return dictos
#return a dict with total hours, days, years of gametime
def get_games_sums(data):
    sum_hours = 0
    for i in data:
        sum_hours = sum_hours + i.get("playtime_forever")
    hours = round(sum_hours / 60, 1)
    days = round(hours / 24, 1)
    years = round(days / 356,1)
    return {"hours": hours, "days": days, "years": years}
#tries to parse private data that might not be availible
def parse_private_profile(data):
    dictos = {}
    possible_fields = ["personaname", "avatarfull", "realname", "loccountrycode", "personastate"]
    for i in possible_fields:
        try:
            dictos[i] = data[i]
        except:
            dictos[i] = None 
    return dictos
#feed it players data will return a sorted version of nth long
def get_most_played_from_player(data, nth):
    data = list(map(lambda x: [x["name"], x["playtime_forever"] ], data))
    #sorted on hours played
    sorted_quantitative = dirty_reverse(selection_sort(dirty_reverse(data)))
    #sorted on alphabetical val
    sorted_qualitative = selection_sort(data)
    # print(sr.the_first(10, sorted_qualitative))
    return( sr.the_first(nth ,sorted_qualitative), sr.the_last(nth, sorted_quantitative) )

#reverses [two items] in a big array
def dirty_reverse(data):
    # print(data)
    return list(map(lambda x: [x[1], x[0]], data ))

#the sorting algoritm required for this assignment
def selection_sort(l):
    sorted_l = []
    for i in range(0, len(l)):
        smallest_index = l.index(min(l))
        sorted_l.append(l[smallest_index])
        del l[smallest_index]
    return sorted_l

def s_servo(x):
    if x == 0:
        servo.max()
    elif x == 1:
        servo.mid()
    else:
        servo.mid()

#populate a huge dict with data
def parse_player(data):
    dictionare = {}
    try: #first qry might fail cause of invalid id or api is down for maintenance
        dictionare["steam_id"] = sr.resolve_vanity_url(data)
        temp_id = dictionare["steam_id"]
    except:
        pass
    player_data = sr.profile_information(temp_id)["response"]["players"][0]
    try: #if user has profile set to private we cant see this
        dictionare["private_data"] = parse_private_profile(player_data)
        dictionare["player_games"] = sr.players_game_list(temp_id)["response"]
        dictionare["game_count"] = dictionare["player_games"]["game_count"]
        print(dictionare["game_count"])
    except:
        pass    
    dictionare["total_time"] = get_games_sums(dictionare["player_games"]["games"])
    dictionare["total_friends"] = len(sr.players_friend_list(temp_id)["friendslist"]["friends"])
    qaul, qaun = get_most_played_from_player(dictionare["player_games"]["games"], 15)
    dictionare["qtity"] = list(map(lambda x: [x[0].replace('"', "'"), (x[1]//60)], qaun))
    dictionare["qlity"] = list(map(lambda x: [x[0].replace('"', "'"), (x[1]//60)], qaul))
    return dictionare

#query list if not downloaded, else open list
list_g = parse_100(15)
owners_count = get_owners(list_g)
game_reviews = get_posneg_reviews(list_g)
myGPIO = 4
servo = Servo(myGPIO)

#routing
@app.route('/search/<sort_type>', methods=['POST', 'GET'])
#search page
def search(sort_type):
    data = request.form.get('search')
    #parse player data
    data_parsed = parse_player(data)
    if data_parsed["private_data"]["personastate"] == 1:
        s_servo(0)
    else:
        s_servo(2)
    games_t = data_parsed["qtity"] if sort_type == "qan" else data_parsed["qlity"] 
    return render_template("search.j2",d_=data_parsed, top_games=games_t)
#homepage
@app.route('/')
def main():
    s_servo(1)
    return render_template('main.j2')
#charts seperatly being rendered in an Iframe
@app.route('/first_chart')
def top_chart():
    return render_template('first_chart.j2', games=owners_count)
@app.route('/second_chart')
def review_chart():
    return render_template('second_chart.j2', reviews=game_reviews)
@app.route('/third_chart')
def player_chart():
    return render_template('third_chart.j2', top_games=games_t)
