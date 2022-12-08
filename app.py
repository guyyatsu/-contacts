from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Set sqlite3 constants.
ContactsDatabase = "./contacts.db"
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

@app.route("/", methods=["GET", "POST"])
def ContactForm():

  # Set sqlite3 constants.
  ContactsDatabase = "./contacts.db"
  connection = sqlite3.connect(ContactsDatabase)
  cursor = connection.cursor()


  if request.method == "GET":
    """ Retrieve form data and write to database."""
    return render_template("ContactForm.html", title="Contact Form")


  if request.method == "POST":

    post_type = "add"

    """ Format and set the users input."""
  
    # Add the last name to the first name.
    name = f"{request.form['FirstName'].lower()}_{request.form['LastName'].lower()}"

    # Email needs no formatting.
    email = f"{request.form['Email']}"

    # Replace spaces in number with dashes.
    if request.form["PreferredPhone"]:
      number = f"{request.form['PreferredPhone'].replace(' ', '-')}"

    # Company gets lowercased, because we dont respect them.
    if request.form["Company"]:
      company = f"{request.form['Company'].lower().replace(' ', '_')}"

    # Website also gets collected without formatting. 
    if request.form["Website"]:
      website = f"{request.form['Website']}"


    """ Check for existing contact in the database. """

    # Select either the name or the email.
    cursor.execute(f"SELECT * FROM contacts WHERE name=? OR email=?;",
                   (name, email))

    # If a match is found, continue to updating the row.
    if len(cursor.fetchall()) > 0:  post_type = "update"

    # Otherwise, populate a new row with the required information.
    else: cursor.execute(f"INSERT INTO contacts (name,email) "
                         f"VALUES( ?, ? )", (name, email))


    """ Update the non-required columns. """

    if "number" in locals():# Add the number, if given.
      cursor.execute(f"UPDATE contacts SET number = ? "
                     f"WHERE name=? OR email=?;",
                     (number, name, email))

    if "company" in locals():# Add the company, if given.
      cursor.execute(f"UPDATE contacts SET company = ? "
                     f"WHERE name=? OR email=?;",
                     (company, name, email))

    if "website" in locals():# Add the website, if given.
      cursor.execute(f"UPDATE contacts SET company = ? "
                     f"WHERE name=? OR email=?;",
                     (website, name, email))

    # Save your work.
    connection.commit()

    #return redirect(url_for("FormSuccess"))
    return redirect(url_for("FormSuccess", post_type=post_type))

@app.route("/<post_type>/success")
def FormSuccess(post_type):
  """ Inform the user of a successful transaction. """

  # Let the user know the UPDATE was successful.
  if post_type == "update":
    return render_template("FormSuccess.html",
      title="Success!",
      InputType="Contact information updated successfully.")

  # Let the user know they successfully ADDED themselves.
  else:
    return render_template("FormSuccess.html",
      title="Success!",
      InputType="Contact information successfully added.")