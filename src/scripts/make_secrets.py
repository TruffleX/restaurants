import os
import logging
import getpass

path_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
path = os.path.join(path_dir, 'secrets')


if __name__ == '__main__':
    mongousername = input("Enter your mongo username: ")
    mongopassword = getpass.getpass("Enter your mongo password: ")
    googlemapskey = getpass.getpass("Paste your google maps api key: ")
    yelp_api_key = getpass.getpass("Paste your yelp api key: ")
    yelp_client_id = getpass.getpass("[Optional?] Paste your yelp client ID: ")

    entries = [
        "MONGO_USER={mongousername}".format(mongousername=mongousername),
        "MONGO_PASS={mongopassword}".format(mongopassword=mongopassword),
        "GOOGLE_MAPS_API_KEY={googlemapskey}".format(googlemapskey=googlemapskey),
        "YELP_API_KEY={yelp_api_key}".format(yelp_api_key=yelp_api_key),
        "YELP_CLIENT_ID={yelp_client_id}".format(yelp_client_id=yelp_client_id)
    ]

    with open(path, 'w') as file_:
        for entry in entries:
            file_.write("{entry}\n".format(entry=entry))

    logging.info("Wrote secrets to {path}".format(path=path))
