###
#       This is the init file for the manager 
#       of the database
#       
#       In this file is only the client Class
#
###
import os
import json

#_____________________________________Classes initialization____________________________________________#
class Data:
    def __init__(self, *args, **kwargs) -> None:
        """
        This class is used to store data from the JSON file.
        Args:
            args (Any): The arguments passed to the constructor of this class.
            kwargs (Dict[str, Any]): The keyworded arguments passed to the constructor of
            this class.

        Methods:
            The to_json method converts the object to JSON format.
        
        """
        for key, valure in kwargs.items():
            setattr(self, key, valure)

    def to_json(self):
        return self.__dict__
    
    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
    
    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value
    
    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __iter__(self):
        return iter(self.__dict__)
    
    def __len__(self):
        return len(self.__dict__)
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value

def from_json(data:dict):
    return Data(**data)

class Collection:
    def __init__(self, name: str, path: str) -> None:
        """
        Classs Collection
        Atributes:

        name: str
            The name of the collection
        path: str
            The path of the collection

        Methods:
            The __init__ method initializes the Collection object with a name, path, and an empty data list.
            The name method is a getter for the private __name attribute.
            The name setter updates the private __name attribute with a new value.
            The path method is a getter for the private __path attribute.
            The path setter updates the private __path attribute with a new value.
            The data method is a getter for the private __data attribute.
            The data setter appends a new value to the private __data list.
            The to_json method converts the object to JSON format.
            The __eq__ method checks if two Collection objects are equal.
            The __ne__ method checks if two Collection objects are not equal.
            The __hash__ method returns the hash value of the object.
            The create_file method creates a new file in the "database" directory with the name specified by the name attribute.
            The get_file method reads data from the file and stores it in the data list.
            The add_data_to_file method appends the last element of the data list to a file.
            The get_data_from_file method reads data from the file and stores it in the data list.
            The delete_data method deletes data from the data list.
            The delete_data_from_file method deletes data from the file.
            The add_data method adds data to the data list and calls the add_data_to_file method.
            The __str__ method returns a string representation of the object.
        """
        self.__name: str = name
        self.__path: str = path
        self.__data: list[Data] = []

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def path(self):
        return self.__path
    
    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, value: Data):
        self.__data.append(value)

    def to_json(self):
        """
        Convert the object to JSON format.
        Returns:
            The object itself in JSON format.
        """
        return self.__dict__

    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
    
    def __hash__(self) -> int:
        return self

    def create_file(self):
        """
        Creates a new file in the 'database' directory with the name specified by the 'name' attribute of the current object.
        
        Parameters:
            self (object): The current object.
        
        Returns:
            None
        
        Raises:
            ValueError: If a file with the same name already exists in the 'database' directory.
        """
        coll = os.listdir("database")

        if self.name in coll:
            raise ValueError("Collection already exists")
        
        with open(self.path, "w") as file:
            file.write(json.dumps({"coll_name" : self.name}) + "\n")

    def get_file(self):
        """
        Read the data from the file and store it in the data list.
        Parameters:
            None.
        Returns:
            None.
        """
        self.get_data_from_file()

    def add_data_to_file(self):
        """
        Append the last element of the data list to a file.
        Parameters:
            None.
        Returns:
            None.
        """
        print(self.data)
        with open(self.path, "a") as file:
            file.write(json.dumps(self.__data[-1].to_json()) + "\n")

    def get_data_from_file(self):
        """
        Read the data from the file and store it in the data list.
        Parameters:
            None.
        Returns:
            None.
        """
        with open(self.path, "r") as file:
            lines = file.readlines()

        for line in lines[1:]:
            self.__data.append(from_json(json.loads(line)))

    def delete_data(self, value: any):
        """
        Delete data from the list of data.
        Parameters:
            value (any): The value to be deleted from the list of data.
        Returns:
            None
        """
        self.delete_data_from_file(value)
        self.data.remove(value)

    def delete_data_from_file(self, value: any):
        """
        Delete data from the file.
        Parameters:
            value (any): The value to be deleted from the file.
        Returns:
            None
        """
        with open(self.path, "r") as file:
            lines = file.readlines()

        with open(self.path, "w") as file:
            for line in lines:
                line = line.strip()
                print(line, value.to_json())
                if value != json.loads(line):
                    file.write(line)

    def add_data(self, *args, **kwargs):
        """
        Adds data to the list of data. The function takes in any number of positional and keyword arguments.
        The data is added to the list self.data. After adding the data, the function calls the method self.add_data_to_file().
        Parameters:
            *args: Any number of positional arguments.
            **kwargs: Any number of keyword arguments.
        Returns:
            None
        """
        temp_data = Data(*args, **kwargs)
        self.data.append(temp_data)
        self.add_data_to_file()

    def __str__(self) -> str:
        return str(self.__dict__)

