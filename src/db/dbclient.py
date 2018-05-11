import logging
import os
import pymongo
import feedparser


class MongoClient:
    url = "mongodb://{user}:{password}@ds263639.mlab.com:63639/trufflex"

    def __init__(self, collection=None):
        password = os.environ.get('MONGO_PASS')
        user = os.environ.get('MONGO_USER')
        url = MongoClient.url.format(user=user, password=password)
        self.client = pymongo.MongoClient(url)
        self.db = self.client.get_database('trufflex')
        if collection is not None:
            self.collection = self.db.get_collection(collection)

    @staticmethod
    def fromCollection(collection):
        return MongoClient(collection)


class RssClient(MongoClient):

    def __init__(self):
        super().__init__("RSS")

class KnowledgeClient(MongoClient):

    def __init__(self):
        super().__init__("knowledge")


# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# from ssl import CERT_NONE
#
# from airflow.hooks.base_hook import BaseHook
# from pymongo import MongoClient
#
#
# class MongoHook(BaseHook):
#     """
#     PyMongo Wrapper to Interact With Mongo Database
#     Mongo Connection Documentation
#     https://docs.mongodb.com/manual/reference/connection-string/index.html
#     You can specify connection string options in extra field of your connection
#     https://docs.mongodb.com/manual/reference/connection-string/index.html#connection-string-options
#     ex.
#         {replicaSet: test, ssl: True, connectTimeoutMS: 30000}
#     """
#     conn_type = 'MongoDb'
#
#     def __init__(self, conn_id='mongo_default', *args, **kwargs):
#         super(MongoHook, self).__init__(source='mongo')
#
#         self.mongo_conn_id = conn_id
#         self.connection = self.get_connection(conn_id)
#         self.extras = self.connection.extra_dejson
#
#     def get_conn(self):
#         """
#         Fetches PyMongo Client
#         """
#         conn = self.connection
#
#         uri = 'mongodb://{creds}{host}{port}/{database}'.format(
#             creds='{}:{}@'.format(
#                 conn.login, conn.password
#             ) if conn.login is not None else '',
#
#             host=conn.host,
#             port='' if conn.port is None else ':{}'.format(conn.port),
#             database='' if conn.schema is None else conn.schema
#         )
#
#         # Mongo Connection Options dict that is unpacked when passed to MongoClient
#         options = self.extras
#
#         # If we are using SSL disable requiring certs from specific hostname
#         if options.get('ssl', False):
#             options.update({'ssl_cert_reqs': CERT_NONE})
#
#         return MongoClient(uri, **options)
#
#     def get_collection(self, mongo_collection, mongo_db=None):
#         """
#         Fetches a mongo collection object for querying.
#         Uses connection schema as DB unless specified
#         """
#         mongo_db = mongo_db if mongo_db is not None else self.connection.schema
#         mongo_conn = self.get_conn()
#
#         return mongo_conn.get_database(mongo_db).get_collection(mongo_collection)
#
#     def aggregate(self, mongo_collection, aggregate_query, mongo_db=None, **kwargs):
#         """
#         Runs and aggregation pipeline and returns the results
#         https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.aggregate
#         http://api.mongodb.com/python/current/examples/aggregation.html
#         """
#         collection = self.get_collection(mongo_collection, mongo_db=mongo_db)
#
#         return collection.aggregate(aggregate_query, **kwargs)
#
#     def find(self, mongo_collection, query, find_one=False, mongo_db=None, **kwargs):
#         """
#         Runs a mongo find query and returns the results
#         https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find
#         """
#         collection = self.get_collection(mongo_collection, mongo_db=mongo_db)
#
#         if find_one:
#             return collection.find_one(query, **kwargs)
#         else:
#             return collection.find(query, **kwargs)
#
#     def insert_one(self, mongo_collection, doc, mongo_db=None, **kwargs):
#         """
#         Inserts a single document into a mongo collection
#         """
#         collection = self.get_collection(mongo_collection, mongo_db=mongo_db)
#
#         return collection.insert_one(doc, **kwargs)
#
#     def insert_many(self, mongo_collection, docs, mongo_db=None, **kwargs):
#         """
#         Inserts many docs into a mongo collection.
#         https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.insert_many
#         """
#         collection = self.get_collection(mongo_collection, mongo_db=mongo_db)
#
#         return collection.insert_many(docs, **kwargs)
#
#
# class MongoOperator(BaseOperator):
#     """
#     Executes sql code in a specific Postgres database
#     :param postgres_conn_id: reference to a specific postgres database
#     :type postgres_conn_id: string
#     :param sql: the sql code to be executed
#     :type sql: Can receive a str representing a sql statement,
#         a list of str (sql statements), or reference to a template file.
#         Template reference are recognized by str ending in '.sql'
#     :param database: name of database which overwrite defined one in connection
#     :type database: string
#     """
#
#     template_fields = ('sql',)
#     template_ext = ('.sql',)
#     ui_color = '#ededed'
#
#     @apply_defaults
#     def __init__(
#             self, sql,
#             mongo_conn_id='postgres_default',
#             parameters=None,
#             database=None,
#             *args, **kwargs):
#         super(MongoOperator, self).__init__(*args, **kwargs)
#         self.sql = sql
#         self.postgres_conn_id = postgres_conn_id
#         self.autocommit = autocommit
#         self.parameters = parameters
#         self.database = database
#
#     def execute(self, context):
#         self.log.info('Executing: %s', self.sql)
#         self.hook = MongoHook(postgres_conn_id=self.postgres_conn_id,
#                                  schema=self.database)
#         self.hook.run(self.sql, self.autocommit, parameters=self.parameters)
#         for output in self.hook.conn.notices:
#             self.log.info(output)