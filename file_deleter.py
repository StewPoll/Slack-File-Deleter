"""
The script deletes all files uploaded to your slack team, older than a given number of weeks.
Default number of weeks is 4.

USAGE:
python file_delete.py token [number_of_weeks]

PARAMS:
---
token (REQUIRED): Slack API token, available at https://api.slack.com/web
number_of_weeks (OPTIONAL): Integer - Defaults to 4.
"""
__author__ = 'TetraEtc'
from slacker import Slacker
import sys
from datetime import timedelta, datetime


def main(token, weeks):
    """
    Main function
    :param token: Available at. https://api.slack.com/web. REQUIRED
    :param weeks: Optional number of weeks. Defaults to 4
    :return:
    """
    slack = Slacker(token)
    # Get list of all files available for the user of the token
    total = slack.files.list(count=1).body['paging']['total']
    num_pages = round(total/1000.00 + .5) # Get number of pages
    print("{} files to be processed, across {} pages".format(total, num_pages))
    # Get files
    files_to_delete = []
    ids = [] # For checking that the API doesn't return duplicate files (Don't think it does, doesn't hurt to be sure
    count = 1
    for page in range(num_pages):
        print ("Pulling page number {}".format(page + 1))
        files = slack.files.list(count=1000, page=page+1).body['files']
        for file in files:
            print("Checking file number {}".format(count))
            # Checking for duplicates
            if file['id'] not in ids:
                ids.append(file['id'])
                if datetime.fromtimestamp(file['timestamp']) < datetime.now() - timedelta(weeks=weeks):
                    files_to_delete.append(file)
                    print("File No. {} will be deleted".format(count))
                else:
                    print ("File No. {} will not be deleted".format(count))
            count+=1

    print("All files checked\nProceeding to delete files")
    print("{} files will be deleted!".format(len(files_to_delete)))
    count = 1
    for file in files_to_delete:
        print("Deleting file {} of {}".format(count, len(files_to_delete)))
        slack.files.delete(file_=file['id'])
        print("Deleted Successfully")
        count += 1


if __name__ == "__main__":
    weeks = 4
    try:
        args = sys.argv[1:]
        token = args [0]
        if len(args) > 1:
            try:
                weeks=int(args[1])
            except ValueError:
                print("If given, second argument must be of type int")
                sys.exit(2)
    except IndexError:
        print("Please provide an API Token")
        print("Usage: python file_deleter.py api_token [weeks]")
        sys.exit(2)

    main(token, weeks)
