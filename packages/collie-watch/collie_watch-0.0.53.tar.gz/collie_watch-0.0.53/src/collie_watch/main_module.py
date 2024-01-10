
import datetime
import logging
import random
from traceback import format_exception, format_tb
from typing import List,Callable
import requests
import hashlib
import sys
import asyncio
from dataclasses import dataclass
from threading import Lock, Thread,Event
from PIL import Image
import numpy as np
from queue import SimpleQueue
import io
from contextlib import contextmanager
import time
from hashlib import sha256
from secrets import token_hex
from collections import deque
import atexit
import uuid
import inspect
from supabase import create_client,Client
import websockets.client as websockets 
import websockets.exceptions as websockets_exceptions
import json
import time
from datetime import timedelta
import psutil
import secrets
from bs4 import BeautifulSoup
import string
import copy

from .utils import Utils
from .widgets.widget import Widget
def _dict_to_ordered_list(d):
    """
    Converts a dictionary with numerical keys to an ordered list of its values.
    Assumes the dictionary keys are consecutive integers starting from 0 or 1.
    """
    # Sort the dictionary by keys and extract the values
    sorted_values = [value for key, value in sorted(d.items(), key=lambda item: int(item[0]))]
    return sorted_values

class CollieWatchHtmlEvents:
    """
    Represents a list of possible HTML events that can be received when using the library.
    """
    CLICK = "click"
    DOUBLE_CLICK = "dblclick"
    MOUSE_DOWN = "mousedown"
    MOUSE_UP = "mouseup"
    KEY_DOWN = "keydown"
    KEY_PRESS = "keypress"
    KEY_UP = "keyup"
    MOUSE_ENTER = "mouseenter"
    MOUSE_LEAVE = "mouseleave"
    FOCUS = "focus"
    BLUR = "blur"
    CHANGE = "change"
    INPUT = "input"
    MOUSE_MOVE = "mousemove"
    WHEEL = "wheel"
    CONTEXT_MENU = "contextmenu"
    TOUCH_START = "touchstart"
    TOUCH_END = "touchend"
    TOUCH_MOVE = "touchmove"
    TOUCH_CANCEL = "touchcancel"
    DRAG_START = "dragstart"
    DRAG = "drag"
    DRAG_ENTER = "dragenter"
    DRAG_LEAVE = "dragleave"
    DRAG_OVER = "dragover"
    DROP = "drop"
    DRAG_END = "dragend"
    MOUSE_OVER = "mouseover"
    MOUSE_OUT = "mouseout"
    RESIZE = "resize"
    SCROLL = "scroll"
    RECEIVED_FILE = "received_file"
    MENU_SELECTION = "menu_selection"

class CollieWatchHtmlInternalEvents:
    # INTERNAL
    SENDING_FILE_CHUNK = "sending_file_chunk"
    HTML_ELEMENTS_REMOVED_BY_ID = "html_elements_removed_by_id"
    internal_events = [SENDING_FILE_CHUNK,HTML_ELEMENTS_REMOVED_BY_ID]


class CollieWatchEvent:
    """
    INTERNAL
    Represents the various events CollieWatch can handle from server.
    """
    UPDATE = "update"
    SET_DASHBOARD_HTML = "set_dashboard_html"
    SET_HTML_CHILDREN_BY_ID = "set_html_children_by_id"
    APPEND_HTML_CHILDREN_BY_ID = "append_html_children_by_id"
    HTML_EVENT: str = "html_event"
    CHILDREN_NOT_FOUND_WITH_ID: str = "children_not_found_with_id"
    REPLACE_HTML_ELEMENT_BY_ID = "replace_html_element_by_id"
    

