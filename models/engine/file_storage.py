#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the list of objects of one type of class"""
        if cls is None:
            return list(self.__objects.values())
        elif isinstance(cls, str):
            return [v for k, v in self.__objects.items()
                    if v.__class__.__name__ == cls]
        else:
            return [v for k, v in self.__objects.items()
                    if isinstance(v, cls)]

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key, obj in self.__objects.items():
            json_objects[key] = obj.to_dict(save_to_disk=True)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                json_objects = json.load(f)
            for key, value in json_objects.items():
                cls_name = value["__class__"]
                if cls_name in classes:
                    obj = classes[cls_name](**value)
                    self.__objects[key] = obj
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """Deserialize JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieve an object"""
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key)

    def count(self, cls=None):
        """Count number of objects in storage"""
        if cls is None:
            return len(self.__objects)
        return len(self.all(cls))

