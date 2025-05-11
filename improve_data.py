import json

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
    

data = load_jsonl("pokemon_data_better_keys.jsonl")

def write_jsonl(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item)
            f.write(json_line + '\n')

# print(data[0])
# print(type(data[0]))
# print(data[0].keys())

## Used to general pokemon data with better keys. 
# for i in range(len(data)):
#     d = data[i]
#     new_dict = dict()
#     poke_name = d['name']
#     for key, val in d.items():
#         if key=="name":
#             new_dict[key] = val
#             continue
#         elif key=="Naturally learned moves":
#             key = "Moves learned"
#         elif key=="TM learned moves":
#             key = "Moves learned by Training Machine"
#         elif key=="Evoltion":
#             key = "Evolution"
#         elif key=="Evoltuion at levels":
#             key = "Levels required to reach evolution stage"
#         new_key = poke_name+"_"+key
#         new_dict[new_key] = val
#     data[i] = new_dict

# write_jsonl(data, "pokemon_data_better_keys.jsonl")


## Used to create data with limited text.
for i in range(len(data)):
    d = data[i]
    new_dict = dict()
    poke_name = d['name']
    for key, val in d.items():
        if key=="name":
            continue
        if key.split("_")[1] in {"Description", "Biology", "Evolution"}:
            if len(val.split(" "))>30:
                val = " ".join(val.split(" ")[:30])
        new_dict[key] = val
    data[i] = new_dict


write_jsonl(data, "pokemon_data_smaller_text_2.jsonl")