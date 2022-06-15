import json

with open('test.json', 'r') as f:
    instance_list = f.readlines()

instance_list = [json.loads(instance) for instance in instance_list]

ref_list = [instance['summary'] for instance in instance_list]

with open('test.ref', 'w') as f:
    print(*ref_list, sep='\n', file=f, end='')