import json
from together import Together
import pandas as pd

client = Together()

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
    

data = load_jsonl("../data/pokemon_data.jsonl")

def write_jsonl(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item)
            f.write(json_line + '\n')

## Used to general pokemon data with better keys. 
for i in range(len(data)):
    d = data[i]
    new_dict = dict()
    poke_name = d['name']
    for key, val in d.items():
        if key=="name":
            new_dict[key] = val
            continue
        elif key=="Naturally learned moves":
            key = "Moves learned"
        elif key=="TM learned moves":
            key = "Moves learned by Training Machine"
        elif key=="Evoltion":
            key = "Evolution"
        elif key=="Evoltuion at levels":
            key = "Levels required to reach evolution stage"
        new_key = poke_name+"_"+key
        new_dict[new_key] = val
    data[i] = new_dict

## Limit text fields values to 20 words
for i in range(len(data)):
    d = data[i]
    new_dict = dict()
    poke_name = d['name']
    for key, val in d.items():
        if key=="name":
            new_dict[key] = val
            continue
        if key.split("_")[1] in {"Description", "Biology", "Evolution"}:
            if len(val.split(" "))>20:
                val = " ".join(val.split(" ")[:20])
        new_dict[key] = val
    data[i] = new_dict

## Add pokemon types
df_types = pd.read_csv("../data/Pokemon_types.csv")
for i in range(len(data)):
    poke_name = data[i]['name']
    data[i][poke_name+"_"+"Type"] = df_types['Types'].iloc[0]

## Update moveset
for i in range(len(data)):
    d = data[i]
    new_dict = dict()
    poke_name = d['name']
    k = poke_name + "_" + "Moves learned"
    move_dict = d[k]
    new_dict = dict()
    for move_name, info in move_dict.items():
        info["move_name"] = move_name
        new_dict[poke_name+ " learns the move "+move_name] = info
    d[k] = new_dict
    d["Moves learned by "+poke_name] = d.pop(k)
    data[i] = d

write_jsonl(data, "../data/pokemon_data_refined.jsonl")