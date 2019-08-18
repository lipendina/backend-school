import unittest
import sys
import os
import copy
path = os.path.abspath(__file__).split('\\')
sys.path.append('\\'.join(path[:-2]))
import helper


class TestHelper(unittest.TestCase):
    def test_tuple_to_dict(self):
        # Case 1: correct data
        tup = (3, 'Москва', 'Ленинский проспект', 'дом 77', 232, 'Иван Иванов', '09.12.1990', 'male')
        dct = helper.tuple_to_dict(tup)
        self.assertEqual(type(dct), dict)

        expected_dict = {
            'citizen_id': 3,
            'town': 'Москва',
            'street': 'Ленинский проспект',
            'building': 'дом 77',
            'apartment': 232,
            'name': 'Иван Иванов',
            'birth_date': '09.12.1990',
            'gender': 'male',
            'relatives': []
        }
        self.assertEqual(dct, expected_dict)

    def test_dict_to_string(self):
        # Case 1: correct data
        dct = {
            'citizen_id': 3,
            'town': 'Волгогрвд',
            'street': 'ул. Мира',
            'building': '13',
            'apartment': 4,
            'name': 'Панда',
            'birth_date': '10.10.2010',
            'gender': 'male',
            'relatives': [10]
        }
        st = helper.dict_to_string(dct)
        self.assertEqual(type(st), str)

    def test_validation_import(self):
        # Case 1: correct data
        get_data1 = {'citizens': [
                        {
                            'citizen_id': 10,
                            'town': 'Какая разница',
                            'street': 'Разница какая',
                            'building': 'Р',
                            'apartment': 123,
                            'name': 'Биек',
                            'birth_date': '20.10.2015',
                            'gender': 'female',
                            'relatives': [3]
                        },
                        {
                            'citizen_id': 3,
                            'town': 'Вагагад',
                            'street': 'Гад',
                            'building': '13',
                            'apartment': 4,
                            'name': 'Панда',
                            'birth_date': '10.10.2010',
                            'gender': 'male',
                            'relatives': [10]
                        }
                    ]}
        result1 = helper.validation_import(get_data1)
        self.assertEqual(result1, False)

        # Case 2: incorrect quantity of fields
        get_data2 = copy.deepcopy(get_data1)
        get_data2['citizens'][0].pop('birth_date')
        result2 = helper.validation_import(get_data2)
        self.assertEqual(result2, True)

        # Case 3: incorrect field name
        get_data3 = copy.deepcopy(get_data1)
        get_data3['citizens'][0].pop('birth_date')
        get_data3['citizens'][0]['birthday'] = '01.01.2000'
        result3 = helper.validation_import(get_data3)
        self.assertEqual(result3, True)

        # Case 4: incorrect value
        get_data4 = copy.deepcopy(get_data1)
        get_data4['citizens'][0]['building'] = 123
        result4 = helper.validation_import(get_data4)
        self.assertEqual(result4, True)

        # Case 5: incorrect relative connection
        get_data5 = copy.deepcopy(get_data1)
        get_data5['citizens'][1]['relatives'] = [4]
        result5 = helper.validation_import(get_data5)
        self.assertEqual(result5, True)

        # Case 6: incorrect date
        get_data6 = copy.deepcopy(get_data1)
        get_data6['citizens'][0]['birth_date'] = '31.02.2015'
        result6 = helper.validation_import(get_data6)
        self.assertEqual(result6, True)

        # Case 7: incorrect gender value
        get_data7 = copy.deepcopy(get_data1)
        get_data7['citizens'][0]['gender'] = 'fimale'
        result7 = helper.validation_import(get_data7)
        self.assertEqual(result7, True)

        get_data8 = copy.deepcopy(get_data1)
        get_data8['citizens'][0]['apartment'] = -5
        result8 = helper.validation_import(get_data8)
        self.assertEqual(result8, True)

    def test_validation_update(self):
        # Case 1: correct data
        data1 = {
            'street': 'Какая разница',
            'building': '13',
            'name': 'Панда няш',
            'birth_date': '10.10.2010',
            'relatives': [10]
        }
        result1 = helper.validation_update(data1)
        self.assertEqual(result1, False)

        # Case 2: incorrect field name
        data2 = copy.deepcopy(data1)
        data2.pop('building')
        data2['bilding'] = '13'
        result2 = helper.validation_update(data2)
        self.assertEqual(result2, True)

        # Case 3: incorrect value
        data3 = copy.deepcopy(data1)
        data3['birth_date'] = 25
        result3 = helper.validation_update(data3)
        self.assertEqual(result3, True)

        # Case 4: incorrect date
        data4 = copy.deepcopy(data1)
        data4['birth_date'] = '31.02.2014'
        result4 = helper.validation_update(data4)
        self.assertEqual(result4, True)

        # Case 5: incorrect gender value
        data5 = copy.deepcopy(data1)
        data5['gender'] = 'fimale'
        result5 = helper.validation_update(data5)
        self.assertEqual(result5, True)

    def test_validation_date(self):
        # Case 1: correct date
        citizen = {
            'birth_date': '25.01.1990'
        }
        self.assertFalse(helper.validation_date(citizen))

        # Case 2: incorrect date
        citizen = {
            'birth_date': '25.01.2030'
        }
        self.assertTrue(helper.validation_date(citizen))

        # Case 3: incorrect format date
        citizen = {
            'birth_date': '2510year'
        }
        self.assertTrue(helper.validation_date(citizen))


if __name__ == '__main__':
    unittest.main()
