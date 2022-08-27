from tqdm import trange
import json

# input_dir = 'data/MixATIS_clean/'
input_dir = 'data/MixSNIPS_clean/'
# input_dir = 'data/MixSNIPS/'
# ref_dir = 'data/ATIS/'
ref_dir = 'data/SNIPS/'
# output_dir = 'data/MixATIS_clean_split/'
output_dir = 'data/MixSNIPS_clean_split_new/'

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

test_res_file = 'tools/MixSNIPS_split_MixSNIPS_split_intent_result.txt'
with open(test_res_file, 'r') as f:
    test_res_list = f.readlines()
test_res_list = [eval(res) for res in test_res_list]
test_res_pos = 0

test_cnt = 0
hit = 0
for filename in ['test.txt']: # ['dev.txt', 'test.txt', 'train.txt']:
    with open(input_dir + filename, 'r') as f:
        input_file = f.readlines()
    input_instances = read_instances(input_file)

    # fw = open(output_dir + filename[:-4] + '.txt', 'w')
    total_instances = len(input_instances)
    for no in trange(total_instances):
        instance = input_instances[no]
        input_text = ' '.join([word.split()[0] for word in instance[:-1]])
        output_text_list = []
        i = 0
        len_instance = len(instance)
        cnt_matched = 0
        all_true = True
        while i < len_instance:
            max_len_atom, max_atom = 0, []
            for atom in ref_instances:
                len_atom = len(atom)
                if len_instance - i + 1 >= len_atom - 1 and len_atom > max_len_atom and match(instance[i:], atom, len_atom):
                    # 
                    max_atom, max_len_atom = atom, len_atom
                    # break
            if max_len_atom > 0:
                cnt_matched += 1
                # print(*max_atom, file=fw, sep='', end='\n')
                i += max_len_atom - 1
                if test_res_list.pop(0) is False:
                    all_true = False
            else:
                i += 1
        # print(cnt_matched)
        if cnt_matched > 0:
            test_cnt += 1
            hit += 1 if all_true else 0

print(test_res_file, hit / test_cnt, hit, test_cnt, )

