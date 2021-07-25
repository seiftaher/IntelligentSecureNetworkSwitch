Intelligent Secure Network Switch
-----

### Introduction

Intelligent Secure Network Switch using machine learning.


### Tech Stack

Our tech stack will include:

* **Python3** as our script language
* **RYU**  as controller
* **Flow manager** 

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── simple_monitor_13.py. 
  ├── simple_switch_13.py
  ├── DataProcessing and Feature Extraction.py 
  ├── Machine Learning Model.ipynb 
  ```



### Development Setup


To start and run the Ryu controller,


0. Using the Docker to build the enviroment 
  ```
  $ docker run -it --privileged -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /lib/modules:/lib/modules \
  osrg/ryu-book
  ```

1. Install flowmanager:
  ```
  $ git clone https://github.com/martimy/flowmanager
  ```

2. Run the Ryu controller:
  ```
  $ cd /<the monitor path>
  $ ryu-manager ~/flowmanager/flowmanager.py simple_monitor_13.py
  ```

3. Navigate to Home page [http://localhost:8080/home/index.html](http://localhost:8080/home/index.html)
