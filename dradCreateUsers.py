#!/usr/bin/env python3
"""
Description: Creates user specific secrets
Use: Once per user
"""
import crypt
import hashlib
import json
from argparse import ArgumentParser


def main(user_list, outfile):
    """writes user secrets to json file
    args:
        users_ (string): string of users and pins seperated by colons e.g. user1:123456789
        outfile (string): name of file to write user_secrets to """
    try:
        secrets = open(outfile, "w")
        print()
    except Exception as e:
        print("Unable to open secrets file: %s" % (e,))
        return 0

    try:
        user_dict = {user.split(":")[0]: {"pin": user.split(":")[1], "id": num} for num, user in enumerate(user_list)}
    except IndexError:
        raise Exception(
            "Unable to parse user name and pin. Please make sure you entered the user-list as "
            "space seperated pairs of usernames and pins. Example: --user-list user1:12345678 user2:12345689")
    info = json.dumps(user_dict)
    secrets.write(info)
    secrets.close()


def get_args():
    """gets arguments from command line"""
    parser = ArgumentParser(description='main interface to provision system')
    parser.add_argument('--user-list', nargs='+',
                        help='list of users and pins seperated by a colon: "user1:12345678 user2:12345679" ',
                        required=True)
    parser.add_argument('--outfile', help='location to save user secrets file', required=True)
    args = parser.parse_args()
    return args.user_list, args.outfile


if __name__ == '__main__':
    users, loc = get_args()
    print(users)
    print(type(users))
    newUsers = []
    for key in users:
        oldusr = key.split(":")[0]
        oldpin = key.split(":")[1]
        newkey = hashlib.sha256(oldusr.encode('utf-8')).hexdigest()
        newkey = str(newkey)+":"
        newkey = str(newkey)+str(hashlib.sha256(oldpin.encode('utf-8')).hexdigest())
        newUsers.append(newkey)
        print(newkey)
    print(newUsers)
    print("generating user specific secrets")
    main(newUsers, loc)
