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

class TestPlotlyGraphs(unittest.TestCase):

    def test_rankings(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement1 = '''
        SELECT Count(*)
        FROM ActivityInfo
        WHERE Rating =1'''

        results = cur.execute(statement1)
        count = results.fetchone()[0]
        self.assertEqual(count, 118)

        statement2 = '''
        SELECT Count(*)
        FROM ActivityInfo
        WHERE Rating =2'''

        results = cur.execute(statement2)
        count = results.fetchone()[0]
        self.assertEqual(count, 21)

        statement3 = '''
        SELECT Count(*)
        FROM ActivityInfo
        WHERE Rating =3'''

        results = cur.execute(statement3)
        count = results.fetchone()[0]
        self.assertEqual(count, 11)

        conn.close()

    def test_reviews(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
        SELECT StateName, NumReviews
        FROM ActivityInfo
        JOIN Activities
        ON Title = Attraction
        JOIN States
        ON State = States.Id
        GROUP BY StateName
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Florida', '10,261'), result_list)
        self.assertEqual(len(result_list), 50)

        conn.close()


    def test_type(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
        SELECT Type, COUNT(*)
        FROM ActivityInfo
        GROUP BY Type
        ORDER BY COUNT(*) DESC
        '''

        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Specialty Museums', 15), result_list)
        self.assertEqual(len(result_list), 51)

        conn.close()

    def test_activities(self):
        results = get_activities("Michigan")
        l = []
        for r in results:
            l.append(r)

        self.assertEqual(str(l[0]), 'Gilmore Car Museum in Hickory Corners')
        self.assertEqual(str(l[1]), 'Detroit Institute of Arts in Detroit')
        self.assertEqual(str(l[2]), 'Pictured Rocks National Lakeshore in Munising')

unittest.main()
