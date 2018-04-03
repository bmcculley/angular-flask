import sys
import json
import argparse
import requests

from angular_flask import app
from angular_flask.core import db
from angular_flask.models import Post


def create_sample_db_entry(api_endpoint, payload):
    url = 'http://localhost:5000/' + api_endpoint
    r = requests.post(
        url, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'})
    print(r.text)


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()

def runserver(debug, host, port):
    app.run(debug=debug, host=host, port=port)


def main():
    parser = argparse.ArgumentParser(
        description='Manage the Flask application.')
    parser.add_argument('-c', '--create', dest='create_db', 
            action='store_true', help='Create the application database.')
    parser.add_argument('-e', '--erase', dest='delete_db', 
            action='store_true', help='Delete the application database.')
    parser.add_argument('-s', '--seedfile', dest='seedfile',
            help='The file with data for seeding the database.')
    parser.add_argument('-r', '--runserver', dest='run', 
            action='store_true', help='Start the Flask application server.')
    parser.add_argument('-d', '--debug', dest='debug',  action='store_true',
                    help='Start the app in debug mode.')
    parser.add_argument('-l', '--listen', dest='host', default='127.0.0.1',
                    help='Where should the server listen. \
                          Defaults to 127.0.0.1.')
    parser.add_argument('-p', '--port', dest='port', default=5000,
                    help='Which port should the server listen on. \
                          Defaults to 5000.')
    # if no args were supplied print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    # should check if trying to create/delete and/or run in the same command

    if args.run:
        runserver(debug, host, port)
    if args.create_db:
        create_db()
        print("DB created!")

    elif args.delete_db:
        drop_db()
        print("DB deleted!")

    # not sure about this yet, i'm thinking it should be removed
    elif args.seedfile not None:
        with open(args.seedfile, 'r') as f:
            seed_data = json.loads(f.read())

        for item_class in seed_data:
            items = seed_data[item_class]
            print(items)
            for item in items:
                print(item)
                create_sample_db_entry('api/' + item_class, item)
        print("\nSample data added to database!")
    else:
        raise Exception('Invalid command')

if __name__ == '__main__':
    main()
