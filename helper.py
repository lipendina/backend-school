from collections import defaultdict


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


def validation(get_data):
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

