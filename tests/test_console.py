#!/usr/bin/python3
"""Module for testing file storage"""
import unittest
import os
from io import StringIO
from console import HBNBCommand
from models import storage
from unittest.mock import patch

class TestConsole(unittest.TestCase):
    def test_do_create(self):
        """Test the do_create command"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            HBNBCommand().onecmd('create BaseModel')
            obj_id = fake_out.getvalue().strip()

        # Check if the object was created and saved
        obj = storage.get('BaseModel', obj_id)
        self.assertIsNotNone(obj)

if __name__ == '__main__':
    unittest.main()
