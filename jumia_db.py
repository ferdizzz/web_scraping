import pymysql.cursors

connection = pymysql.connect( host = "localhost",
                              user = "root",
                              password = "",
                              db = "jumia",
                              charset = "utf8mb4",
                              cursorclass = pymysql.cursors.DictCursor)


def create_tables():
  with connection.cursor() as Cursor:
    create_smartphones = """CREATE TABLE IF NOT EXISTS smartphones_data(
                                ID INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                PhoneBrand VARCHAR(255),
                                Specification VARCHAR(255),
                                Oldprice BIGINT(10),
                                Newprice BIGINT(10),
                                Rating FLOAT(255, 2)
                                );
                              """
    Cursor.execute(create_smartphones)


def write_smartphones(phonebrand, specification, oldprice, newprice, rating):
  with connection.cursor() as Cursor:
    add_smartphones = f"INSERT INTO smartphones_data (PhoneBrand, Specification, Oldprice, Newprice, Rating) VALUES('{phonebrand}', '{specification}', {oldprice}, {newprice}, {rating})"

    Cursor.execute(add_smartphones)
    connection.commit()

# create_tables()