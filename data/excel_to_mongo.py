# from jsonschema import Validator
from cmath import nan
from distutils.log import error
import json
import re
from turtle import title
import pandas as pd
import pymongo


conn_str = "mongodb+srv://keshab:keshab123@cluster0.bqo0o.mongodb.net/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(conn_str, connect=False)
    db_name = "marlabs_chatbot"
    response_coll_name = "responses"
    # form_coll_name = "forms"
    # topics_coll_name = "topics"
    my_db = client[db_name]
    my_coll = my_db[response_coll_name]
    # form_coll = my_db[form_coll_name]
    # topic_coll = my_db[topics_coll_name]
    # print("DB Connected successfully")
except pymongo.errors.ConnectionFailure as e:
    print("Database connection problem: ", e)

# Update response
def updateResponse(response_name, response_payload):
    query = {"response_name":response_name}
    new_values = response_payload
    my_coll.update_one(query, new_values)
    

def responseValidator(db_name, collection_name):
    response_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["response_name", "response_payload"],
            "properties": {
                "response_name": {
                    "bsonType": "string",
                    "unique": True,
                    "description": "Must be string and should match with anction in stories."
                },
                "response_payload": {
                    "bsonType": "array",
                    "description": "arrays of payloads"
                }
            }
        }
    }
    val = db_name.command("collMod",collection_name,validator=response_validator)
    # print(val)

def indexing(collection_name):
    # index1 = collection_name.create_index([("response_name", pymongo.DESCENDING)])
    index2 = collection_name.create_index([("response_name", 1)],unique= True)
    # print(index1)
    # print(index2)

    
def uploadResponses():
    xls = pd.ExcelFile('data/responses_data.xlsx')
    data = pd.read_excel(xls, 'responses')
    # Delete previous data in colection
    my_coll.delete_many({})

    # make 'response_name' field unique
    # indexing(my_coll)
    # print("total:",len(data))

    for index,row in data.iterrows():
        # break
        response_name = row[2].strip()
        resp_text = row[3]
        resp_buttons = row[4]
        resp_url = row[5]
        response_payload_arr=[]
        if (pd.isna(response_name)):
            print("No response name found: ",row)
            continue
        if(not pd.isna(resp_text)):
            raw_text = resp_text
            text_array = raw_text.split(";")
            text_resp_payload = {
                "type":"text",
                "data":text_array,
                "class":""
            }
            response_payload_arr.append(text_resp_payload)
            
        
        # if((pd.isna(resp_buttons)) and (pd.isna(resp_url)) and response_name!="action_utter_greet"):
            
        #     text = 'Can i help you with anything more?'
        #     # print("text")
        #     text_resp_payload = {
        #         "type":"text",
        #         "data":text
        #     }
        #     response_payload_arr.append(text_resp_payload)


        if(not pd.isna(resp_buttons)):
            btn_arr = resp_buttons.split(",")
            buttons_arr=[]
            for intent_button in btn_arr:
                intent_button = intent_button.split(":",1)
                button_title = intent_button[0].strip()
                button_intent = intent_button[1].strip()
                dict_button = {
                    "title":button_title,
                    "payload":button_intent
                }
                buttons_arr.append(dict_button)
            buttons_intent_payload = {
                "type":"buttons",
                "data":buttons_arr
            }
            response_payload_arr.append(buttons_intent_payload)

        if(not pd.isna(resp_url)):
            urls_arr = resp_url.split("|")
            buttons_url_arr=[]
            for url_button in urls_arr:
                print(url_button)
                url_button = url_button.split(";",1)
                button_title = url_button[0].strip()
                button_url = url_button[1].strip()
                dict_button = {
                    "title":button_title,
                    "url":button_url
                }
                buttons_url_arr.append(dict_button)
            buttons_url_payload = {
                "type":"buttons",
                "data":buttons_url_arr
            }
            response_payload_arr.append(buttons_url_payload)        
        
        response_obj ={
            "response_name": response_name,
            "response_payload": response_payload_arr
        }
        result = my_coll.find_one({"response_name":response_name})
        # If response name not in db
        if(result==None):
            res = my_coll.insert_one(response_obj)
            # print(response_name)
        
        # if(response_name=="action_utter_PRE_Definition"):
        updateResponse(response_name,{ "$set":response_obj})
        
        
def uploadForm():
    xls = pd.ExcelFile('ResponsesData\mChat Responses.xlsx')
    form_data = pd.read_excel(xls, 'forms')
    
    # Each row
    for index,row in form_data.iterrows():
        response_name = str(row[0]).strip()
        form_title = str(row[1]).strip()
        form_subtitle = str(row[2]).strip()
        form_fields = str(row[3]).strip()

        fields=[]
        # Each fields in form fields
        for field in form_fields.split(";"):
            field_array = field.strip("][").split(",")
            field_inputName = field_array[0].strip()
            field_slotName = field_array[1].strip()
            field_inputType = field_array[2].strip()
            
            fields.append({"inputName":field_inputName, "slotName":field_slotName, "inputType":field_inputType}) 
        
        # final form object 
        response_payload = {
            "response_name": response_name,
            "response_payload":[
                {"type":"form"},
                {"data":[
                    {"form_title": form_title},
                    {"form_subtitle": form_subtitle},
                    {"fields":fields}
                ]}
            ]
        }
        # print(response_payload)
        form_coll.delete_many({})
        res = form_coll.insert_one(response_payload)
    # print("form")

def uploadTopics():
    xls = pd.ExcelFile('ResponsesData\mChat Responses.xlsx')
    form_data = pd.read_excel(xls, 'responses')
    topic_coll.delete_many({})
    # Each row
    try:
        for index,row in form_data.iterrows():
            topic = str(row[4]).strip()
            if(topic!="nan"):
                check = topic_coll.find_one({"topic":topic})
                topic_intent = str(row[0]).strip()
                if(check==None):
                    resp = topic_coll.insert_one({"topic":topic, "topic_intent":topic_intent})
                    print("Insert => ",topic,":",topic_intent)
                else:
                    resp = topic_coll.update_one({"topic":topic},{"$set":{"topic_intent":topic_intent}})
                    print("Update => ",topic,":",topic_intent)


    except pymongo.errors.PyMongoError as e:
        print("Error while uploading topics. \nMessage: "+str(e))
            

###################
uploadResponses()
# uploadForm()
# uploadTopics()

