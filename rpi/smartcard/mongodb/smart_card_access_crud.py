"""
Base class for storage data of the access executed via Smart Card

MIT License
Smart Card Contactless Raspberry Pi sample project

Copyright (c) 2022 Antonio Musarra (Antonio Musarra's Blog - https://www.dontesta.it)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from rpi import version
from pymongo import MongoClient

__author__ = "Antonio Musarra"
__copyright__ = "Copyright (c) 2022 Antonio Musarra (Antonio Musarra's Blog - https://www.dontesta.it)"
__credits__ = ["Antonio Musarra"]
__version__ = version.__version__
__license__ = "MIT"
__maintainer__ = "Antonio Musarra"
__email__ = "antonio.musarra@gmail.com"
__status__ = "Development"


class SmartCardAccessCrud:
    """
    The Python class for storage data of the access executed via Smart Card

    This class uses pymongo for retrieve and put data into mongodb database
    """

    def __init__(self, connection_url=None):
        if connection_url is None:
            self.client = MongoClient("mongodb://localhost:27017/")
        else:
            self.client = MongoClient(connection_url)

        database = "SmartCardAccessCrudDB"
        collection = "SmartCardAccess"

        cursor = self.client[database]

        self.collection = cursor[collection]

    def insert_data(self, data):
        response = self.collection.insert_one(data)

        return str(response.inserted_id)

    def read(self, search_filter=None):
        if search_filter is None:
            documents = self.collection.find()
        else:
            documents = self.collection.find(search_filter)

        return list(documents)

    def update_data(self, search_filter, data):
        updated_data = {"$set": data}
        response = self.collection.update_one(search_filter, updated_data)
        return response.modified_count

    def delete_data(self, search_filter):
        response = self.collection.delete_one(search_filter)
        return response.deleted_count
