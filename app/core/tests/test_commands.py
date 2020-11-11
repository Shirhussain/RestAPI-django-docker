from unittest.mock import  patch 

from django.core.management import  call_command
from django.db.utils import  OperationalError
from django.test import  TestCase

"""
Mocking:
    mocking is when you change the behavior of dependencies of the code that you tested.
    We use mocking to avoid any unintended side effects and also to isolate to specific peace of code 
    you wanna test. 
    i.e: imagine that you wanna test a function that send an email.
    remember that never write a test that depend on external services. because you can't grantee that 
    service will be available at the point that you gonna run the tested.
    you can use mocking to avoide sending an actual email. 
    it's avoid sending email just check that email function is working correctly 
"""

class CommandTests(TestCase):
    """Sometime it happend in Docker that django try to connect to db but it can't at the first place 
    to avoid some errors we have to  wait and try again after some seconds
    """ 

    def test_wait_for_db_reply(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi: 
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError]*5+[True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

