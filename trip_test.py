import unittest
from trip import *

class TestDatabase(unittest.TestCase):
    def test_activities_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Location FROM Activities'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Montgomery',), result_list)
        self.assertEqual(len(result_list), 150)

        sql = '''
            SELECT State, Attraction, Location, URL
            FROM Activities
            WHERE Location="La Jolla"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0][0], 5)

        conn.close()

    def test_activityinfo_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Title
            FROM ActivityInfo
            WHERE Type="Historic Sites"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('The Gateway Arch',), result_list)
        self.assertEqual(len(result_list), 6)

        sql = '''
            SELECT COUNT(*)
            FROM ActivityInfo
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 150)

        conn.close()

    def test_states_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT StateName
            FROM States
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Florida',), result_list)
        self.assertEqual(len(result_list), 50)

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT NumReviews
            FROM ActivityInfo
            JOIN Activities
            ON Title = Attraction
            JOIN States
            ON State = States.Id
            WHERE StateName="Florida"
                AND Location="Key West"
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, "9,789")
        conn.close()

unittest.main()
