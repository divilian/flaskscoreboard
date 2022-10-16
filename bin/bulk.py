
import sqlite3
import sys
import pandas as pd
import os

if len(sys.argv) != 4:
    sys.exit("Usage: bulk.py nameOfDatabase.sqlite nameOfCsvFile.csv tag.")
dbfile = sys.argv[1]
filename = sys.argv[2]
tag = sys.argv[3]
if not os.path.exists(dbfile):
    sys.exit(f"No such file {dbfile}.")
if not os.path.exists(filename):
    sys.exit(f"No such file {filename}.")

conn = sqlite3.connect(dbfile)

scores = pd.read_csv(filename)

def charNameFor(conn, realname):
    matches = [ m for m in conn.execute(f"""
        select charname from chars
        where lower(realname) like '%{realname}%'
    """)]
    if len(matches) == 1:
        return matches[0][0]
    else:
        sys.exit(f"\nSorry, {len(matches)} matches for '{p}'.\n")

conn.execute("begin")

for row in scores.itertuples():
    conn.execute("""
        insert into xp (username,xps,tag) values (?,?,?)
        """, (charNameFor(conn, row[1]), int(row[2]), tag))
    print(f"Entered {row[2]} points for {row[1]}.")
conn.execute("commit")
