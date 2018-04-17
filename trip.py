import requests
from bs4 import BeautifulSoup
import sys
import sqlite3
import json
import plotly.plotly as py
import plotly.graph_objs as go

# create trip.db database
# contains 2 tables: Activities and ActivityInfo
DBNAME = 'trip.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# init db
def drop_db():

    # Drop tables
    statement1 = '''
        DROP TABLE IF EXISTS 'Activities';
    '''

    statement2 = '''
        DROP TABLE IF EXISTS 'ActivityInfo';
    '''

    statement3 = '''
        DROP TABLE IF EXISTS 'States'
    '''

    cur.execute(statement1)
    cur.execute(statement2)
    cur.execute(statement3)

    conn.commit()

def create_tables():
    query1 = '''
        CREATE TABLE 'Activities' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'State' INTEGER,
            'Attraction' TEXT,
            'Location' TEXT,
            'URL' TEXT
        );
    '''

    query2 = '''
        CREATE TABLE 'ActivityInfo' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Title' TEXT,
        'Type' TEXT,
        'Rating' INTEGER,
        'NumReviews' INTEGER
        );
    '''

    query3 = '''
        CREATE TABLE 'States' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'StateName' TEXT
        );
    '''


    cur.execute(query1)
    cur.execute(query2)
    cur.execute(query3)

    conn.commit()
    conn.close()

# Cache STATE ACTIVITIES
# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
CACHE_FNAME2 = 'cache2.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

try:
    cache_file = open(CACHE_FNAME2, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION2 = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION2 = {}

def get_unique_key(url, code):
    full_url = url + code
    return full_url

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)

def make_request_using_cache(url, code):
    unique_ident = get_unique_key(url, code)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data

        full_url = url + code
        resp = requests.get(full_url)

        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]




