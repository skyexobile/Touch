# Touch

OutputTest.py is current code for Touch Media project. Requires devices plugged in.

Other programs will need to ping touch_server with its data.

Touch_server contains clock and will record timestamp of other programs. It will then send data to touch_cient (metadata stream), which writes data out in a csv.

Everything is writing to port 5000 currently, running on localhost.
