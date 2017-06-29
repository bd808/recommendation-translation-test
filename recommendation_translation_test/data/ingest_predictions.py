import sqlalchemy
import pandas
import sys


if __name__ == '__main__':
    engine = sqlalchemy.create_engine('postgresql://testing:testing@localhost/test')
    df = pandas.read_csv(sys.argv[1])
    df.to_sql('predictions', engine, if_exists='replace')