class DB:
    def __init__(self, db_name: str) -> None:
        """
        Class DB, is the databes manager
        Initializes the database object.
        Parameters:
            db_name (str): The name of the database.
        
        Attributes:
            __db_name (str): The name of the database.
            __collections (list[Collection]): A list of all the collections in the database.
        
        Methods:
            db_name: Getter and setter methods for the db_name attribute.
            collections: Getter and setter methods for the collections attribute.
            add_collection(self, name): Adds a new collection to the database by creating a new collection directory and file.
            get_collections(self): Returns a list of all the collections in the database by reading the collection directories and files.
            __str__(self) -> str: Returns a string representation of the database object.
            __eq__(self, __value: object) -> bool: Checks if two database objects are equal.
            __ne__(self, __value: object) -> bool: Checks if two database objects are not equal.
            __hash__(self) -> int: Returns the hash value of the database object.
            __repr__(self) -> str: Returns a string representation of the database object.
            __str__(self) -> str: Returns a string representation of the database object.
        """
        self.__db_name: str = db_name
        self.__collections: list[Collection] = []

    @property
    def db_name(self):
        return self.__db_name
    
    @db_name.setter
    def db_name(self, value):
        self.__db_name = value

    @property
    def collections(self) -> list[Collection]:
        return self.__collections
    
    @collections.setter
    def collections(self, value: Collection):
        self.__collections.append(value)

    def add_collection(self, name):
        """
        Adds a new collection to the database.
        Parameters:
            name (str): The name of the collection to be added.
        Returns:
            Dir: The newly created collection directory.
        """
        new_dir = Collection(name, f"database/{self.db_name}/{name}.jsonl")
        new_dir.create_file()
        self.collections.append(new_dir)

        return self.collections[-1]
    
    def get_collections(self):
        """
        Returns a list of all the collections in the database.
        Parameters:
            None.
        Returns:
            list: A list of all the collections in the database.
        """
        collections = os.listdir(f"database/{self.db_name}")
        self.__collections = [Collection(c.split(".")[0], f"database/{self.db_name}/{c}") for c in collections]  
        for collection in self.__collections:
            collection.get_file()
        return self.collections

    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__
    
    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
    
    def __hash__(self) -> int:
        return self
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def __str__(self) -> str:
        return str(self.__dict__)
    

class Client():
    def __init__(self) -> None:
        """
        Class Client, 
        Initialize the connection with the database with the use
        of the DB class.
        Atributes:
            db (DB): The database object.
        
        Methods:
            db: A property that returns the current database instance.
            db.setter: Sets the current database instance.
            __str__: Returns a string representation of the Client object.
            add_db: Initializes a new database with the given name, creates a directory for it, and returns the new database object.
            get_db: Initializes and returns a new instance of the DB class, sets it as the current database, and retrieves the collections for that database.
            make_dir: Creates a new directory called "database" in the current working directory.
        """
        self.__db: DB

        self.make_dir()

    @property
    def db(self):
        return self.__db
    
    @db.setter
    def db(self, value: DB):
        self.__db = value

    def __str__(self) -> str:
        return str(self.__dict__)
    
    def add_db(self, name: str):
        """
        Initializes a new database with the given name.
        Parameters:
            name (str): The name of the new database.
        Returns:
            DB: The newly created database.
        Raises:
            OSError: If the directory for the database already exists.
        """
        new_db = DB(name)
        self.db = new_db
        if not os.path.exists(f"database/{self.db.db_name}"):
            os.mkdir(f"database/{self.db.db_name}")

        return self.db

    def get_db(self):
        """
        Initializes and returns a new instance of the DB class.
        Parameters:
            self (object): The object instance.
        
        Returns:
            db (DB): The initialized DB object.
        """
        self.db = DB(os.listdir("database")[0])
        self.db.get_collections()

        return self.db
    
    def make_dir(self):
        """
        Creates a new directory in the current working directory.
        Parameters:
            None.
        Returns:
            None.
        """
        if not os.path.exists("database"):
            os.mkdir("database")
            return