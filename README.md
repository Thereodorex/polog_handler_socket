# Socket handler for polog lib

## Usage

### Client
```python
  from socket_handler import socket_sender

  HOST = '127.0.0.1'
  PORT = 65432
  
  from polog import config
  from polog import flog
  
  config.add_handlers(socket_sender(HOST, PORT))
  
  @flog
  def logged_func(arg):
    return arg
    
  logged_func("test polog socket handler")
```
    
### Server
```python
  from socket_handler import Server
  
  HOST = '127.0.0.1'
  PORT = 65432
  
  def simple_handler(args, **kwargs):
    print(args)
    print(kwargs)

  print("Server started.")
  app = Server(HOST, PORT, handler=simple_handler) # Any polog handler could be here
  app.start_server()
  app.loop()
  app.stop_server()
```
