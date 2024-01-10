import sys
import logging
import psycopg2


class TestDatabaseConnection:

    def setup_class(self):
        self.host = 'postgres_test'
        self.username = 'postgres'
        self.password = 'postgres'
        self.port = '5432'
        self.dbname = 'postgres'
        self.conn = None
        logging.basicConfig(level=logging.INFO)

    def test_connection(self):
        """Connect to a Postgres database."""
        try:
            if(self.conn is None):
                self.conn = psycopg2.connect(host=self.host,
                                             user=self.username,
                                             password=self.password,
                                             port=self.port,
                                             dbname=self.dbname)
            assert True
        except psycopg2.DatabaseError as e:
            logging.error(e)
            assert False
            sys.exit()
        finally:
            logging.info('Connection opened successfully.')
