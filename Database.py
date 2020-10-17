import pymysql

class RedditDealStruct:
    def __init__(self, title='NA', reddit_link='NA'):
        self.title = title
        self.reddit_link = reddit_link

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
        # TODO: Acquire data from GUI
        # For now, we acquire necessary data from a file.
        with open('./redditLogin', 'r') as fp:
            client_id = fp.readline().strip()
            client_secret = fp.readline().strip()
            user_agent = fp.readline().strip()
            username = fp.readline().strip()
            password = fp.readline().strip()

        # Create database if it does not exist
        self.__create_database()

        # Open database connection
        self.database = pymysql.connect(host='localhost',
                                        user=username,
                                        passwd=password,
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

        # TODO: Acquire data from GUI
        # For now, we acquire necessary data from a file.
        with open('./redditLogin', 'r') as fp:
            client_id = fp.readline().strip()
            client_secret = fp.readline().strip()
            user_agent = fp.readline().strip()
            username = fp.readline().strip()
            password = fp.readline().strip()

        # Open connection
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     passwd=password)
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
        sql = "INSERT INTO DEALS ({}) VALUES {}".format(", ".join(self.columns), tuple(reddit_deal.acquire_values()))
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




