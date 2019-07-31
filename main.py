from flask import Flask, Response, request
import json
import database
import helper
from datetime import datetime
from collections import defaultdict
import numpy


class Application(object):
    def init_http_server(self):
        app = self.app

        @app.route('/imports', methods=['POST'])
        def add_citizen():
            get_data = json.loads(request.data)
            import_id = self.db.execute_query('your query') + 1
            # check citizens
            # insert database
            return_data = {

            }
            return Response(json.dumps(return_data, indent=2), status=201, content_type='application/json')

        @app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PUT'])
        def update_citizen(import_id, citizen_id):
            return_data = {
                'data': '/imports/{}/citizens/{}'.format(import_id, citizen_id)
            }
            return Response(json.dumps(return_data, indent=2), status=200, content_type='application/json')

        @app.route('/imports/<import_id>/citizens', methods=['GET'])
        def all_citizens(import_id):
            query1 = 'SELECT citizens_id, town, street, building, apartment, name, ' \
                    'birth_date, gender FROM citizens WHERE import_id = {}'.format(import_id)
            result1 = self.db.execute_query(query1)
            dct = {}
            for i in result1:
                dct[i[0]] = helper.tuple_to_dict(i)

            query2 = 'SELECT citizen_id, relative_id FROM relatives WHERE import_id = {}'.format(import_id)
            result2 = self.db.execute_query(query2)
            for i in result2:
                dct[i[0]]['relatives'].append(i[1])

            return_data = {
                'data': [i for i in dct.values()]
            }
            return Response(json.dumps(return_data, indent=2, ensure_ascii=False), status=200,
                            content_type='application/json')

        @app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
        def by_gifts(import_id):
            query = 'SELECT relatives.citizen_id, relatives.relative_id, citizens.birth_date ' \
                    'FROM relatives, citizens WHERE relatives.relative_id = citizens.citizens_id ' \
                    'AND citizens.import_id = {}'.format(import_id)
            result = self.db.execute_query(query)

            dct = {}
            for i in result:
                d = datetime.strptime(i[2], '%d.%m.%Y')
                if dct.get(d.month) is None:
                    dct[d.month] = defaultdict(int)
                dct[d.month][i[0]] += 1

            data = {}
            for i in range(1, 13):
                data[i] = []
                if dct.get(i) is None:
                    continue
                for key, value in dct[i].items():
                    data[i].append({'citizen_id': key, 'presents': value})

            return_data = {
                'data': data
            }
            return Response(json.dumps(return_data, indent=2, ensure_ascii=False), status=200,
                            content_type='application/json')

        @app.route('/imports/<import_id>/towns/stat/percentile/age', methods=['GET'])
        def by_age(import_id):
            query = 'SELECT town, birth_date FROM citizens WHERE import_id = {}'.format(import_id)
            result = self.db.execute_query(query)
            dct = defaultdict(list)
            for i in result:
                birth_date = datetime.strptime(i[1], '%d.%m.%Y')
                now = datetime.now().date()
                if (now.month, now.day) > (birth_date.month, birth_date.day):
                    age = now.year - birth_date.year
                else:
                    age = now.year - birth_date.year - 1

                dct[i[0]].append(age)

            data = []
            for key, value in dct.items():
                data.append({'town': key, 'p50': int(numpy.percentile(value, 50, interpolation='linear')),
                             'p75': int(numpy.percentile(value, 75, interpolation='linear')),
                             'p99': int(numpy.percentile(value, 99, interpolation='linear'))})

            return_data = {
                'data': data
            }

            return Response(json.dumps(return_data, indent=2, ensure_ascii=False), status=200,
                            content_type='application/json')

    def __init__(self):
        self.app = Flask(__name__)
        self.init_http_server()
        self.db = database.Database('sqlite.db')

    def run(self):
        self.app.run(host='localhost', port=8080)


if __name__ == '__main__':
    server = Application()
    server.run()