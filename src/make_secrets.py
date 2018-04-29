import os
import logging
import getpass

path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
path = os.path.join(path_dir, 'secrets')


if __name__ == '__main__':
    mongousername = input("Enter your mongo username: ")
    mongopassword = getpass.getpass("Enter your mongo password: ")

    entries = [
        f"MONGO_USER={mongousername}",
        f"MONGO_PASS={mongopassword}",
    ]

    with open(path, 'w') as file_:
        for entry in entries:
            file_.write(f"{entry}\n")

    logging.info(f"Wrote secrets to {path}")
