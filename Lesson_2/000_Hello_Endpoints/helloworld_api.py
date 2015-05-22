"""Hello World API implemented using Google Cloud Endpoints.

Contains declarations of endpoint, endpoint methods,
as well as the ProtoRPC message class and container required
for endpoint method definition.
"""
import endpoints
from protorpc import messages #Toolkit for building APIs and uses Google's protocol buffers. Efficient data format that used from lots of languages.
from protorpc import message_types
from protorpc import remote


# If the request contains path or querystring arguments,
# you cannot use a simple Message class.
# Instead, you must use a ResourceContainer class
REQUEST_CONTAINER = endpoints.ResourceContainer( #Request class #Resource Containers supports options that messages.Message does not such as query string parameters.
    message_types.VoidMessage,
    name=messages.StringField(1), #Contains one field that is a string.
)

REQUEST_GREETING_CONTAINER = endpoints.ResourceContainer( #Request class #Resource Containers supports options that messages.Message does not such as query string parameters.
    period=messages.StringField(1), #Contains one field that is a string.
    name=messages.StringField(2),
)


package = 'Hello'


class Hello(messages.Message): #For response class need to define class that is subclass messages.Message.
    """String that stores a message."""
    greeting = messages.StringField(1) #Name: greeting; type: messages.StringField(#); Type could be another message type.


@endpoints.api(name='helloworldendpoints', version='v1') #Name and version are required arguments. #API name and class name do not have to be the same.
class HelloWorldApi(remote.Service): 
    """Helloworld API v1."""
                                                            #Each API method is a method in the api class
    @endpoints.method(message_types.VoidMessage, Hello, #Tells what it takes in its request and what it returns among other things.
      path = "sayHello", http_method='GET', name = "sayHello")
    def say_hello(self, request):
      return Hello(greeting="Hello World")
                                              #Request class: message_types.VoidMessage / REQUEST_CONTAINER; Response class: Hello
    @endpoints.method(REQUEST_CONTAINER, Hello,
      path = "sayHelloByName", http_method='GET', name = "sayHelloByName")
    def say_hello_by_name(self, request):
      greet = "Hello {}".format(request.name)
      return Hello(greeting=greet)

    @endpoints.method(REQUEST_GREETING_CONTAINER, Hello,
      path = "sayHelloByPeriod", http_method='GET', name = "sayHelloByPeriod")
    def say_hello_by_period(self, request):
      greet = "Good {}, {}!".format(request.period, request.name)
      return Hello(greeting=greet)


APPLICATION = endpoints.api_server([HelloWorldApi]) #Starts the server that supports the API
