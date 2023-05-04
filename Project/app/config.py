import os


class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USERNAME = os.getenv('DB_USERNAME', 'sexymanager')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'helloworld')
