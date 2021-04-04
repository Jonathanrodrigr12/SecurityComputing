from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.configuration_manager import ConfigurationManger
from project.resources.utils.generals_utils import GeneralsUtils
from project.resources.utils.registry_utils import RegistryUtils


class PostgreSqlContext():

    __session_maker = None

    def __init__(self, connection_string_name):
        self.configure(connection_string_name)

    def get_connection_string_configuration(self, key):
        if not GeneralsUtils.validate_attribute(key, self.__configurations):
            return None

        return self.__configurations[key]

    def configure(self, connection_string_name):
        # T
        DATABASE_SYSTEMS = ('postgres', 'redis')
        # T
        DATABASE_DRIVERS = ('pg8000',)

        connection_string = ConfigurationManger.\
            get_connection_string(connection_string_name)

        connection_string_parts = connection_string.split(",")

        if len(connection_string_parts) != 3 and\
           len(connection_string_parts) != 4:
            raise Exception("")

        database_system = connection_string_parts[0]

        driver = connection_string_parts[1]

        parameters = connection_string_parts[2]

        configurations = ""

        if len(connection_string_parts) == 4 and\
           GeneralsUtils.validate_string(connection_string_parts[3]):
            configurations = "?{}".format(connection_string_parts[3])

        if database_system not in DATABASE_SYSTEMS:
            raise Exception("")

        if driver not in DATABASE_DRIVERS:
            raise Exception("")

        connection_string_split = "{}+{}://{}{}".\
            format(database_system,
                   driver,
                   parameters,
                   configurations).split("?")

        self.__connection_string = connection_string_split.pop(0)

        self.__configurations = {}

        try:
            configurations_array = connection_string_split[0].split("&")
            for configuration in configurations_array:
                key, value = configuration.split("=")
                self.__configurations[key] = value

        except Exception as error:
            raise Exception("", error)

        engine = create_engine(self.__connection_string)
        self.__session_maker = sessionmaker(bind=engine)

    def get_connection_string(self):
        return self.__connection_string

    @contextmanager
    def session(self):
        session = self.__session_maker()
        try:
            yield session
            session.commit()

        except Exception as error:
            session.rollback()
            raise Exception("Error trying to connect to the database", error)

        finally:
            session.close()
            session.bind.dispose()