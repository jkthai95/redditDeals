import pymysql
import Utils

class RedditDealStruct:
    def __init__(self, id='NA'):
        self.id = id

        # List of members
        self.__members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def acquire_members(self):
        """
        Return list of members inside struct.
        :return:  list of strings.
        """
        return self.__members

    def acquire_values(self):
        """
        Return list of values for each member inside struct.
        :return: list of strings
        """
        return [getattr(self, member) for member in self.__members]


class Database:
    def __init__(self):
        # Acquire login information from text file.
        login_info = Utils.get_login_info()
        self.username = login_info['username']
        self.password = login_info['password']

        # Create database if it does not exist
        self.__create_database()

        # Open database connection
        self.database = pymysql.connect(host='localhost',
                                        user=login_info['username'],
                                        passwd=login_info['password'],
                                        db='redditDealsDB')

        # Prepare cursor object
        self.cursor = self.database.cursor()

        # Columns within table
        self.columns = tuple(RedditDealStruct().acquire_members())

        # Create table of database
        self.__create_table()

    def __del__(self):
        # Close database connection
        self.database.close()

    def __create_database(self):
        # Open connection
        connection = pymysql.connect(host='localhost',
                                     user=self.username,
                                     passwd=self.password)
        # Prepare cursor object
        cursor = connection.cursor()

        # Create database if it does not exist
        sql = "CREATE DATABASE IF NOT EXISTS redditDealsDB"
        try:
            cursor.execute(sql)
        except:
            print("Could not create redditDealsDB. ")

        # Close connection
        connection.close()


    def __create_table(self):
        """
        Creates a table for mySQL database.
        """
        # TODO: Add code to maintain database. For now, we will create a new one each time.
        # Delete old table
        self.cursor.execute("DROP TABLE IF EXISTS DEALS")

        # Acquire columns
        columns = RedditDealStruct().acquire_members()

        # Create table
        sql = "CREATE TABLE DEALS ({} CHAR(255))".format(" CHAR(255) , ".join(columns))
        self.cursor.execute(sql)

    def insert_deal(self, reddit_deal):
        """
        Inserts reddit deal into mySQL database.
        :param reddit_deal: instance of RedditDealStruct()
        """
        sql = "INSERT INTO DEALS ({}) VALUES ({})".format(", ".join(self.columns), ", ".join(reddit_deal.acquire_values()))
        try:
            self.cursor.execute(sql)
            self.database.commit()
        except:
            # TODO: String values are too long. Modify code to save submission id instead, \
            #  and pull data based on submission id if necessary

            # Inserting data failed. Rollback.)
            self.database.rollback()

    def get_table(self):
        """
        Acquires entire table for database.
        :return: mySQL table.
        """
        sql = "SELECT * FROM DEALS"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            # Error when trying to fetch table
            print("Error: unable to fetch table. ")
            results = []
        return results




