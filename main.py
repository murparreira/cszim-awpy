from awpy import DemoParser
from awpy.analytics.stats import player_stats
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
  print(request.method)
  if request.method == 'POST':
    demo_file = request.form['demo_file']
    demo_file_path = "/code/demos/{demo_file}".format(demo_file=demo_file)
    demo_parser = DemoParser(
      demofile=demo_file_path, 
      demo_id=demo_file, 
      parse_rate=128)

    data = demo_parser.parse()

    player_stats_json = {}
    player_stats_json['players'] = player_stats(data["gameRounds"], return_type="json")
    player_stats_json['rounds'] = data["gameRounds"]

    i = 0
    while i < len(data["gameRounds"]):
      for kill in data["gameRounds"][i]["kills"]:
        steam_id = str(kill["attackerSteamID"])
        if steam_id in player_stats_json['players']:
          if "player_kills" in player_stats_json['players'][steam_id]:
            player_stats_json['players'][steam_id]["player_kills"].append(kill)
          else:
            player_stats_json['players'][steam_id].update({"player_kills": [kill]})
      i += 1
    

    return player_stats_json

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
