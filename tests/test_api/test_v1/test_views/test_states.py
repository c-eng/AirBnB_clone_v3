#!/usr/bin/python3
'''Test states view for expected behavior and documentation'''
import unittest
from flask import Flask
from api.v1.app import app, storage
from models.state import State


class TestStates(unittest.TestCase):
    '''Test class for states view'''

    @classmethod
    def setUpClass(cls):
        '''Set up flask'''
        from api.v1.app import app
        cls.app = app.test_client()
        '''
        cls.test_state = State(name="Test_State", id="7777777")
        cls.test_state.save()
        '''

    def test_get(self):
        '''Test GET on /states view'''
        result = type(self).app.get('/api/v1/states/')
        """
        print(result.data.decode(encoding='UTF-8'))
        """
        self.assertEqual(result.status_code, 200)
