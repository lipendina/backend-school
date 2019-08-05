from collections import defaultdict


fields = {
    'citizen_id': int,
    'town': str,
    'street': str,
    'building': str,
    'apartment': int,
    'name': str,
    'birth_date': str,
    'gender': str,
    'relatives': list
}


def tuple_to_dict(tup):
    return {
        'citizen_id': tup[0],
        'town': tup[1],
        'street': tup[2],
        'building': tup[3],
        'apartment': tup[4],
        'name': tup[5],
        'birth_date': tup[6],
        'gender': tup[7],
        'relatives': []
    }


def validation_import(get_data):
    for i in get_data['citizens']:
        if len(i.keys()) != len(fields.keys()):
            return True
        for key, value in i.items():
            if key not in fields.keys():
                return True
            if type(value) != fields[key]:
                return True
    dct = defaultdict(list)
    for i in get_data['citizens']:
        dct[i['citizen_id']] = i['relatives']

    for citizen, relatives in dct.items():
        for relative in relatives:
            if citizen not in dct[relative]:
                return True
    return False


def validation_update(get_data):
    for key, value in get_data.items():
        if key not in fields.keys():
            return True
        if type(value) != fields[key]:
            return True
    return False


def dict_to_string(dct):
    st = []
    for key, value in dct.items():
        if key == 'relatives':
            continue
        if type(value) is int:
            st.append('='.join([key, str(value)]))
        elif type(value) is str:
            st.append('{}="{}"'.format(key, value))
    return ', '.join(st)






