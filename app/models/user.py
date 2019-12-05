import os
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
from flask import current_app

from app.extension import mongo
from app.errors import api_abort

class User(object):     

    @staticmethod
    def set_password(pwd):
        password_hash = generate_password_hash(pwd)
        return password_hash

    @staticmethod
    def validate_password(password_hash, password):
        return check_password_hash(password_hash, password)

    
    def validate_user_exist(self, query):
        ''':param query: <class dict> {"_id": "xxx"}'''
        user_info = mongo.db.users.find_one(query)
        if user_info:
            return True
        return False
    

    def insert(self, user_info):
        """Insert user info
        Args:
            user_info: dict
            username: str
            email:  str or  None
            password_hash: str or None

        Returns:
            返回一个 ObjectId 的str 

            For example:
                5de675e4cc14c528f2e98969

        Raises:

        """
        pwd = user_info.get('password', '')

        Object_Id = mongo.db.users.insert_one({
            "username" : user_info["username"],
            "password_hash" : self.set_password(pwd),
            "email" : user_info.get('email', ''),
            "role" : "USER",
            "avatar_url": user_info.get('avatar_url', ''),
            "locket" : False,
        }).inserted_id # Object_Id:  <class bson.objectid.ObjectId>
        current_app.logger.info(f'Create User: {Object_Id}')
        return str(Object_Id)

    def find(self, query):
        '''
        Args:
            query: <str:user_id> or dict 

        Returns:
            dict or None 
            For example:
                {
                    '_id': '',
                    'username': '',
                    'email': '',
                    'role': 'USER' or 'ADMIN',
                    'locket: False,
                    'password_hash':'',
                }
        Raises:
            None
        '''
        if type(query) == str:
            u = mongo.db.users.find_one({'_id': ObjectId(query)})
        else:
            u = mongo.db.users.find_one(query)
        if u:
            u['_id'] = str(u['_id'])
            return u
        else: 
            return None


user = User()