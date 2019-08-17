import unittest
import sys
import os
path = os.path.abspath(__file__).split('\\')
sys.path.append('\\'.join(path[:-2]))
import database



class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = database.Database('testdatabase.db')

    @classmethod
    def tearDownClass(cls):
        os.remove('testdatabase.db')

    def test_create(self):
        # Case 1: presence of database
        self.assertEqual(os.path.isfile('testdatabase.db'), True)

        # Case 2: table schema of 'citizens'
        query1 = 'PRAGMA table_info(citizens)'
        result1 = self.db.execute_query(query1)
        data1 = {}
        expected_result1 = {
            'id': 'INTEGER',
            'import_id': 'INTEGER',
            'citizen_id': 'INTEGER',
            'town': 'TEXT',
            'street': 'TEXT',
            'building': 'TEXT',
            'apartment': 'INTEGER',
            'name': 'TEXT',
            'birth_date': 'TEXT',
            'gender': 'TEXT'
        }
        for tup in result1:
            data1[tup[1]] = tup[2]
        self.assertEqual(expected_result1, data1)

        # Case 3: table schema of 'relatives'
        query2 = 'PRAGMA table_info(relatives)'
        result2 = self.db.execute_query(query2)
        data2 = {}
        expected_result2 = {
            'id': 'INTEGER',
            'import_id': 'INTEGER',
            'citizen_id': 'INTEGER',
            'relative_id': 'INTEGER'
        }
        for tup in result2:
            data2[tup[1]] = tup[2]
        self.assertEqual(expected_result2, data2)

    def test_execute_many(self):
        # Case 1: insert into table 'citizens'
        data_citizens = [(3, 4, 'Волгоград', 'ул. Рокоссовского', '52а', 113, 'Иванов Иван', '10.10.2000', 'male')]
        add_query1 = 'INSERT INTO citizens (import_id, citizen_id, town, street, building, apartment,' \
                     'name, birth_date, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.db.execute_many(add_query1, data_citizens)
        select_query1 = 'SELECT import_id, citizen_id, town, street, building, apartment, name, birth_date, gender ' \
                        'FROM citizens WHERE import_id=3 AND citizen_id=4'
        res_citizens = self.db.execute_query(select_query1)
        self.assertEqual(res_citizens, data_citizens)

        # Case 2: insert into table 'relatives'
        data_relatives = [(3, 4, 2)]
        add_query2 = 'INSERT INTO relatives (import_id, citizen_id, relative_id) VALUES (?, ?, ?)'
        self.db.execute_many(add_query2, data_relatives)
        select_query2 = 'SELECT import_id, citizen_id, relative_id FROM relatives WHERE import_id=3 AND citizen_id=4'
        res_relatives = self.db.execute_query(select_query2)
        self.assertEqual(res_relatives, data_relatives)

    def test_execute_query(self):
        # Case 1: updating data of citizen
        update_query = 'UPDATE citizens SET apartment=345 WHERE import_id=3 AND citizen_id=4'
        self.db.execute_query(update_query)
        select_query1 = 'SELECT import_id, citizen_id, town, street, building, apartment, name, birth_date, gender ' \
                        'FROM citizens WHERE import_id=3 AND citizen_id=4'
        res_update = self.db.execute_query(select_query1)
        updated_data = [(3, 4, 'Волгоград', 'ул. Рокоссовского', '52а', 345, 'Иванов Иван', '10.10.2000', 'male')]
        self.assertEqual(res_update, updated_data)

        # Case 2: data deletion
        delete_query = 'DELETE FROM citizens WHERE import_id=3 AND citizen_id=4'
        self.db.execute_query(delete_query)
        select_query2 = 'SELECT import_id, citizen_id, town, street, building, apartment, name, birth_date, gender ' \
                        'FROM citizens WHERE import_id=3 AND citizen_id=4'
        result = self.db.execute_query(select_query2)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
