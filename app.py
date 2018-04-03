import os
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
    print r.text


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


def main():
    parser = argparse.ArgumentParser(
        description='Manage the Flask application.')
    parser.add_argument('-c', '--create', action='store_true',
            help='Create the application database.')
    parser.add_argument('-d', '--delete', action='store_true',
            help='Delete the application database.')
    parser.add_argument('-s', '--seedfile', dest="seedfile",
            help='The file with data for seeding the database.')
    args = parser.parse_args()

    # runserver()
    if args.command == 'create_db':
        create_db()
        print("DB created!")

    elif args.command == 'delete_db':
        drop_db()
        print("DB deleted!")

    elif args.command == 'seed_db' and args.seedfile:
        with open(args.seedfile, 'r') as f:
            seed_data = json.loads(f.read())

        for item_class in seed_data:
            items = seed_data[item_class]
            print(items)
            for item in items:
                print item
                create_sample_db_entry('api/' + item_class, item)

        print("\nSample data added to database!")
    else:
        raise Exception('Invalid command')

if __name__ == '__main__':
    main()
