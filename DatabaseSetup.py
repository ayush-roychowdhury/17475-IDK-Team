# Adds new user to the user set within the database. Returns True if the user
# was successfully added and False if there already exists a user with the
# specified username in the user set.
def createNewUser(username, userid, password):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Users
    people = db.UserSet    
    exists = people.find_one({'username': username})
    if exists != None:
        return False
    document = {'userid': userid,
                'username': username,
                'password': password,
                'projects': []}
    people.insert_one(document)
    client.close()
    return True

# Returns the list of project names associated with the provided username if
# login is successful. If login is unsuccessful (i.e. password was wrong),
# returns False
def login(username, userid, password):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Users
    people = db.UserSet
    person = people.find_one({'username': username,
                              'userid': userid,
                              'password': password})
    if person == None:
        return False
    else:
        return person['projects']

# Adds new project to the specified user. Returns True if successful and False
# if a project with that name already exists.
def createProject(username, project_id, project_name, project_desc):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Projects
    projects = db[username]    
    exists = projects.find_one({'project_name': project_name})
    if exists != None:
        return False
    #Project database has fields for project ID, project name, project description,
    #and hardware names/quantities currently checked out to that project.
    document = {'project_id': project_id,
                'project_name': project_name,
                'project_desc': project_desc,
                'hardware': {}}
    projects.insert_one(document)
    client.close()
    return True

# Returns dict of hardware currently checked out if given project exists, False otherwise.
# Prereq: username is a valid user.
def selectProject(username, project_name):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Projects
    projects = db[username]
    project = projects.find_one({'project_name': project_name})
    if project == None:
        return False
    else:
        return project['hardware']

# TODO: Add similar methods for hardware database.
# Hardware has name, capacity, availability, and possibly other fields.

# Adds a piece of hardware to the database. Mostly for debugging and administrative
# uses for now. Note that a negative amt can be used to remove hardware from the database.
def addHardware(hw_name, amt):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Hardware
    hw_set = db.HW_Set
    hw = hw_set.find_one({'name': hw_name})
    if hw == None:
        document = {'name': hw_name,
                    'capacity': amt,
                    'availability': amt}
        hw_set.insert_one(document)
    else:
        if amt < 0:
            removal_amt = -amt if -amt <= hw['availability'] else hw['availability']
            hw['availability'] -= removal_amt
            hw['capacity'] -= removal_amt
        else:
            hw['availability'] += amt
            hw['capacity'] += amt

# Checks out specified hardware amount from the specified project
# Returns: 2, if the project doesn't exist with the specified username.
#          1, if there is not enough capacity to check out all of the
#             requested hardware. In this case, the remaining capacity
#             is checked out, which is less than the requested amount.
#          0, if all of the requested hardware is successfully checked
#             out.
def check_out(hw_name, amt, project_name, username):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Projects
    projects = db[username]
    project = projects.find_one({'project_name': project_name})
    if project == None:
        return 2
    
    db = client.Hardware
    hw_set = db.HW_Set
    hw = hw_set.find_one({'name': hw_name})
    if hw['availability'] < amt:
        #TODO
        return 1
    else:
        #TODO
        return 0
    
