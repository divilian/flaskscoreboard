
import sqlite3
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: enter.py nameOfXpFile.sqlite.")

conn = sqlite3.connect(sys.argv[1])

# Return a tuple with the character name and real name of the one and only
# match the user specifies, re-asking until there is exactly one match. Returns
# "done","done" if the user types "done".
def prompt(conn):
    while True:
        p = input("Partial name for student (or done): ")
        if p == "done":
            return "done","done"
        matches = [ m for m in conn.execute(f"""
            select charname,realname from chars
            where lower(realname) like '%{p}%'
        """)]
        if len(matches) == 1:
            return matches[0][0], matches[0][1]
        else:
            print(f"Sorry, {len(matches)} matches for '{p}'.")



tag = input("Enter tag (for all students): ")
charname, realname = prompt(conn)
while charname != "done":
    pts = int(input(f"XP for {realname}: "))
    conn.execute("""
        insert into xp (username, xps, tag) values
        (?,?,?)
        """, (charname, pts, tag))
    conn.commit()
    print(f"...supposedly entered {pts} points for {charname}...")
    charname, realname = prompt(conn)
