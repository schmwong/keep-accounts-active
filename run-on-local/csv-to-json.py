"""
Run this script in your local machine.

Please ensure your source file is in this
comma-delimited format before continuing:

,,USR,PWD
1,user@example.com,password1
2,user2@example.com,password2
3,abc@xyz.com,password3

Output:
A text file containing a single JSON string in the format
{"user@example.com": "password1", "user2@example.com": "password2", "abc@xyz.com": "password3"}
"""


import json
from csv import DictReader

# Change these to match your source and destination filenames
source_file = "MEGA.csv"
dest_file = "MEGA.txt"


cred_dict = {}
with open(source_file, mode="r") as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        cred_dict[(row["USR"]).strip()] = row["PWD"].strip()


cred_str = json.dumps(cred_dict)


with open(dest_file, "w") as text_file:
    text_file.write(cred_str)

print(
    f"""
Written to {dest_file}:

{cred_str}
"""
)
