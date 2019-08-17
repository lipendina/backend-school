import unittest
import requests
import json
import multiprocessing
import sys
import os
path = os.path.abspath(__file__).split('\\')
sys.path.append('\\'.join(path[:-2]))
from main import Application

app = Application('testbase.db')


def run_app():
    app.run()


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.thr = multiprocessing.Process(target=run_app)
        cls.thr.start()

        data = {
            (1, 1, 'Волгоград', 'ул. Рокоссовского', '52а', 113, 'Иванов Иван', '10.10.2000', 'male'),
            (1, 2, 'Волжский', 'пл. Труда', '17', 112, 'Белек', '15.02.1990', 'female'),
            (1, 3, 'Москва', 'ул. Зеленоградская', '17к5', 333, 'Панда', '25.01.1990', 'male')
        }
        add_query1 = 'INSERT INTO citizens (import_id, citizen_id, town, street, building, apartment,' \
                     'name, birth_date, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        app.db.execute_many(add_query1, data)

        rel = {
            (1, 1, 2),
            (1, 2, 1),
            (1, 3, 2),
            (1, 2, 3)
        }
        add_query2 = 'INSERT INTO relatives (import_id, citizen_id, relative_id) VALUES (?, ?, ?)'
        app.db.execute_many(add_query2, rel)

    @classmethod
    def tearDownClass(cls):
        cls.thr.terminate()
        os.remove('testbase.db')

    def test_add_citizen(self):
        url = 'http://localhost:8080/imports'

        # Case 1: correct data
        expected_data = {
                            "data": {
                                "import_id": 2
                            }
                        }

        post_fields1 = {'citizens': [
            {
                'citizen_id': 3,
                'town': 'Вагагад',
                'street': 'Гад',
                'building': '13',
                'apartment': 4,
                'name': 'Панданяш',
                'birth_date': '10.10.2010',
                'gender': 'male',
                'relatives': [10]
            },
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
            }
        ]}

        r1 = requests.post(url=url, data=json.dumps(post_fields1))
        get_data = json.loads(r1.text)
        self.assertEqual(r1.status_code, 201)
        self.assertEqual(get_data, expected_data)

        # Case 2: incorrect quantity of fields
        post_fields2 = {'citizens': [
            {
                'citizen_id': 10,
                'town': 'Какая разница',
                'street': 'Разница какая',
                'building': '22',
                'apartment': 88,
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
                'birth_date': '10.10.2010',
                'gender': 'male',
                'relatives': [10]
            }
        ]}
        r2 = requests.post(url=url, data=json.dumps(post_fields2))
        self.assertEqual(r2.status_code, 400)

        # Case 3: incorrect field name
        post_fields3 = {'citizens': [
            {
                'citizen_id': 10,
                'city': 'Какая разница',
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
        r3 = requests.post(url=url, data=json.dumps(post_fields3))
        self.assertEqual(r3.status_code, 400)

        # Case 4: incorrect value
        post_fields4 = {'citizens': [
            {
                'citizen_id': 10,
                'town': 'Какая разница',
                'street': 'Разница какая',
                'building': '20',
                'apartment': 'кв. 120',
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
        r4 = requests.post(url=url, data=json.dumps(post_fields4))
        self.assertEqual(r4.status_code, 400)

        # Case 5: incorrect relative connection
        post_fields5 = {'citizens': [
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
                'relatives': [8]
            }
        ]}
        r5 = requests.post(url=url, data=json.dumps(post_fields5))
        self.assertEqual(r5.status_code, 400)

    def test_update_citizen(self):
        url = 'http://localhost:8080/imports/{}/citizens/{}'.format(1, 2)

        # Case 1: correct data
        post_fields1 = {
            'name': 'Татьяна',
            'birth_date': '02.02.1997',
        }
        expected_data = {
            "data": {
                "citizen_id": 2,
                "town": "Волжский",
                "street": "пл. Труда",
                "building": "17",
                "apartment": 112,
                "name": "Татьяна",
                "birth_date": "02.02.1997",
                "gender": "female",
                "relatives": [1, 3]
            }
        }
        r1 = requests.patch(url=url, data=json.dumps(post_fields1))
        get_data = json.loads(r1.text)
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(get_data, expected_data)

        # Case 2: incorrect field name
        post_fields2 = {
                "city": "Волгоград",
        }
        r2 = requests.patch(url=url, data=json.dumps(post_fields2))
        self.assertEqual(r2.status_code, 400)

        # Case 3: incorrect type of value
        post_fields3 = {
            "apartment": '113'
        }
        r3 = requests.patch(url=url, data=json.dumps(post_fields3))
        self.assertEqual(r3.status_code, 400)

        # Case 4: relatives connection
        post_fields4 = {
            'relatives': [3]
        }
        expected_data2 = {
            "data": {
                "citizen_id": 2,
                "town": "Волжский",
                "street": "пл. Труда",
                "building": "17",
                "apartment": 112,
                "name": "Татьяна",
                "birth_date": "02.02.1997",
                "gender": "female",
                "relatives": [3]
            }
        }
        r4 = requests.patch(url=url, data=json.dumps(post_fields4))
        get_data = json.loads(r4.text)
        self.assertEqual(r4.status_code, 200)
        self.assertEqual(get_data, expected_data2)

    def test_all_citizen(self):
        url = 'http://localhost:8080/imports/1/citizens'
        expected_data = {
            "data": [
                {
                    "citizen_id": 1,
                    "town": "Волгоград",
                    "street": "ул. Рокоссовского",
                    "building": "52а",
                    "apartment": 113,
                    "name": "Иванов Иван",
                    "birth_date": "10.10.2000",
                    "gender": "male",
                    "relatives": [2]
                },
                {
                    "citizen_id": 2,
                    "town": "Волжский",
                    "street": "пл. Труда",
                    "building": "17",
                    "apartment": 112,
                    "name": "Белек",
                    "birth_date": "15.02.1990",
                    "gender": "female",
                    "relatives": [1, 3]
                },
                {
                    "citizen_id": 3,
                    "town": "Москва",
                    "street": "ул. Зеленоградская",
                    "building": "17к5",
                    "apartment": 333,
                    "name": "Панда",
                    "birth_date": "25.01.1990",
                    "gender": "male",
                    "relatives": [2]
                }
            ]
        }
        get_data = requests.get(url=url)
        self.assertEqual(get_data.status_code, 200)
        citizens = json.loads(get_data.text)
        citizens['data'].sort(key=lambda citizen: citizen["citizen_id"])
        self.assertEqual(citizens, expected_data)

    def test_by_gifts(self):
        url = 'http://localhost:8080/imports/1/citizens/birthdays'
        expected_data = {
                            "data": {
                              "1": [
                                  {
                                      "citizen_id": 2,
                                      "presents": 1,
                                  }
                              ],
                              "2": [
                                  {
                                      "citizen_id": 1,
                                      "presents": 1,
                                  },
                                  {
                                      "citizen_id": 3,
                                      "presents": 1,
                                  }
                              ],
                              "3": [],
                              "4": [],
                              "5": [],
                              "6": [],
                              "7": [],
                              "8": [],
                              "9": [],
                              "10": [
                                  {
                                      "citizen_id": 2,
                                      "presents": 1,
                                  }
                              ],
                              "11": [],
                              "12": []
                            }
                        }

        get_data = requests.get(url=url)
        self.assertEqual(get_data.status_code, 200)
        gifts = json.loads(get_data.text)
        self.assertEqual(gifts, expected_data)

    def test_by_age(self):
        url = 'http://localhost:8080/imports/1/towns/stat/percentile/age'
        expected_data = {
                            "data": [
                                {
                                    "town": "Волгоград",
                                    "p50": 18.0,
                                    "p75": 18.0,
                                    "p99": 18.0
                                },
                                {
                                    "town": "Волжский",
                                    "p50": 29.0,
                                    "p75": 29.0,
                                    "p99": 29.0
                                },
                                {
                                    "town": "Москва",
                                    "p50": 29.0,
                                    "p75": 29.0,
                                    "p99": 29.0
                                }
                            ]
                        }

        get_data = requests.get(url=url)
        self.assertEqual(get_data.status_code, 200)
        ages = json.loads(get_data.text)
        ages['data'].sort(key=lambda x: x['town'])
        self.assertEqual(ages, expected_data)


if __name__ == '__main__':
    unittest.main()
