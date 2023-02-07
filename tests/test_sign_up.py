import unittest
from unittest import mock
from fastapi import HTTPException
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from Controllers.UserController import signUp



class TestSignUp(unittest.TestCase):
    def setUp(self):
        self.db_mock = mock.MagicMock()
        self.request = mock.MagicMock()
        self.request.email = "test@email.com"
        self.request.telephoneNumber = "1234567890"
        self.request.password = "test_password"
        self.request.roles = ["test_role"]
        self.request.name = "test_name"

    def test_signUp_success(self):
        self.db_mock.add.return_value = None

        response = signUp(self.request, self.db_mock)
        
        self.assertEqual(response, {"detail":"register succedded"})
        self.db_mock.add.assert_called_once()
        self.db_mock.commit.assert_called_once()

    def test_signUp_missing_field(self):
        self.request.email = None

        with self.assertRaises(HTTPException) as context:
            signUp(self.request, self.db_mock)
            
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.detail, "all firlds are required")

    def test_signUp_email_already_in_use(self):
        self.db_mock.add.side_effect = IntegrityError

        with self.assertRaises(HTTPException) as context:
            signUp(self.request, self.db_mock)
            
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "this email is used")

    def test_signUp_role_not_found(self):
        self.db_mock.commit.side_effect = FlushError

        with self.assertRaises(HTTPException) as context:
            signUp(self.request, self.db_mock)
            
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "role not found")