"""
Tool for extracting summary data from "Details" tab of SARAO archive,
for LADUMA/MeerKAT tracks.

Zack Hutchens
March 2021
"""


def extractinfo(details):
    print(details)

if __name__=='__main__':
    # query user to paste "Details" tab
    text = input("Paste information from the 'details' tab:")
    extractinfo(text)
