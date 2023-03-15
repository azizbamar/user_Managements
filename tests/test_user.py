from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
data = {
  "email": "oussemaa7s82@gamil.com",
  "name": "oussema",
  "phoneNumber": "+21650993586",
  "role": "admin",
  "authorization": True
}

#TEST SIGN UP
# def test_signUp():
#     response = client.post('/user_sign_up', json=data)
#     assert response.status_code == 200
#     assert response.json() == {"detail":"register succedded"}

# def test_reSignUp():
#     response = client.post('/user_sign_up', json=data)
#     assert response.status_code == 401
#     assert response.json() == {"detail":"email already in use"}

# def test_SignUpwithInexistantRole():
#     response = client.post('/user_sign_up', json= {
#   "email": "oussemaa782@gamil.com",
#   "name": "oussema",
#   "phoneNumber": "+21628526362",
#   "role": "",
#   "authorization": True
# })
#     assert response.status_code == 404
#     assert response.json() == {"detail":"role not found"}
#TEST SIGN IN 
# data = {
#     "email" : "azizbamar16@gmail.com",
#     "password" : "XeoBOEObRsHusv3b"
# }
# def test_signIn():
#     response = client.post('/user_sign_in',json=data)
#     assert response.status_code == 200

# def test_wrongSignIn():
#     response = client.post('/user_sign_in' , json = {
#         "email" : "aaa@hotmail.fr",
#         "password" : "aaaa"
#     })
#     assert response.status_code == 401
#     assert response.json() == {"detail" : "wrong email or password"}

#TEST TOKEN SIGN IN 
# def test_checkValidAccessToken():
#     #GET VALID TOKEN FROM DATABASE "tokens"
#     token ="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImF6aXpiYW1hcjE2QGdtYWlsLmNvbSIsImV4cCI6MTY3ODc4NjYxOC42MjEyMzU0fQ.lOm08_m36hWtkfQtEMODqPgfUAFyLXILG2xV5CyQOv_ZoQNYREEMS4fF7d5xXIujKHaLxkhqq0z1nPPJ5hyUkA"
#     response = client.post('/token_sign_in', headers={"token": token})
#     assert response.status_code == 200

# def test_checkInvalidAccessToken():
#     token ="aaaa"
#     response = client.post('/token_sign_in', headers={"token": token})
#     assert response.status_code == 401

# token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImF6aXpiYW1hcjE2QGdtYWlsLmNvbSIsImV4cCI6MTY3ODc4NjQxOS4yMzk0Mzg4fQ.g8Si3Uht62BP2ivep9vaczi7EtQ2uRD-fyU2OqGfDaEzisi_RJUf4VK44gIpIxjVyq84w69HJ6PHDKwHZCbRDA"
# def test_checkAccessToken():
#     response = client.post('/token_sign_in', headers={"token": token})
#     assert response.status_code == 401
#     assert response.json() == {"detail":"unauthorized"}

# def test_checkTokenSessionExpired():
#     #GET  TOKEN FROM DATABASE "tokens"
#     token="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImF6aXpiYW1hcjE2QGdtYWlsLmNvbSIsImV4cCI6MTY3ODcwMTYyNC43NjE2MzA4fQ.IJQvd_8C_4ir7BM7cL1_eEkzqzqByBXO72_Blrd_e1kvx7r3zL_5K8zU31rKVIO0Kby1PEtKO3TMyRH6Vt8IcA"
#     response = client.post('/token_sign_in',headers={"token": token})
#     assert response.status_code == 403
#     assert response.json() == {"detail":"session expired"}

#TEST PHONE SIGN IN
# data = {
#     "email" : "azizbamar16@gmail.com",
#     "password" : "XeoBOEObRsHusv3b",
#   "rememberME": True,
#   "phone": {
#     "uid": "string",
#     "model": "string",
#     "osVersion": "string"
#   }
# }
# def test_InvalidSignInFromPhone():
#     response = client.post('/user_sign_in_from_phone',json ={
#     "email" : "aaa@hotmail.com",
#     "password" : "XeoBOEObRsHusv3b",
#   "rememberME": True,
#   "phone": {
#     "uid": "string",
#     "model": "string",
#     "osVersion": "string"
#   }
# })
#     assert response.status_code == 401
#     assert response.json() == {"detail":"wrong email or password"}


# def test_signInFromPhone():
#     response = client.post('/user_sign_in_from_phone',json =data )
#     assert response.status_code == 200

# def test_SignInFromOtherPhone():
#     data = {
#     "email" : "azizbamar16@gmail.com",
#     "password" : "XeoBOEObRsHusv3b",
#   "rememberME": True,
#   "phone": {
#     "uid": "string2",
#     "model": "string",
#     "osVersion": "string"
#   }
# }
#     response = client.post('/user_sign_in_from_phone',json =data )
#     assert response.status_code == 403
#     assert response.json() == {"detail":"Forbidden"}




#TEST SIGN OUT
# def test_signOut():
#     #GET VAILD TOKEN FROM DATABASE
#     token = ""
#     response = client.post('/user_sign_out',headers={"token" : token})
#     assert response.status_code == 200
#     assert response.json() == {"detail" : "sign out successful"}

# def test_signOutInvalidToken():
#     token = "aaaa"
#     response = client.post('/user_sign_out',headers={"token" : token})
#     assert response.status_code == 404
#     assert response.json() == {"detail" : "token not found"}

#TEST SIGN OUT FROM PHONE

# def test_signOutFromPhone():
#     token ="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImF6aXpiYW1hcjE2QGdtYWlsLmNvbSIsImV4cCI6MTY4Mzg4Nzc4Mi4yMjQwNjN9.KLftYAxpyezSzLfe4YnnhIPUlky3TWYXI4jBJcjmtbWhi1IkxWZY1wGB_hUdUJrgOvi2sEq2C27QJEoTsHx46Q"
#     response = client.post('/user_sign_out_from_phone',headers={"token" : token} )
#     assert response.status_code == 200
#     assert response.json() == {"detail":"sign out succedded"}  

# def test_signOutFromPhoneInvalidToken():
#     token ="test"
#     response = client.post('/user_sign_out_from_phone',headers={"token" : token} )
#     assert response.status_code == 404
#     assert response.json() == {"detail":"token not found"}   

# def test_removePhoneForUser():
#     response = client.post('/removePhone/2')
#     assert response.status_code == 200
#     assert response.json() == {"detail":"Phone deleted"}

# def test_removePhoneForUserWithoutPhone():
#     response = client.post('/removePhone/2')
#     assert response.status_code == 401
#     assert response.json() == {"detail":"User has not a phone"}

# def test_removePhoneForInexistantUser():
#     response = client.post('/removePhone/-5')
#     assert response.status_code == 401
#     assert response.json() == {"detail":"User not found"}   


# def test_getUsersByName():
#     response = client.get('/users/123')
#     assert response.status_code == 200

# def test_deleteUser():
# GET AN ID FROM DATABASE
#       response = client.delete('/deleteUser/2')
#       assert response.status_code == 200
#       assert response.json() == {"detail":"User deleted"}   
# def test_deleteInexistantUser():
#       response = client.delete('/deleteUser/2')
#       assert response.status_code == 401
#       assert response.json() == {"detail":"User not found"}  


