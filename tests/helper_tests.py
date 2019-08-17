import unittest
import sys
import os
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
        get_data2 = {'citizens': [
                        {
                            'citizen_id': 10,
                            'town': 'Какая разница',
                            'street': 'Разница какая',
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
        result2 = helper.validation_import(get_data2)
        self.assertEqual(result2, True)

        # Case 3: incorrect field name
        get_data3 = {'citizens': [
                        {
                            'citizen_id': 10,
                            'town': 'Какая разница',
                            'street': 'Разница какая',
                            'building': 'Р',
                            'apartment': 123,
                            'name': 'Биек',
                            'birthday': '20.10.2015',
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
        result3 = helper.validation_import(get_data3)
        self.assertEqual(result3, True)

        # Case 4: incorrect value
        get_data4 = {'citizens': [
                    {
                        'citizen_id': 10,
                        'town': 'Какая разница',
                        'street': 'Разница какая',
                        'building': 20,
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
        result4 = helper.validation_import(get_data4)
        self.assertEqual(result4, True)

        # Case 5: incorrect relative connection
        get_data5 = {'citizens': [
                    {
                        'citizen_id': 10,
                        'town': 'Какая разница',
                        'street': 'Разница какая',
                        'building': '20',
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
                        'relatives': [4]
                    }
                ]}
        result5 = helper.validation_import(get_data5)
        self.assertEqual(result5, True)

        # Case 6: incorrect date
        get_data6 = {'citizens': [
                    {
                        'citizen_id': 10,
                        'town': 'Какая разница',
                        'street': 'Разница какая',
                        'building': '20',
                        'apartment': 123,
                        'name': 'Биек',
                        'birth_date': '31.02.2015',
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
        result6 = helper.validation_import(get_data6)
        self.assertEqual(result6, True)

        # Case 7: incorrect gender value
        get_data7 = {'citizens': [
            {
                'citizen_id': 10,
                'town': 'Какая разница',
                'street': 'Разница какая',
                'building': '20',
                'apartment': 123,
                'name': 'Биек',
                'birth_date': '30.10.2015',
                'gender': 'fimale',
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
        result7 = helper.validation_import(get_data7)
        self.assertEqual(result7, True)

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
        data2 = {
            'street': 'Какая разница',
            'bilding': '13',
            'name': 'Панда няш',
            'birth_date': '10.10.2010',
            'relatives': [10]
        }
        result2 = helper.validation_update(data2)
        self.assertEqual(result2, True)

        # Case 3: incorrect value
        data3 = {
            'street': 'Какая разница',
            'building': '13',
            'name': 'Панда няш',
            'birth_date': 25,
            'relatives': [10]
        }
        result3 = helper.validation_update(data3)
        self.assertEqual(result3, True)

        # Case 4: incorrect date
        get_data4 = {
            'street': 'Какая разница',
            'building': '13',
            'name': 'Панда няш',
            'birth_date': '31.02.2015',
            'relatives': [10]
        }
        result4 = helper.validation_update(get_data4)
        self.assertEqual(result4, True)

        # Case 5: incorrect gender value
        get_data5 = {
            'street': 'Какая разница',
            'building': '13',
            'name': 'Панда няш',
            'gender': 'fimale',
            'relatives': [10]
        }
        result5 = helper.validation_update(get_data5)
        self.assertEqual(result5, True)


if __name__ == '__main__':
    unittest.main()