class CollieWatch:
    """
    Main class for the CollieWatch functionality.
    """
    __api_request_callback = lambda x: x
    __callbacks_map = {}
    __supabase: Client = None
    __token: str = None
    __pool: SimpleQueue = SimpleQueue()
    __thread_lock = Lock()
    __background_thread: Thread()
    __dev = False
    __callbacks_to_call_sync = SimpleQueue()
    __start_time = time.monotonic()
    __program_id = None
    __program_name = None
    __html_event_callback = lambda x: x
    __file_chunks_pool = {}

    @staticmethod
    def add_callback_by_id(id,types,callback):
        """
        Adds a callback function to the given HTML element ID and event type.

        Args:
            id (str): The ID of the HTML element.
            event_type (str): The type of the event.
            callback (Callable): The callback function.
        """
        if not CollieWatch.__callbacks_map.get(id):
            CollieWatch.__callbacks_map[id] = {}
        if not CollieWatch.__callbacks_map[id]:
            CollieWatch.__callbacks_map[id] = {}
        for type in types:
            #print(f'registering callback for {type} on {id}')
            CollieWatch.__callbacks_map[id][type] = callback

    @staticmethod
    def has_initialized():
        """
        Checks if CollieWatch has been initialized.

        Returns:
            bool: True if initialized, False otherwise.
        """
        return CollieWatch.__token != None

    @staticmethod
    def set_development_mode():
        """
        Enables the development mode for CollieWatch.
        """

        CollieWatch.__dev = True
    
    @staticmethod
    def set_html_event_callback(callback):
        """
        Sets the callback function for handling HTML events.

        Check README for examples.

        Args:
            callback (Callable): The callback function.
        """
        CollieWatch.__html_event_callback = callback

    @staticmethod
    def set_receive_api_request_callback(callback):
        """
        NOT IMPLEMENTED

        Sets the callback function for handling received API requests.

        Args:
            callback (Callable): The callback function.
        """
        CollieWatch.__api_request_callback = callback

    

    @staticmethod
    async def ___background_thread_handler():
        """
        INTERNAL 

        Background thread handler for managing WebSocket communication.
        """
        print(f"starting background thread with token {CollieWatch.__token}")
        subprotocols = ["_".join(["program",CollieWatch.__token,CollieWatch.__program_id] + ([] if CollieWatch.__program_name == None else ["-".join(CollieWatch.__program_name.split())]))]
        async with websockets.connect("wss://seal-app-isidc.ondigitalocean.app/" if not CollieWatch.__dev else "ws://localhost:8080",timeout=120,subprotocols=subprotocols,max_size=104857600 * 10) as websocket:
            
            try:
                await asyncio.sleep(3)
                asyncio.create_task(CollieWatch.__check_for_message(websocket))
                
                while True:       
                    await websocket.send(json.dumps({"type":CollieWatchEvent.UPDATE,"data":{"time":time.monotonic() - CollieWatch.__start_time,"program_id":CollieWatch.__program_id,
                        "process_data":{"cpu":psutil.cpu_percent(),"memory_used":psutil.virtual_memory().used,"memory_total":psutil.virtual_memory().total,"disk_used":psutil.disk_usage('/').used,"disk_total":psutil.disk_usage("/").total}}}))
                    while not CollieWatch.__pool.empty():
                        data = CollieWatch.__pool.get()
                        await websocket.send(data)
                    await asyncio.sleep(0.3)
            except websockets_exceptions.ConnectionClosedError:
                print("Connection closed, reopenning")
                

    @staticmethod
    def __add_to_pool(event_type: str,data: dict):
        """ 
        INTERNAL

        Adds the given event and data to the processing pool.

        Args:
            event_type (str): The type of the event.
            data (dict): Data associated with the event.
        """
        CollieWatch.__pool.put(json.dumps({"type":event_type,"data":data,"program_id":CollieWatch.__program_id}))
    

    @staticmethod
    async def __check_for_message(websocket: websockets.WebSocketClientProtocol):
        """
        INTERNAL

        Monitors the WebSocket for incoming messages and processes them.

        Args:
            websocket (websockets.WebSocketClientProtocol): The active WebSocket connection.
        """
        print("starting checking for messages")
        while True:
            try:
                message = await websocket.recv()
                message = json.loads(message)
                if message["type"] == CollieWatchEvent.HTML_EVENT:
                    if message["data"]["type"] in CollieWatchHtmlInternalEvents.internal_events:
                        if message["data"]["type"] == CollieWatchHtmlInternalEvents.SENDING_FILE_CHUNK:
                            if CollieWatch.__file_chunks_pool.get(message["data"]["target_id"]) == None:
                                CollieWatch.__file_chunks_pool[message["data"]["target_id"]] = []
                            
                            #receiving individual chunks
                            CollieWatch.__file_chunks_pool[message["data"]["target_id"]] += _dict_to_ordered_list(message["data"]["chunk"])
                            
                            
                            if message["data"]["target_id"] in CollieWatch.__callbacks_map and  CollieWatch.__callbacks_map[message["data"]["target_id"]].get(CollieWatchHtmlInternalEvents.SENDING_FILE_CHUNK):
                                    callback = lambda a=message["data"]:  CollieWatch.__callbacks_map[a["target_id"]][CollieWatchHtmlInternalEvents.SENDING_FILE_CHUNK]({"type":CollieWatchHtmlInternalEvents.SENDING_FILE_CHUNK,"progress":a["progress"],"target_id": a["target_id"],"chunk":a["chunk"]})
                                    CollieWatch.__callbacks_to_call_sync.put(callback)
                                    
                            if message["data"]["last_chunk"]:

                                callback_to_use = lambda a=message["data"],b=CollieWatch.__file_chunks_pool[message["data"]["target_id"]]: CollieWatch.__html_event_callback({"type":CollieWatchHtmlEvents.RECEIVED_FILE,"target_id": a["target_id"],"file":bytes(b),"file_name":a["file_name"]})
                                
                                #general callback
                                CollieWatch.__callbacks_to_call_sync.put(callback_to_use)
                                        
                                #specific callback for the widget
                                if message["data"]["target_id"] in CollieWatch.__callbacks_map and CollieWatch.__callbacks_map[message["data"]["target_id"]].get(CollieWatchHtmlEvents.RECEIVED_FILE):
                                    callback = lambda a=message["data"],b=CollieWatch.__file_chunks_pool[message["data"]["target_id"]]: CollieWatch.__callbacks_map[a["target_id"]][CollieWatchHtmlEvents.RECEIVED_FILE]({"type":CollieWatchHtmlEvents.RECEIVED_FILE,"target_id": a["target_id"],"file":bytes(b),"file_name":a["file_name"]})
                                    CollieWatch.__callbacks_to_call_sync.put(callback)
                                
                                del CollieWatch.__file_chunks_pool[message["data"]["target_id"]]
                        
                        continue
                    
                    CollieWatch.__callbacks_to_call_sync.put(lambda a=message["data"]: CollieWatch.__html_event_callback(a) if len(inspect.signature(CollieWatch.__html_event_callback).parameters) > 0 else CollieWatch.__html_event_callback())
                    if message["data"]["target"].get("id") and CollieWatch.__callbacks_map.get(message["data"]["target"]["id"]):
                        if CollieWatch.__callbacks_map[message["data"]["target"]["id"]].get(message["data"]["type"]):
                            callback = CollieWatch.__callbacks_map[message["data"]["target"]["id"]][message["data"]["type"]]
                            CollieWatch.__callbacks_to_call_sync.put(lambda a=message["data"]: callback(a) if len(inspect.signature(callback).parameters) > 0 else callback())
                    
                        
                if message['type'] == CollieWatchEvent.CHILDREN_NOT_FOUND_WITH_ID:
                    print(f'Could not find any children with id "{message["data"]}"')
                elif message["type"] == CollieWatchHtmlInternalEvents.HTML_ELEMENTS_REMOVED_BY_ID:
                    for id in message["data"]:
                        if id in CollieWatch.__callbacks_map:
                            del CollieWatch.__callbacks_map[id]

            except asyncio.TimeoutError:
                continue
            except websockets_exceptions.ConnectionClosedError:
                break
            except Exception as e:
                print(e)

    @staticmethod
    def run_events_sync():
        """
        Runs the registered synchronous events.
        """
        while not CollieWatch.__callbacks_to_call_sync.empty():
                callback = CollieWatch.__callbacks_to_call_sync.get()
                callback()

    @staticmethod
    def initialize(token,program_name=None):
        """
        Initializes CollieWatch with the provided token and program name.

        Args:
            token (str): The token for initialization.
            program_name (str, optional): The program name to show on the dashboard. Please do not provide names separated by underlines ("_").Defaults to "Untitled Program".

        Returns:
            bool: True if initialization succeeded, False otherwise.
        """
        CollieWatch.__supabase = create_client("https://acyzjlibhoowdqjrdmwu.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjeXpqbGliaG9vd2RxanJkbXd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTMyNTI2MDgsImV4cCI6MjAwODgyODYwOH0.cSP7MaxuIZUknfp-_9srZyiOmQwokEdDXlyo4mci_S8")
        try:
            data,count = CollieWatch.__supabase.from_("dashboards").select("*").eq("dashboard_token",token).execute()
            user_found = len(data[1]) != 0
            if not user_found:
                print(f'Could not find any dashboards with token "{token}".\nPlease provide a valid dashboard token!')
                return False
            CollieWatch.__program_name = program_name
            CollieWatch.__program_id = secrets.token_hex(16)
            CollieWatch.__token = token
            CollieWatch.__background_thread = Thread(target=asyncio.run,args=(CollieWatch.___background_thread_handler(),),daemon=True)
            CollieWatch.__background_thread.start()

            if CollieWatch.__dev:
                print("Development mode enabled. Please make sure you have the CollieWatch backend running on localhost:8080")
        

            return user_found
        except Exception as e:
            print(e)
            return False
    

   
    @staticmethod
    def __assign_ids_to_html_elements(html):
        """Assign random IDs to all elements in the HTML that don't have IDs."""
        soup = BeautifulSoup(html, 'html.parser')

        for tag in soup.find_all(True):  # finds all tags
            if not tag.get("id"):
                tag['id'] = Utils.generate_random_id()

        return str(soup)
    


    @staticmethod
    def set_dashboard_html(html):

        
        html = html if not isinstance(html,Widget) else html.render()
        modified_html = CollieWatch.__assign_ids_to_html_elements(html)
        CollieWatch.__add_to_pool(CollieWatchEvent.SET_DASHBOARD_HTML, {"html": f"<div>{modified_html}</div>"})

    @staticmethod
    def set_html_children_by_id(id, html):
        html = html if not isinstance(html,Widget) else html.render()
        modified_html = CollieWatch.__assign_ids_to_html_elements(html)
        CollieWatch.__add_to_pool(CollieWatchEvent.SET_HTML_CHILDREN_BY_ID, {"id": id, "html": modified_html})

    @staticmethod
    def append_html_children_by_id(id, html):
        html = html if not isinstance(html,Widget) else html.render()
        modified_html = CollieWatch.__assign_ids_to_html_elements(html)
        CollieWatch.__add_to_pool(CollieWatchEvent.APPEND_HTML_CHILDREN_BY_ID, {"id": id, "html": modified_html})

    @staticmethod
    def replace_html_element_by_id(id, html):
        html = html if not isinstance(html,Widget) else html.render()
        modified_html = CollieWatch.__assign_ids_to_html_elements(html)
        CollieWatch.__add_to_pool(CollieWatchEvent.REPLACE_HTML_ELEMENT_BY_ID, {"id": id, "html": modified_html})

    