from environs import Env
import os

env = Env()

ROOT = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(os.path.dirname(ROOT))
env_file = os.path.join(BASE_DIR, '.env')
if env.bool('IS_TEST', False):
    env_file = os.path.join(BASE_DIR, '.test.env')
if os.path.exists(env_file):
    env.read_env(env_file)

DB_HOST = env('DB_HOST')
DB_PASSWORD = env('DB_PASSWORD')
DB_PORT = env('DB_PORT')
DB_USER = env('DB_USER')
CONNECTION_STRING = f'{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
DB_NAME = env('DB_NAME')
ENV = env('ENV')
PORT = env('PORT', 5432)
HOST = env('PORT', '127.0.0.1')

