# Touch

InputTest.py records all touch data up to the release and sends to TServer.py.
  Once a release is detected, it will try to recalibrate
metadata.py writes data form server into a CSV file

OutputTest.py is expecting input value and will squeeze accordingly.
InputOutputTest.py is a program that contains input and output stuff.


Other programs will need to ping touch_server with its data.

Touch_server contains clock and will record timestamp of other programs. It will then send data to touch_client (metadata stream), which writes data out in a csv.

Everything is writing to port 5000 currently, running on localhost.
