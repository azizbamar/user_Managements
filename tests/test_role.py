from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
data = {
    "name" : "azizRole",
    "claims" : "test"
}
# def test_createRole():
#     response = client.post('/addRole',json = data)
#     assert response.status_code == 200
#     assert response.json() == {"detail":"register succedded"}

# def test_addExistingRoleName():
#     response = client.post('/addRole', json = data)
#     assert response.status_code == 404
#     assert response.json() == {"detail" :"claims id not found"}

# def test_getAllRoles():
#     response = client.get('/roles')
#     assert response.status_code == 200
    
# def test_updateRole():
#     response = client.put('/updateRole/26', json = {"name" : "test" , "claims" : "test claims"})
#     assert response.status_code == 200
#     assert response.json() == "role updated successfully"
# def test_updateInexistantRole():
#     response = client.put('updateRole/6',json = {"name" : "test" , "claims" : "test claims"})
#     assert response.status_code == 404
#     assert response.json() == {"detail" : "role not found"}


# def test_deleteRole():
#     response = client.delete('/deleteRole/26')
#     assert response.status_code == 200
#     assert response.json() == {"detail":"Role deleted"}

# def test_deleteInexistantRole():
#     response = client.delete('/deleteRole/-8')
#     assert response.status_code == 404
#     assert response.json() == {"detail" : "role not found"}

# def test_getUserRoles():
#     response = client.get('/userRole/1')
#     assert response.status_code == 200 
#     assert response.json() == "admin"

# def test_getInexistantUserRoles():
#     response = client.get('/userRole/-8')
#     assert response.status_code == 404 
#     assert response.json() == {"detail" : "user not found"}