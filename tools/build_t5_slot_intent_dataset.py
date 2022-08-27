data_dir_list = ['ATIS', 'MixATIS_clean', 'MixATIS_clean_split', 'SNIPS', 'MixSNIPS', 'MixSNIPS_split']

import os
import json

def read_instances(input_file):
    instance = []
    instance_list = []
    for line in input_file:
        if line != '\n':
            instance.append(line.strip())
        else:
            instance_list.append(instance)
            instance = []
    if instance != []:
        instance_list.append(instance)
    return instance_list

for data_dir in data_dir_list:
    output_dir_path = os.path.join('data', data_dir + '_t5_intent')
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    for filename in ['dev.txt', 'test.txt', 'train.txt']:
        fw = open(os.path.join(output_dir_path, filename.replace('.txt', '.json')), 'w')
        with open(os.path.join('data', data_dir, filename), 'r') as f:
            lines = f.readlines()
        instance_list = read_instances(lines)
        for instance in instance_list:
            tokens = ""
            labels = ""

            # intent is at the end of the lines
            for line in instance[:-1]:
                token, label = line.split()
                tokens += token + ' '
                # labels += '<%s>' % label + ' ' # token + ' <%s>' % label + ' '
            # intents = instance[-1].split('#') if data_dir in ['MixATIS_clean', 'MixSNIPS_clean'] else [instance[-1]]
            # intents = ['<%s>' % intent for intent in intents]
            # labels += ' '.join(intents)
            labels = instance[-1].replace('#', ' ')
            print(
                json.dumps({
                    "text": tokens.strip(),
                    "summary": labels.strip()
                }), file=fw
            )


        