from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType, AllSlotsReset, FollowupAction

import re
import time
import pymongo
import random

# MongoDB connection


def connectDB(coll_name):
    conn_str = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.7.0"
    try:
        client = pymongo.MongoClient(conn_str)
        db_name = "marlabs_chatbot"
        my_db = client[db_name]
        my_coll = my_db[coll_name]
        # print("DB Connected successfully:")
        return my_coll
    except pymongo.errors.ConnectionFailure as e:
        print("Database connection problem: ", str(e))

## query DB and send response


def getResponse(response_name):
    coll_name = "responses"
    my_coll = connectDB(coll_name)
    try:
        res = my_coll.find_one({"response_name": response_name})

        if (res == None):
            print("Result None for response name: ", response_name)
            return []
        response = res["response_payload"]
        # print(my_coll.find({"response_name": response_name}).explain()["executionStats"])
        for item in response:
          if(item['type']=="text"):
            data = item['data']
            selected_text = random.choice(data)
            item['data'] = selected_text
        return response
    except pymongo.errors.OperationFailure as e:
        print("MongoDB Operational Failure: ", e.details)
        return []


#########################################
class ActionUtterGreet(Action):
    def name(self) -> Text:
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_greet"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return [FollowupAction(name="action_utter_menu")]

class ActionUtterMenu(Action):
    def name(self) -> Text:
        return "action_utter_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_menu"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return []

class ActionUtterGoodbye(Action):
    def name(self) -> Text:
        return "action_utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_goodbye"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return []

class ActionUtterCanIHelpMore(Action):
    def name(self) -> Text:
        return "action_utter_can_i_help_more"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_can_i_help_more"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return []

class ActionUtterTypeQueryBelow(Action):
    def name(self) -> Text:
        return "action_utter_type_query_below"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_type_query_below"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return []


class ActionUtterPleaseRephrase(Action):
    def name(self) -> Text:
        return "action_utter_please_rephrase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_please_rephrase"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return []
#################################################
class ActionUtterAboutMarlabs(Action):
    def name(self) -> Text:
        return "action_utter_about_marlabs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_about_marlabs"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return [FollowupAction(name="action_utter_can_i_help_more")]

class ActionUtterWhatDoYouDo(Action):
    def name(self) -> Text:
        return "action_utter_what_do_you_do"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_what_do_you_do"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return [FollowupAction(name="action_utter_can_i_help_more")]

class ActionUtterTalkToAdvisor(Action):
    def name(self) -> Text:
        return "action_utter_talk_to_advisor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_talk_to_advisor"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return [FollowupAction(name="action_utter_can_i_help_more")]

class ActionUtterMarlabsCareer(Action):
    def name(self) -> Text:
        return "action_utter_marlabs_career"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_marlabs_career"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return [FollowupAction(name="action_utter_can_i_help_more")]

class ActionUtterLatestPublications(Action):
    def name(self) -> Text:
        return "action_utter_latest_publications"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp_name = "utter_latest_publications"
        response = getResponse(resp_name)
        dispatcher.utter_message(json_message=response)
        return [FollowupAction(name="action_utter_can_i_help_more")]