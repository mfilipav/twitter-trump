
import json

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor

import folium

fname = 'usr_timeline_realDonaldTrump.jsonl'
fname = 'home_timeline.jsonl'
geo_tweets = 'realDonaldTrump.geo.json'      # Output file

with open(fname, 'r') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": [],
    }
    for line in f:
        tweet = json.loads(line)
        #print(tweet)
        try:
            if tweet['coordinates']:
                geo_json_feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": tweet['coordinates']['coordinates'],
                    },
                    "properties": {
                        "text": tweet['text'],
                        "created_at": tweet['created_at']
                    },
                }
                geo_data['features'].append(geo_json_feature)
                print(geo_json_feature)
        except KeyError:
            # json doc is not a tweet
            continue

with open(geo_tweets, 'w') as f:
    f.write(json.dumps(geo_data, indent=4))



def make_map(geojson_file, map_file):
    # Create folium map centered at (latitude, longitude)
    tweet_map = folium.Map(location=[50, -50], zoom_start=2)
    # In case Tweets get too clustered
    marker_cluster = folium.MarkerCluster().add_to(tweet_map)

    geodata = json.load(open(geojson_file))
    for tweet in geodata['features']:
        tweet['geometry']['coordinates'].reverse()
        marker = folium.Marker(tweet['geometry']['coordinates'], popup=tweet['properties']['text'])
        marker.add_to(marker_cluster)

    tweet_map.save(map_file)


make_map(geo_tweets, 'example.html')

from IPython.display import IFrame
IFrame('example.html', width=700, height=350)
