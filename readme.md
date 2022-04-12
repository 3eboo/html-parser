### Running the project

* Go to project directory (html-parser) & Create virtual env 
  * `python3 -m venv .`
* activate your virtual environment:
  * `source venv/bin/activate`
* install scrapy & Twisted with these versions as they are the ones used when developed and compatible with each other.
  * `pip3 install scrapy==1.7.4`
  * `pip3 install Twisted==20.3.0`
* Now run the main file which will extract the data required from `task-booking.html` and export it to `output_data.json` as json formatted stream
  * `python3 main.py`
