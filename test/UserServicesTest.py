import unittest, os
from users.UserServices import User, UserManager

class TestUser(unittest.TestCase):

    def test_userconstructor(self):
        u = User()
        self.assertEqual(u.description, u"")
        self.assertEqual(u.nickName, u"")
        self.assertEqual(u.email, u"")

    def test_getallusers(self):
        os.environ['OPENSHIFT_MONGODB_DB_URL']=u"mongodb://mmxvi:eurommxvi@127.0.0.1:27017/euroxxxvi"
        mgr = UserManager()
        self.assertIsNotNone(mgr.getDb())

        users = mgr.getAllUsers()
        for u in users:
            print(u)
        self.assertIsNotNone(users)

    def test_getsaveuser(self):
        os.environ['OPENSHIFT_MONGODB_DB_URL']=u"mongodb://mmxvi:eurommxvi@127.0.0.1:27017/euroxxxvi"
        mgr = UserManager()

        usera = mgr.saveUser("email@test.fr", "", "", "uuidxxx", False, u"zoo")
        self.assertIsNotNone(usera)

        user = mgr.getUserByEmail(u"email@test.fr")


        self.assertIsNotNone(user)

        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.user_id)

if __name__ == '__main__':
    unittest.main()