# Cache 2
def make_request_using_cache2(url):
    unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION2:
        # print("Getting cached data...")
        return CACHE_DICTION2[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data

        resp = requests.get(url)

        CACHE_DICTION2[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION2)
        fw = open(CACHE_FNAME2,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION2[unique_ident]


# need state code in link to scrape page
state_code_dict = {
    'Alabama': 'g28922',
    'Alaska' : 'g28923',
    'Arizona' : 'g28924',
    'Arkansas' : 'g28925',
    'California' : 'g28926',
    'Colorado' : 'g28927',
    'Connecticut' : 'g28928',
    'Delaware' : 'g28929',
    'Florida' : 'g28930',
    'Georgia' : 'g28931',
    'Hawaii' : 'g28932',
    'Idaho' : 'g28933',
    'Illinois' : 'g28934',
    'Indiana' : 'g28935',
    'Iowa' : 'g28936',
    'Kansas' : 'g28937',
    'Kentucky' : 'g28938',
    'Louisiana' : 'g28939',
    'Maine' : 'g28940',
    'Maryland' : 'g28941',
    'Massachusetts' : 'g28942',
    'Michigan' : 'g28943',
    'Minnesota' : 'g28944',
    'Mississippi' : 'g28945',
    'Missouri' : 'g28946',
    'Montana' : 'g28947',
    'Nebraska' : 'g28948',
    'Nevada' : 'g28949',
    'New_Hampshire' : 'g28950',
    'New_Jersey' : 'g28951',
    'New_Mexico' : 'g28952',
    'New_York' : 'g28953',
    'North_Carolina' : 'g28954',
    'North_Dakota' : 'g28955',
    'Ohio' : 'g28956',
    'Oklahoma' : 'g28957',
    'Oregon' : 'g28958',
    'Pennsylvania' : 'g28959',
    'Rhode_Island' : 'g28960',
    'South_Carolina' : 'g28961',
    'South_Dakota' : 'g28962',
    'Tennessee' : 'g28963',
    'Texas' : 'g28964',
    'Utah' : 'g28965',
    'Vermont' : 'g28966',
    'Virginia' : 'g28967',
    'Washington' : 'g28968',
    'West_Virginia' : 'g28971',
    'Wisconsin' : 'g28972',
    'Wyoming' : 'g28973'
}

state_to_num = {
    'Alabama': 1,
    'Alaska' : 2,
    'Arizona' : 3,
    'Arkansas' : 4,
    'California' : 5,
    'Colorado' : 6,
    'Connecticut' : 7,
    'Delaware' : 8,
    'Florida' : 9,
    'Georgia' : 10,
    'Hawaii' : 11,
    'Idaho' : 12,
    'Illinois' : 13,
    'Indiana' : 14,
    'Iowa' : 15,
    'Kansas' : 16,
    'Kentucky' : 17,
    'Louisiana' : 18,
    'Maine' : 19,
    'Maryland' : 20,
    'Massachusetts' : 21,
    'Michigan' : 22,
    'Minnesota' : 23,
    'Mississippi' : 24,
    'Missouri' : 25,
    'Montana' : 26,
    'Nebraska' : 27,
    'Nevada' : 28,
    'New Hampshire' : 29,
    'New Jersey' : 30,
    'New Mexico' : 31,
    'New York' : 32,
    'North Carolina' : 33,
    'North Dakota' : 34,
    'Ohio' : 35,
    'Oklahoma' : 36,
    'Oregon' : 37,
    'Pennsylvania' : 38,
    'Rhode Island' : 39,
    'South Carolina' : 40,
    'South Dakota' : 41,
    'Tennessee' : 42,
    'Texas' : 43,
    'Utah' : 44,
    'Vermont' : 45,
    'Virginia' : 46,
    'Washington' : 47,
    'West Virginia' : 48,
    'Wisconsin' : 49,
    'Wyoming' : 50
}



def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for state in state_code_dict:
        baseurl = 'https://www.tripadvisor.com/Attractions-'
        state_code = state_code_dict[state]
        full_url = baseurl + state_code
        page_text = make_request_using_cache(baseurl, state_code)
        soup = BeautifulSoup(page_text, 'html.parser')
        todo = soup.find_all(class_='listing_title')
        count = 0
        for t in todo:
            if count < 3:
                if t.find('a') is not None:
                    a = t.find('a').text
                else:
                    a = "None"
                url = "https://www.tripadvisor.com" + t.find('a')['href']
                if t.find('span') is not None :
                    l = t.find('span').text
                else:
                    l = "None"
                loc = state.replace("_", " ")
                insertion = (None, state_to_num[loc], a, l, url)
                statement = 'INSERT INTO "Activities" '
                statement += 'VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                count = count + 1
                text = make_request_using_cache2(url)
                ramen = BeautifulSoup(text, 'html.parser')
                detail = ramen.find_all(class_='detail')
                popularity = ramen.find_all(class_='header_popularity')
                reviews = ramen.find_all(class_='header_rating')
                for d,p,r in zip(detail,popularity,reviews):
                    if d.find('a') is not None:
                        type = d.find('a').text
                    else:
                        type = "None"
                    if p.find('span') is not None:
                        rating = p.find('span').text[1:]
                    else:
                        rating = 0
                    rev = r.find('a')
                    if rev.find('span') is not None:
                        num_reviews = rev.find('span').text
                    else:
                        num_reviews = 0
                insert = (None, a, type, rating, num_reviews)
                statement = 'INSERT INTO "ActivityInfo" '
                statement += 'VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement, insert)
            else:
                break

    for s in state_to_num:
        statement = 'INSERT INTO "States" '
        statement += 'VALUES (?, ?)'
        insert = (None, s)
        cur.execute(statement, insert)

    conn.commit()

class State:
    def __init__(self, name, attraction, location, url=None):
        self.name = name
        self.attraction = attraction
        self.location = location
        self.url = url

    def __str__(self):
        str_ = self.attraction + " in " + self.location
        return str_

def get_activities(state) :
    activities = []
    query = '''
    SELECT StateName, Attraction, Location, URL
    FROM Activities
    JOIN ActivityInfo
    ON Title = Attraction
    JOIN States
    ON State = States.Id
    WHERE StateName = '''
    query += "'" + state + "'"
    cur.execute(query)
    for row in cur:
        place = State(row[0], row[1], row[2], row[3])
        activities.append(place)

    return activities



if __name__ == "__main__":
    # drop_db()
    # create_tables()
    # init_db()

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    entered = input('Enter command (or "help" for options): ')
    entered = entered.split()
    command = entered[0]

    while (command != "exit"):
        if command == "exit" :
            print("Bye!")

        # GRAPH 1
        # Creates chart showing how many activities rank #1, #2, and #3
        elif command == "rankings":
            nums = []
            for x in range(1,4):
                statement = '''
                SELECT Count(*)
                FROM ActivityInfo
                WHERE Rating ='''
                statement += str(x)
                cur.execute(statement)
                for row in cur:
                    nums.append(row[0])

            data = [go.Bar(
                x=['1', '2', '3'],
                y= nums,
            )]

            layout = go.Layout(
                title='Activities Sorted By Ranking',
            )

            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='basic-bar')

        # GRAPH 2
        # Number of Activity Reviews on Trip Advisor for the Top Three Activities per State
        elif command == "reviews":
            x = []
            y = []
            statement = '''
            SELECT StateName, NumReviews
            FROM ActivityInfo
            JOIN Activities
            ON Title = Attraction
            JOIN States
            ON State = States.Id
            GROUP BY StateName
            '''
            cur.execute(statement)
            for row in cur:
                x.append(row[0])
                y.append(row[1])

            data = [go.Scatter(
                x=x,
                y=y
            )]

            layout = go.Layout(
                title='Sum of Trip Advisor Reviews for the Top Three Activities per State',
            )

            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='basic-scatter')

        # GRAPH 3
        # pie chart that sorts all activities by type
        elif command == "type":
            x= []
            y= []
            statement = '''
            SELECT Type, COUNT(*)
            FROM ActivityInfo
            GROUP BY Type
            ORDER BY COUNT(*) DESC
            '''
            cur.execute(statement)
            for row in cur:
                x.append(row[0])
                y.append(row[1])

            labels = x
            values = y

            trace = go.Pie(labels=labels, values=values)

            py.plot([trace], filename='basic_pie_chart')

        # GRAPH 4
        # provides a table of the top 3 activities to do in the state
        # user inputs "activities" followed by a state capitalized
        # ex: activities Michigan
        # ex: activities New York
        elif command == "activities":
            states = []
            todo = []
            if len(entered) < 3:
                states.append(entered[1])
                all_activities = get_activities(entered[1])
                for a in all_activities:
                    todo.append(str(a))
            else:
                state = entered[1] + " " + entered[2]
                all_activities = get_activities(state)
                states.append(state)
                for a in all_activities:
                    todo.append(str(a))

            trace = go.Table(
            type = 'table',
            header=dict(values=states),
            cells=dict(values=[todo]))

            data = [trace]
            py.plot(data, filename = 'styled_table')

        elif command == "help":
            help = '''1) "rankings" - generates bar chart showing how many activities rank #1, #2, and #3\n'''
            help += '''2) "reviews" - creates scatter plot depicting the sum of every states top three activity reviews\n'''
            help+= '''3) "type" - makes a pie chart sorting all activities by type\n'''
            help+= '''4) "activities [State]" - a user inputs "activities" followed by a state capitalized (i.e. "activities Michigan" or "activities New York") and the program produces a table of the top three activities to do in the state specified'''
            print(help)

        else:
            print("Bad input :( try again!")

        entered = input('Enter command (or "help" for options): ')
        entered = entered.split()
        command = entered[0]


    if command == "exit" :
        print("Bye!")
