from typing import Any
import os
import pandas as pd
import pymongo
import json
from ensure import ensure_annotations


from typing import Any
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
import json
from ensure import ensure_annotations

# Lets write code to create package of mongodb database
class mongodb_operation: # here i have created a class and given named as monogdb_operation, we use the class and objects concepts inorder to have ability to use certain part of the code of the class so we class code through once the object is initlized at outside of the class so by using the initlized object we can use the any part of the code of the class so here part of the code means which we defined various fucntion like create_client,create_database etc 

    def __init__(self,client_url: str, database_name: str, collection_name: str=None): #  # inisde the mongodb_operation class i have defined one method or function which is constructor file and passed 3 parameters which are client_url,database_name,collection_name here first i have defined the construter for utilizing the arguments which i passed to constructor in the anyhwere part of the code of class, we can use those construtor arguments once we intilized those arguments with self then that means we can those arguments anywhere part of the code of class
        self.client_url=client_url  # here iam initlizing varaibles by using self and varaibles of which that i have defined 3 parameters inside my constructor fucntion ,we use self for the arguments which it helps us use those arguments anyhwere of part of the code of a class so self acts as an  
        self.database_name=database_name # so self acts as object to use arguments of the the constructor so  that's y i have intilized the self with those 3 arguments to reuse those arguments in anywhere part of the code of the class
        self.collection_name=collection_name

    def create_client(self): # here iam creating the client so that's y i have defined the another fucntion with self keyword to resue the varaible or argument that we created in the construtor file
        client=MongoClient(self.client_url) # So by using MongoClient function iam using reusing the self.client varaible and which iam passing into varaible client
        return client  # so here iam returning the client 


    def create_database(self):  # here  iam creating the database so thats y i have defined the fucntion with self keyword to use the create_client()
        client=self.create_client()  # here for creating the database we required the client right as we disscuesd in the mongodb concept  that's y iam getiing the client from the above fucntion through self keyword 
        database=client[self.database_name] # here iam passing the self.database_name varaible in the client  and database name passing into the variable database
        return database  # here iam returining that database
        
    def create_collection(self,collection=None): # so after creating the database we required the collection file to save our docuemnt which the data is in formate of Key:value pair
        database=self.create_database()  # the same i have created the collection by using the database_name
        collection=database[collection]
        return collection

    def insert_record(self,record:dict,collection_name:str): # After done creation of collection file i have to insert the record either single record or muiltple record so for that iam writng the logic below which helps to insert the signle and muiltple records in the collection file
        if type(record)==list: # writing a logic for getiing to know whether the inserting record type is list or not so i said that if the record type is found as list  , so here list means a document which consist of many records with key:value pair so like that document we pass the more dict values in the list then that would become a document with many records 
            for data in record: # here iam interating over each record by data varaible 
                if type(data)!= dict: # while iterating if i found that my data varaiable datatypes is not dict then iam raising Typeerror  with message that record must be in dict datatype
                    raise TypeError("record must be in the dict")
                # if the datapassed the above logic then iam going to write the logic below which helps us to insert many records of data in the collection
            collection=self.create_collection(collection_name)
            collection.insert_many(record)
            # if the datapassed the above logic then iam going to write the logic below which helps us to insert single records of data in the collection
        elif type(record)==dict:
            collection=self.create_collection(collection_name)
            collection.insert_one(record)

# if we want ot insert the bulk data then iam writing the below logic which helps to insert the bulk data 
    def bulk_insert(self,datafile:str,collection_name:str=None):
        self.path=datafile

         # here iam writing the condition to read the datafile if it is in excel or csv file 
        if self.path.endswith('.csv'):
            data=pd.read_csv(self.path,encoding='utf-8')

        elif self.path.endswith('.xlsx'):
            data=pd.read_excel(self.path,encoding='utf-8')
        # here iam converting the data into json formate then only i can load the data     
        datajson=json.loads(data.to_json(orient='record')) # here i orient= record means iam originizing data in the form of record 

         # here iam going to save that converted data into json one in collection finally, so below by adding function with logics we can add many fuctionalities to our package here fucntionalitlies means update delete etc 
        collection=self.create_collection()
        collection.insert_many(datajson)

# till here we done with writing the logic of inserting either single or many or bulk records inside our class now we need to call class through object for executing the logic that we created inside the class

# here Mongodb_crud.py consist of the code which is related to the mongodb_database conenction so we can add the functionalities like the