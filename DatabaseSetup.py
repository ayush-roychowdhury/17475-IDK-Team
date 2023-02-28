# Adds new user to the user set within the database. Returns True if the user
# was successfully added and False if there already exists a user with the
# specified username in the user set.
def addNewUser(username, userid, password):
    from pymongo import MongoClient
    client = pymongo.MongoClient("mongodb+srv://rickhanish:ECE461LPassword@cluster0.e0ejs3p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Users
    people = db.UserSet    
    exists = people.find_one({'username': username})
    if exists != None:
        return False
    document = {'userid': ObjectID(userid),
                'username': username,
                'password': password}
    people.insert_one(document)
    client.close()
    return True
