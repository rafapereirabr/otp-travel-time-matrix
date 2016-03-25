# otp-travel-time-matrix
This repository aims to provide a reproducible example of how to build an Origin-Destination travel time matrix using OpenTripPlanner (OTP) and Python. The Python scripts presented here still can be much improved and it would be great to have your contributions, specially if you have ideas on how to improve the speed/efficiency of the code, or include a progress bar etc !

**Input**
* An Open Street Map of the region in `.pbf` format
* GTFS dataset
* The OTP java application `.jar` file
*  Jython standalone application `.jar` file
* A  `.csv` file with long lat of the points i
* A Python script 

**Output**
* A `.csv` file with the travel time between pairs of points. It looks something like this:
```
GEOID    GEOID    travel_time
    1        1            60
    1        2           861
    1        3          2234
    2        1           861
    2        2            42
    2        3          3032
    3        1          2235
    3        2          3040
    3        3            92
```

___
### This repository should help you build a travel time matrix in 4 simple steps


##### Step 1: Install Jython 2.7 in your computer
[Here](http://www.jython.org/downloads.html) you find the executable jar for installing Jython

##### Step 2: Download files to your folder

Most of the files you need are in this repository already. The other files you can download from here:

* [jython-standalone.jar](http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar)

* [otp-0.19.0-SNAPSHOT-shaded.jar](http://maven.conveyal.com.s3.amazonaws.com/org/opentripplanner/otp/0.19.0/otp-0.19.0-shaded.jar)
* [portland_oregon.osm.pbf](https://s3.amazonaws.com/metro-extracts.mapzen.com/portland_oregon.osm.pbf)


##### Step 3: Build Graph.obj
Open your Command Prompt and run this line to set the directory where you've saved the files

`cd C:\Users\rafa\Desktop\otp-travel-time-matrix`

Now run this line to build the Graph.obj

`java –Xmx10G -jar otp-0.19.0-SNAPSHOT-shaded.jar --cache C:\Users\rafa\Desktop\otp-travel-time-matrix --basePath C:\Users\rafa\Desktop\otp-travel-time-matrix --build C:\Users\rafa\Desktop\otp-travel-time-matrix`


##### Step 4: Run the Python script

Two options here:

**4.1** A simple script like `python_script.py` will return a travel time matrix for one single departing time (e.g. at 10:00:00 on  15-November-2015)

`c:\jython2.7.0\bin\jython.exe -J-XX:-UseGCOverheadLimit -J-Xmx10G -Dpython.path=otp-0.19.0-SNAPSHOT-shaded.jar python_script.py`

**4.2** Another option is to use a script like `python_script_loopHM.py`, which will create a different travel time matrix departing every ten minutes, say between 10am and 6pm, and save each matix in a separete `.csv` file

`c:\jython2.7.0\bin\jython.exe -J-XX:-UseGCOverheadLimit -J-Xmx10G -Dpython.path=otp-0.19.0-SNAPSHOT-shaded.jar python_script_loopHM.py`



This code is inspired by [@laurentg's code](https://github.com/opentripplanner/OpenTripPlanner/blob/master/src/test/resources/scripts/test.py) but it tries to achieve a different output, providing a travel time matrix. @laurentg has also made important contributions to this repository, to which I am grateful.

More information about how to automate OTP [here](http://docs.opentripplanner.org/en/latest/Scripting/).

