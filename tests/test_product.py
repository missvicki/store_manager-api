"""test authentication"""
import unittest
import json
import psycopg2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from api.views import app
from api.database import DatabaseConnection