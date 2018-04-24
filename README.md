# Touch

OutputTest.py is current code for Touch Media project. Requires devices plugged in.

touch_input.py is simple program that records input force and sends it to the server. Comes with a "calibrate" button to reset sensor back to 0. 

Other programs will need to ping touch_server with its data.

Touch_server contains clock and will record timestamp of other programs. It will then send data to touch_client (metadata stream), which writes data out in a csv.

Everything is writing to port 5000 currently, running on localhost.
