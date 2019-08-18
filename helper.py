import math
from collections import defaultdict
from datetime import datetime


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


def validation_date(citizen):
    try:
        datetime.strptime(citizen['birth_date'], '%d.%m.%Y')
    except (ValueError, TypeError):
        return True
    return False


def validation_import(get_data):
    for i in get_data['citizens']:
        if len(i.keys()) != len(fields.keys()):
            return True
        for key, value in i.items():
            if key not in fields.keys():
                return True
            if type(value) != fields[key]:
                return True
        if validation_date(i):
            return True
        if i['gender'] != 'male' and i['gender'] != 'female':
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
    if 'birth_date' in get_data.keys():
        if validation_date(get_data):
            return True
    if 'gender' in get_data.keys():
        if get_data['gender'] != 'male' and get_data['gender'] != 'female':
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


def percentile(arr, percents):
    if not arr:
        return
    answ = []
    arr.sort()
    for percent in percents:
        val_k = ((len(arr) - 1) * percent) / 100
        val_cl = math.ceil(val_k)
        val_fl = math.floor(val_k)
        if val_cl == val_fl:
            answ.append(arr[int(val_k)])
        else:
            left, right = arr[int(val_fl)] * (val_cl - val_k), arr[int(val_cl)] * (val_k - val_fl)
            answ.append(left + right)
    return answ

