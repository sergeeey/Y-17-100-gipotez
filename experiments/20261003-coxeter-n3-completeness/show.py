import json,sys
for f in sys.argv[1:]:
    for line in open(f,encoding='utf8'):
        if line.startswith('{'):
            o=json.loads(line); print(f, 'p=',o['p'],'maxlab=',o['maxlab'],'combos',o['n_combos'],'secs',o['secs'])
            print('  iso per d:', {d:v['iso_classes'] for d,v in o['per_d'].items()}, 'total', sum(v['iso_classes'] for v in o['per_d'].values()), 'euler_bad', sum(v['euler_bad'] for v in o['per_d'].values()), 'vin!=geo', sum(abs(v['vin']-v['geo']) for v in o['per_d'].values()))
