from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

with open("/home/hunter/.ssh/id_ed25519.pub") as pubkeyFile:
  KeyHeaders = pubkeyFile.read()\
                         .split(" ")

PublicKey = KeyHeaders[1]

# Set sqlite3 constants.
ContactsDatabase = "/administrator/.contacts.db"
connection = sqlite3.connect(ContactsDatabase)
cursor = connection.cursor()

# Create the contacts table if it doesn't alread exist.
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts';")
if len(cursor.fetchall()) == 0:
  cursor.execute(f"CREATE TABLE contacts ("
                 f"name TEXT PRIMARY KEY NOT NULL,"
                 f"email TEXT NOT NULL,"
                 f"number TEXT,"
                 f"company TEXT"
                 f"website TEXT)")
  connection.commit()


# Initialize the flask instance.
app = Flask(__name__)
app.secret_key = str(PublicKey)
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/", methods=["GET", "POST"])
def ContactForm():

  # Set sqlite3 constants.
  ContactsDatabase = "/administrator/.contacts.db"
  connection = sqlite3.connect(ContactsDatabase)
  cursor = connection.cursor()


  if request.method == "GET":

    """ Check for existing session variables. """
    # This allows the user to review their
    # submission after they've already entered it.
    if session.get("name") == None: name= None
    else: name= session["name"].title().replace("_", " ")
    namePlaceholer = "Firstname Lastname"

    if session.get("email") == None: email= None
    else: email= session["email"]
    emailPlaceholder = "YOUsername@YOURDOMAIN.mail"

    if session.get("number") == None: number= None
    else: number= session["number"]
    numberPlaceholder = "123-456-7899"

    if session.get("company") == None: company= None
    else: company= session["company"].title().replace("_", " ")
    companyPlaceholder = "Business Factory ltd"

    if session.get("website") == None: website= None
    else: website= session["website"]
    companyPlaceholder = "https://yourdomain.ltd"


    """ Retrieve form data and write to database."""
    return render_template("ContactForm.html",
                           title="Contact Form",
                           name=name,
                           email=email,
                           number=number,
                           company=company,
                           website=website)


  if request.method == "POST":



    """ Format and set the users input."""
  
    # Name.
    session["name"]= name= f"{request.form['ContactName'].lower().replace(' ', '_')}"
    #session["name"] = name


    # Email.
    session["email"]= email= f"{request.form['Email']}"
    #session["email"] = email


    # Phone Number.
    if request.form["PreferredPhone"]:
      session["number"]= number= f"{request.form['PreferredPhone'].replace(' ', '-')}"
      print(session["number"])
      #session["number"] = number


    # Company.
    if request.form["Company"]:
      session["company"]= company= f"{request.form['Company'].lower().replace(' ', '_')}"
      #session["company"] = company


    # Website.
    if request.form["Website"]:
      session["website"]= website= f"{request.form['Website']}"
      #session["website"] = website



    """ Write or update entry. """
    # When an entry is made the page is refreshed and the previously
    # given information is displayed so that the user has the option
    # to review their input and change it as necessary.
    #
    # In an effort to prevent us from having to choose between
    # required keys, we'll simply delete any rows matching
    # any of the keys.

    # Select either the name or the email.
    cursor.execute(
      f"SELECT * FROM contacts WHERE name=? OR email=?;",
      (name, email)); _results = cursor.fetchall()

    # If a match is found, delete the entry and rewrite it.
    if len(_results) > 0:
      cursor.execute(f"DELETE FROM contacts WHERE name=? OR email=?",
                     (name, email))

    # Write a new row with the required name and email.
    cursor.execute(f"INSERT INTO contacts (name,email) "
                       f"VALUES( ?, ? )", (name, email))


    """ Write optional fields to the database row. """
    # These options are nice to have, but not required
    # input.
    #
    # To check for a variables existence we use the
    # built-in .locals against every optional field.
    #
    # If any matches are found, apply the appropriate
    # SQLite transaction.

    if "number" in locals():# Add the number, if given.
      cursor.execute(f"UPDATE contacts SET number = ? "
                     f"WHERE name=? OR email=?;",
                     (number, name, email)); del number


    if "company" in locals():# Add the company, if given.
      cursor.execute(f"UPDATE contacts SET company = ? "
                     f"WHERE name=? OR email=?;",
                     (company, name, email)); del company


    if "website" in locals():# Add the website, if given.
      cursor.execute(f"UPDATE contacts SET company = ? "
                     f"WHERE name=? OR email=?;",
                     (website, name, email)); del website


    # Save your work.
    connection.commit()

    return redirect("https://guyyatsu.me/contacts")


@app.route("/success")
def FormSuccess():
  """ Inform the user of a successful transaction. """

  # Let the user know the UPDATE was successful.
  if session["update"]:
    return render_template("FormSuccess.html",
      title="Success!",
      InputType="Contact information updated successfully.")

  # Let the user know they successfully ADDED themselves.
  else:
    return render_template("FormSuccess.html",
      title="Success!",
      InputType="Contact information successfully added.")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="65354")
