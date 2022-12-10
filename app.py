#!/bin/python3
""" A Flask endpoint that provides back-end services for https://guyyatsu.me/contacts.

Upon initial rendering the visitor is presented with two input fields;

    ```Name:```
       ~and~~~~~~>>which are both stored as lower_score string literals in the database.
       ~and~~~~~~>>get returned along with any POST requests.
    ```Email:```

When a POST request is caught its contents are selected for against the contacts.db file.

Any results are considered to be deliberate updates and the matches are deleted,
while a new line containing the updated results is committed to the table.
"""

#import argparse
import sqlite3

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session


""" INITIALIZE CONTACTS DATABASE """
# TODO: Add command-line argument for specifying a .db filepath.
ContactsDatabase = "/administrator/.contacts.db"
if len( sqlite3.connect(ContactsDatabase)\
               .cursor()\
               .execute( f"SELECT name "
                         f"FROM sqlite_master "
                         f"WHERE "
                         f"type='table' "
                         f"AND "
                         f"name='contacts';")\
               .fetchall()) == 0: sqlite3.connect(ContactsDatabase)\
                                         .cursor.execute( f"CREATE TABLE "
                                                          f"IF NOT EXISTS "
                                                          f"contacts ("
                                                            f"name "
                                                              f"TEXT "
                                                              f"NOT NULL"
                                                              f"PRIMARY KEY,"
                                                            f"email "
                                                              f"TEXT "
                                                              f"NOT NULL"
                                                          f")" ); connection.commit()


""" READ PUBKEY """
with open("/home/hunter/.ssh/id_ed25519.pub") as pubkeyFile:
  PublicKey = pubkeyFile.read()\
                        .strip()\
                        .split(" ")[1]


""" DEFINE FLASK INSTANCE """
app = Flask(__name__)
app.secret_key = str(PublicKey)
app.config['SESSION_TYPE'] = 'filesystem'


""" APP ROUTING """
@app.route("/", methods=["GET", "POST"])
def ContactForm():
  """
  """

  """ HANDLE [GET] METHOD """
  if request.method == "GET":

    """ SET DEFAULT NAME """
    if session.get("name") == None: name = "Firstname Lastname"
    """ USE SESSION NAME """
    else: name = session["name"].title().replace("_", " ")

    """ SET DEFAULT EMAIL """
    if session.get("email") == None: email = "YOUsername@YOUrdomain.mail"
    """ USE SESSION EMAIL """
    else: email = session["email"]

    # TODO: Utilize loopable custom input.
    # TODO: Implement input-masking.

    """ PREPARE VIEWPOINT """
    return render_template( "ContactForm.html",
                            title="Contact Form",
                            name=name,
                            email=email           )


  """ HANDLE [POST] METHOD """
  if request.method == "POST":

    """ CONNECT TO DATABASE """
    connection = sqlite3.connect(ContactsDatabase)
    cursor = connection.cursor()

    """ HANDLE REQUIRED ARGUMENTS """
    session["name"]= name= f"{request.form['ContactName'].lower().replace(' ', '_')}"
    session["email"]= email= f"{request.form['Email']}"

    """ HANDLE OPTIONAL ARGUMENTS """
    # TODO: Allow for a single custom input that
    #       adds to the updated review display.


    """ DATABASE LOOKUP """
    cursor.execute( f"SELECT * FROM contacts WHERE name=? OR email=?;",
                    (name, email)); _results = cursor.fetchall()

    """ DELETE MATCHES """
    if len(_results) > 0:
      cursor.execute(f"DELETE FROM contacts WHERE name=? OR email=?",
                     (name, email))

    """ (RE)WRITE TO TABLE """
    cursor.execute(f"INSERT INTO contacts (name,email) "
                       f"VALUES( ?, ? )", (name, email))

    """ TRANSACT UPDATE """
    connection.commit()
    return redirect("https://guyyatsu.me/contacts")


""" DEFINE RUNTIME """
if __name__ == "__main__":
  # TODO: Add command-line argument for host and port.
  app.run(host="0.0.0.0", port="65354")
