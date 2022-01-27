import json
from flask import Flask, request, Response
import bdd

app = Flask(__name__)
db_path = 'logiciel.db'
IP = '127.0.0.1'
PORT = '90'

@app.route('/log_in', methods=['post'])
def log_in_server():
    """ TODO """
    if not request.data:
        return 'fail'
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    x = prams.split()
    name = x[0]
    password = x[1]

    if bdd.log_in(db_path, name, password):
        return Response(status=200)
    else:
        return Response(status=500)

@app.route('/message', methods=['post'])
def handle_message():
    """ TODO """
    if not request.data:
        return 'fail'
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    print(prams)
    return prams


@app.route('/add_user', methods=['post'])
def addUser():
    """ TODO """
    if not request.data:
        return 'fail'
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    x = prams.split()
    name = x[0]
    password = x[1]
    print(name)
    print(password)
    if bdd.verify_name(name) is True and bdd.verify_password(password) is True:
        bdd.add_user(db_path, name, password, IP, PORT)
        print("User added")
        return params
    else:
        print("Wrong format of username or password")
        return params


@app.route('/ip', methods=['GET'])
def get_ip():
    """ TODO """
    name = request.args.get("name")
    return bdd.get_user_ip(db_path, name)[0][0]

@app.route('/isconnected', methods=['GET'])
def connexion():
    """ TODO """
    print("Client is connected")
    return Response(status=200)

@app.route('/get_store_key', methods=['post'])
def get_store_key():
    """ TODO """
    if not request.data:
        return 'fail'
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    x = prams.split()
    name_dest = x[0]
    name_user = x[1]

    print(name_dest)
    print(name_user)
    pub_key_dest = bdd.get_public_key(db_path, name_dest)

    if bdd.store_dest_public_key(db_path, name_user, pub_key_dest):
        return Response(status=200)
    else:
        return Response(status=500)

if __name__ == '__main__':
    bdd.delete_db(db_path)
    bdd.create_db(db_path)
    app.run(host=IP, port=PORT)
