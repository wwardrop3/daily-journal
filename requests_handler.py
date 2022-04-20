
from http.server import BaseHTTPRequestHandler, HTTPServer
# from multiprocessing.sharedctypes import Value

import json

from Views.entry_requests import create_new_entry, delete_entry, get_all_entries, get_entries_by_search_term, update_entry
from Views.entry_requests import get_single_entry
from Views.mood_requests import get_all_moods
from Views.tag_request import get_all_tags




# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


# class is the blueprint for an object...self is a reference to the class itself...self is "my " pronoun...makes instance first then passes instance into the class to attach the properties
# init creates empty object, then calls its own init method, passes the object into init method to attach properties to it

# this is a unique request handler
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    # tv guide of the API
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        
        self._set_headers(201)
        
        content_len = int(self.headers.get("content-length", 0))
        
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        parsed = self.parse_url(self.path)
        
        (resource, id) = parsed
        
        new_entry = None
        
        if resource == "entries":
           new_entry = create_new_entry(post_body)
        
        self.wfile.write(f"{new_entry}".encode())
        
        
        
        
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    # self contains a path that includes the id we are going to delete
    def do_DELETE(self):
        
        self._set_headers(204)
        parsed = self.parse_url(self.path)
        
        if len(parsed) == 2:
            (resource, id) = parsed
            if resource == "entries":
                delete_entry(id)
        
        self.wfile.write("".encode())
        
    #this method is going to override the parent's method.  Handles modifying PUT requests
    def do_PUT(self):
        content_len = int(self.headers.get("content-length", 0))
        
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        parsed = self.parse_url(self.path)

        (resource, id) = parsed
    
        success = False
    
        if resource == "entries":
            success = update_entry(post_body, id)
        
        if success:
            self._set_headers(200)
            # if rows were affected, that means the object being updated was found and altered so 200 is success message
        else: 
            self._set_headers(404)
        
        
        self.wfile.write("".encode())

# Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)
        
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed
            
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
                    
            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = f"{get_all_moods()}"
            
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "q" and resource == "entries":
                response = get_entries_by_search_term(value)
                
            elif key =="q" and resource =="animals":
                
                # this results as a json string
                response = get_animals_by_location(value)
                
            elif key =="location_id" and resource =="employees":
                print(key)
                
                # this results as a json string
                response = get_employees_by_location(value)
                
                
            elif key =="status" and resource =="animals":
                print(key)
                
                # this results as a json string
                response = get_animals_by_status(value)

        # this sends back the encoded response to the client
        self.wfile.write(f"{response}".encode())
        
        
        
    def parse_url(self, path):
        
        path_params = path.split("/")
        resource = path_params[1]
        
        
        if "?" in resource:
            param = resource.split("?")[0]
            resource = resource.split("?")[1]
            pair = resource.split("=")
            key = pair[0]
            value = pair[1]
            
            return (param, key, value)
            
        else:
            id = None
            
            try:
                # None/animals/None
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
    
            
        
        
        
        


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    # this is where the external server address would go
    host = ''
    # a host can have multiple things, so the 8088 is the apartment unit of the building
    port = 8088
    # port is basically the event listener, where the httpserver is listening for changes
    #inside http server will instantiate the new handle requests object
    HTTPServer((host, port), HandleRequests).serve_forever()
    # it will only make 1 instance of handle requests at the outset before an actual request is made


# this protects the file from being called elsewhere
if __name__ == "__main__":
    main()
    