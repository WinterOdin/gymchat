import pandas as pd
import json
import copy
with open('exercises.json','r') as f:
    data = json.loads(f.read())

df = pd.json_normalize(data, record_path = ['exercises'])

parsed_df = df[['name', 'category']]
parsed_df.loc[:, 'authorized'] = True
parsed_df.index = parsed_df.index + 1

with open('template.json','r') as f:
    data_template = json.loads(f.read())

dict_list = []

for index, row in parsed_df.iterrows():
    new_template = copy.deepcopy(data_template)
    new_template['pk'] = index
    new_template['fields']['name'] = row['name']
    new_template['fields']['category'] = row['category']
    new_template['fields']['authorized'] = row['authorized']
    dict_list.append(new_template)

    
# output_file = open('converted.json', 'w', encoding='utf-8')
# for dic in dict_list:
#     json.dump(dic, output_file) 
#     output_file.write("\n")
with open('converted.json', 'w') as fout:
    json.dump(dict_list , fout, indent=4)
