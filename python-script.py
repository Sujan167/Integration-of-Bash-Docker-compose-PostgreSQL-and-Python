'''
This is the python script to have hands on json file and postgres database. Here is a sample data which is fetched and store in another filtered json file. Further it map the schema and insert bulk data into postgres database.
'''
import time
import os
import psycopg2
import json

# primary_file is the source file where all data is available.
# As data may be bulk and low spec RAM may not handle it thus a secondary file is used. clean data is stored in this file from where data can be directly inserted into database
primary_file = 'sampleData.json'
secondary_file = 'FilterData.json'
tableName = 'Test_Table'

# This is for database connection.
host = 'localhost'
port = '5432'
user = 'postgres'
password = 'postgres'
dbname = 'postgres'


def fetchData():
    '''
    This function fetch the required data from primary file and store in secondary file
    '''
    try:
        with open(primary_file) as f:
            content = json.load(f)

        data = content['data']
    except Exception as e:
        print(f"Error in opening {primary_file}!!!")
        return None

    wrapper = {}
    result = []
    try:
        for item in data:
            id = item['id']
            name = item['name']
            description = item['description']
            price = item['price']
            brandName = item['brandName']
            categoryName = item['categoryName']
            imageUrl = item['imageUrl']

            createrName = item['creatorInfo']['createdByName']
            contact = item['creatorInfo']['createdByUsername']

            latitude = item['location']['locationLatitude']
            longitude = item['location']['locationLongitude']
            locationDescription = item['location']['locationDescription']

            # filtered data is mapped into a dictionary of each item
            filterData = {
                'id': id,
                'name': name,
                'description': description,
                'price': price,
                'brandName': brandName,
                'categoryName': categoryName,
                'imageUrl': imageUrl,

                'createrName': createrName,
                'contact': contact,
                'latitude': latitude,
                'longitude': longitude,
                'locationDescription': locationDescription
            }
            # It creates a big list of all data which are in dictionary formate
            result.append(filterData)
    except Exception as e:
        print(f"Error in fetching from {primary_file}")
        return None

    wrapper['results'] = result
    # Finally fetched data is stored into secondary file
    with open(secondary_file, 'a') as f:
        f.write(json.dumps(result, indent=2))


def dataMapping():
    '''
    This function is for connection with postgres database. It first establish the connection with database and creates a table, map the data with the schema, read the fetched data from secondary file and upload bulk data into the database
    '''

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )

        # After inserting data, it needs to be commit the change in database thus autocommit=True means it automatically does commit
        conn.autocommit = True

        # create cursor object
        cur = conn.cursor()

        # execute a query for creating table
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {tableName}(
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(5000),
            price VARCHAR(255),
            brandName VARCHAR(255),
            categoryName VARCHAR(255),
            imageUrl VARCHAR(255),
            createrName VARCHAR(255),
            contact VARCHAR(255),
            latitude VARCHAR(255) ,
            longitude VARCHAR(255),
            locationDescription VARCHAR(255)
            )
        ''')

        # Schema
        sql = f"INSERT INTO {tableName} (id, name, description,price,brandName,categoryName,imageUrl,createrName,contact,latitude,longitude,locationDescription) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"

        # read fetched data and then ready to upload.
        with open(secondary_file) as f:
            content = json.load(f)

        final = []

        # NOTE: postgres needs a list of tuples. thus converting the data into a list of tuples

        for item in content:
            result = tuple(item.values())
            final.append(result)

        # Execute the query for inserting bulk data
        cur.executemany(sql, final)

    # close cursor and connection after the operation
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: ", error)
        # If the operation is not completed then rollback database state into previous state
        conn.rollback()

    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    fetchData()
    print("Uploading data in the database.\nPlease wait for a while...")
    time.sleep(2)
    dataMapping()
    print("Congratulation, Data Inserted Successfully!")
    time.sleep(2)
    os.remove(secondary_file)
