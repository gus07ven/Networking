from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

# TODOS = {
#     'server1': {
#              'ip': '127.1.1.1',
#              'port': 1111
#     },
#     'server2': {
#                'ip': '127.2.2.2',
#                'port': 2222
#            },
#     'server3': {
#                'ip': '127.3.3.3',
#                'port': 3333
#            },
# }

TODOS = ['server1', 'server2']

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# Server: allows to get, delete, update, and create a new server.
class Server(Resource):
    def get(self, server_id):
        abort_if_todo_doesnt_exist(server_id)
        return TODOS[server_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

    def post(self):
        args = parser.parse.args()
        #server_id = int(max(TODOS.keys()).lstrip('server')) + 1
        #server_id = 'server%i' % server_id
        #TODOS[server_id] = {'task': args['task']}
        TODOS.append(args)
        return TODOS[server_id], 201


# Servers: shows a list of all todos, and lets you POST to add new tasks
class Servers(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        server_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        server_id = 'server%i' % server_id
        TODOS[server_id] = {'task': args['task']}
        return TODOS[server_id], 201


# Actually setup the Api resource routing here
api.add_resource(Servers, '/servers')
api.add_resource(Server, '/servers/<server_id>')

if __name__ == '__main__':
    app.run(debug=True)