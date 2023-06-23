from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "banan"


# Working
class jsondata():
    namelist = "Names.json"
    tasklist = "Tasks.json"

    # Working
    def adminExists():
        with open(jsondata.namelist, "r") as file:
            data = json.load(file)
        for person in data.values():
            if person.get("Admin", False):
                return True
        return False

    # Working
    def randid():
        playerids = []

        ID = random.randint(1000, 9999)
        while ID in playerids:
            ID = random.randint(1000, 9999)
        playerids.append(ID)

        return ID

    # Working
    def addperson(name, age, gender, admin):
        filename = "Names.json"

        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r") as file:
                data = json.load(file)
        else:
            data = {}

        if admin and jsondata.adminExists():
            raise Exception("Es existiert bereits ein Admin")

        friend = False
        person_id = "Person" + str(len(data) + 1)
        person_data = {
            "ID": jsondata.randid(),
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Admin": admin,
            "friend": friend
        }
        data[person_id] = person_data

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        return person_data["ID"]

# Working
def createLists():
    namelist = "Names.json"
    tasklist = "Tasks.json"
    data = {}
    if not os.path.exists(namelist):
        with open(namelist, "w") as file:
            json.dump(data, file)

    if not os.path.exists(tasklist):
        with open(tasklist, "w") as file:
            json.dump(data, file)
createLists()


# Working
def verifyLogin(name, id):
    filename = "Names.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for person in data.values():
                if person.get("Name") == name and str(person.get("ID")) == id:
                    session["admin"] = person.get("Admin", False)  # Store the admin status in the session
                    return True
    return False

# Working
@app.route("/")  # Starseite
def starscreen():
    return render_template("startscreen.html")


# Working
@app.route("/overview") #Dient der übersichtlichkeit, jenachdem welchen Status du hast
def overview():
    name = session.get("name")
    id = session.get("ID")

    if not name or not id:
        return redirect("/login")

    with open("Names.json", "r") as file:
        data = json.load(file)

    is_admin = False
    is_friend = False

    for person in data.values():
        if str(person.get("ID")) == id:
            if person.get("Name") == name:
                is_admin = person.get("Admin")
                is_friend = person.get("friend")
                break

    return render_template("overview.html", is_admin=is_admin, is_friend=is_friend)


# Working (Except for Time remaining)
@app.route("/addtask", methods=["GET", "POST"])  # Fügt eine Aufgabe hinzu
def addtask():
    if request.method == "POST":
        task = request.form["task"]
        description = request.form["description"]
        deadline = request.form["deadline"]
        filename = "Tasks.json"

        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r") as file:
                data = json.load(file)
        else:
            data = {}

        task_id = "Aufgabe" + str(len(data) + 1)

        created_at = datetime.strptime(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")
        deadline_at = datetime.strptime(deadline, "%Y/%m/%d")
        remaining = deadline_at - created_at
        task_data = {
            "Aufgabe": task,
            "Beschreibung": description,
            "Erledigen bis": deadline,
            "Erstellt": created_at.strftime("%m/%d/%Y %H:%M"),
            "Verbleibende Zeit": f"{remaining.days} Tage"
        }
        data[task_id] = task_data

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        return redirect("/overview")
    return render_template("addtask.html")

#Working
@app.route("/deltask", methods=["POST", "GET"])
def deltask():
    if request.method == "POST":
        filename = "Tasks.json"
        taskName = request.form.get("taskName")

        with open(filename, "r") as file:
            data = json.load(file)

        if taskName in data:
            del data[taskName]

            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

            return "Die Aufgabe wurde erfolgreich gelöscht"
        else:
            return "Die Aufgabe wurde nicht gefunden"
    return render_template("deltask.html")

#Working
@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        filename = "Tasks.json"

        taskName = request.form.get("task_name")
        taskValue = request.form.get("task_value")
        newValue = request.form.get("new_value")

        with open(filename, "r") as file:
            data = json.load(file)

        if task_name in data:
            task = data[taskName]
            if taskValue in task:
                task[taskValuealue] = newValue

                with open(filename, "w") as file:
                    json.dump(data, file, indent=4)

                return "Die Aufgabe wurde erfolgreich aktualisiert"
            else:
                return "Die angegebene Eigenschaft existiert nicht"
        else:
            return "Die Aufgabe wurde nicht gefunden"

    return render_template("edit.html")

#Working
@app.route("/removefriend", methods = ["GET", "POST"]) #Entfernt einen Freund
def removefriend():
    if request.method == "POST":
        filename = "Names.json"
        name = request.form.get("name")
        login_id = request.form.get("login_id")

        with open(filename, "r") as file:
            data = json.load(file)

        for key, value in data.items():
            if "ID" in value and value["ID"] == int(login_id):
                if "Name" in value and value["Name"] == name:
                    value["friend"] = False

                    with open(filename, "w") as file:
                      json.dump(data, file, indent=4)

                    return redirect("/overview")
        return "Der Name oder die ID sind ungültig"
    return render_template("removefriend.html")

#Working
@app.route("/addfriend", methods = ["GET", "POST"])  # Fügt einen Freund hinzu (Freunde können eigene Listen selbst bearbeiten)
def addfriend():
    if request.method == "POST":
        filename = "Names.json"
        name = request.form.get("name")
        login_id = request.form.get("login_id")

        with open(filename, "r") as file:
            data = json.load(file)

        for key, value in data.items():
            if "ID" in value and value["ID"] == int(login_id):
                if "Name" in value and value["Name"] == name:
                    value["friend"] = True

                    with open(filename, "w") as file:
                      json.dump(data, file, indent=4)

                    return redirect("/overview")
        return "Der Name oder die ID sind ungültig"
    return render_template("addfriend.html")

# Working
@app.route("/register", methods=["GET", "POST"])  # Erstellt einen Account mit Name und Passwort
def register():
    if request.method == "POST":
        firstname = request.form["firstname"]
        age = request.form["age"]
        gender = request.form["gender"]
        admin = request.form.get("admin") == "True"

        id = jsondata.addperson(firstname, age, gender, admin)

        return f"Du hast dich erfolgreich registriert, deine Login ID lautet {id}, diese ist später wichtig um die anzumelden"
    return render_template("register.html")


# Working
@app.route("/login", methods=["GET", "POST"])  # Loggt dich in deinem Account ein
def login():
    if request.method == "POST":
        name = request.form["loginname"]
        id = request.form["loginid"]

        if verifyLogin(name, id):
            session["name"] = name
            session["ID"] = id
            return redirect("/overview")
        else:
            return "Der Name oder deine ID sind ungültig"

    return render_template("login.html")

#Working
@app.route("/view")  # sieht alle Aufgabe aller deiner Freunde ein
def view():
    filename = "Tasks.json"
    with open(filename, "r") as file:
        data = json.load(file)

    return render_template("view.html", data=data)

#Working
@app.route("/friends")  # Gibt alle deine Freunde aus
def friends():
    filename = "Names.json"

    with open(filename, "r") as file:
        data = json.load(file)

    friends = []
    for person, info in data.items():
        if "friend" in info and info["friend"]:
            name = info["Name"]
            id = info["ID"]
            friends.append({"Name": name, "ID": id})

    return render_template("friends.html", friends=friends)

# oder flask --app .\main.py run im Terminal eingeben
if __name__ == "__main__":
    app.run(debug=False)