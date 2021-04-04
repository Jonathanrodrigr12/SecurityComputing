from pyms.flask.app import Microservice
from project.models.init_database import database


class AppMicroserviceIp(Microservice):
    def init_libs(self):

        database.init_app(self.application)
        with self.application.test_request_context():
            database.create_all()


def create_app():
    """Initialize the Flask app, register blueprint and intialize all libraries
    return the app and the database objects.
    :return:
    """

    microservice = AppMicroserviceIp(path=__file__)
    app = microservice.create_app()

    return app
