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
    document = {'project_id': project_id,
                'project_name': project_name,
                'project_desc': project_desc,
                'hardware': {}}
    projects.insert_one(document)
    client.close()
    return True
    #TODO
    #Project database has fields for project ID, project name, project description,
    #and hardware names/quantities currently checked out to that project.

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
