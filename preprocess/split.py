from tqdm import trange
# input_dir = 'data/MixSNIPS_clean/'
input_dir = 'data/MixSNIPS/'
ref_dir = 'data/SNIPS/'
output_dir = 'data/MixSNIPS_split/'

def read_instances(input_file):
    instance = []
    instance_list = []
    for line in input_file:
        if line != '\n':
            instance.append(line)
        else:
            instance_list.append(instance)
            instance = []
    return instance_list

def match(instance, atom, n):
    for i in range(n-1):
        if instance[i] != atom[i]:
            return False
    return True

for filename in ['dev.txt', 'test.txt', 'train.txt']:
    with open(input_dir + filename, 'r') as f:
        input_file = f.readlines()
    input_instances = read_instances(input_file)

    with open(ref_dir + filename, 'r') as f:
        ref_file = f.readlines()
    ref_instances = read_instances(ref_file)

    fw = open(output_dir + filename, 'w')
    total_instances = len(input_instances)
    for no in trange(total_instances):
        instance = input_instances[no]
        i = 0
        len_instance = len(instance)
        while i < len_instance:
            for atom in ref_instances:
                len_atom = len(atom)
                if len_instance - i + 1 >= len_atom - 1 and match(instance[i:], atom, len_atom):
                    print(*atom, file=fw, sep='', end='\n')
                    i += len_atom - 1
                    break
            i += 1
