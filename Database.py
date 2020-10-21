import pymysql
import Utils

maximum_string_size = 255

class RedditDealStruct:
    def __init__(self, id='NA', title='NA', permalink='NA', deal=0):
        # Note: These parameters follow praw.Reddit.submission() syntax
        self.id = id                # Submission ID
        self.title = title          # Title of submission
        self.permalink = permalink  # Link to reddit submission
        self.deal = deal            # Best deal from submission (Percent off)

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
        temp_reddit_struct = RedditDealStruct()
        members = temp_reddit_struct.acquire_members()
        columns = []
        for member in members:
            # Acquire data of member
            data = getattr(temp_reddit_struct, member)

            # Define column name and type
            # Note: We can add additional types here.
            if isinstance(data, int):
                columns.append(str(member) + ' int')
            elif isinstance(data, str):
                columns.append(str(member) + ' CHAR({})'.format(maximum_string_size))

        # Create table
        sql = "CREATE TABLE DEALS ({})".format(", ".join(columns))

        self.cursor.execute(sql)

    def insert_deal(self, reddit_deal):
        """
        Inserts reddit deal into mySQL database.
        :param reddit_deal: instance of RedditDealStruct()
        """
        # Convert values to string
        str_values = []
        for value in reddit_deal.acquire_values():
            if isinstance(value, str) and len(value) > maximum_string_size:
                # If string is too long, place 'NA' in table instead.
                value = '\'NA\''

            str_values.append(str(value))

        sql = "INSERT INTO DEALS ({}) VALUES ({})".format(", ".join(self.columns), ", ".join(str_values))
        try:
            self.cursor.execute(sql)
            self.database.commit()
        except Exception as e:
            # TODO: String values are too long. Modify code to save submission id instead, \
            #  and pull data based on submission id if necessary
            print(e)

            # Inserting data failed. Rollback.)
            self.database.rollback()

    def get_table(self):
        """
        Acquires entire table for database.
        :return: mySQL table, list of field names
        """
        sql = "SELECT * FROM DEALS"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            field_names = [i[0] for i in self.cursor.description]
        except:
            # Error when trying to fetch table
            print("Error: unable to fetch table. ")
            results = []
        return results, field_names




