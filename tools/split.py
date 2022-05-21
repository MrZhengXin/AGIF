from tqdm import trange
import json

input_dir = 'data/MixSNIPS_clean/'
# input_dir = 'data/MixSNIPS/'
ref_dir = 'data/SNIPS/'
output_dir = 'data/MixSNIPS_clean_seq2seq/'

def read_instances(input_file):
    instance = []
    instance_list = []
    for line in input_file:
        if line != '\n':
            instance.append(line)
        else:
            instance_list.append(instance)
            instance = []
    if instance != []:
        instance_list.append(instance)
    return instance_list

def match(instance, atom, n):
    for i in range(n-1):
        if instance[i] != atom[i]:
            return False
    return True

ref_instances = []
for filename in ['dev.txt', 'test.txt', 'train.txt']:
    with open(ref_dir + filename, 'r') as f:
        ref_file = f.readlines()
    ref_instances += read_instances(ref_file)

for filename in ['dev.txt', 'test.txt', 'train.txt']:
    with open(input_dir + filename, 'r') as f:
        input_file = f.readlines()
    input_instances = read_instances(input_file)

    fw = open(output_dir + filename[:-4] + '.json', 'w')
    total_instances = len(input_instances)
    for no in trange(total_instances):
        instance = input_instances[no]
        input_text = ' '.join([word.split()[0] for word in instance[:-1]])
        output_text_list = []
        i = 0
        len_instance = len(instance)
        cnt_matched = 0
        while i < len_instance:
            max_len_atom, max_atom = 0, []
            for atom in ref_instances:
                len_atom = len(atom)
                if len_instance - i + 1 >= len_atom - 1 and len_atom > max_len_atom and match(instance[i:], atom, len_atom):
                    # print(*atom, file=fw, sep='', end='\n')
                    max_atom, max_len_atom = atom, len_atom
                    # break
            if max_len_atom > 0:
                cnt_matched += 1
                output_text_list.append(
                    ' '.join([word.split()[0] for word in max_atom[:-1]])
                )
                i += max_len_atom - 1
            else:
                i += 1
        output_text = '; '.join(output_text_list)
        if (len(output_text.split()) + cnt_matched) / len(input_text.split()) >= 0.8:
            print(json.dumps({
                'text': input_text, 'summary': output_text}
                ), file=fw
            )
        else:
            print(input_text, output_text, sep='\n', end='\n\n')
