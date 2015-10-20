# otp-travel-time-matrix
This repository aims to provide a reproducible exmple of how to build a travel time matrix using OpenTripPlanner (OTP).

As you will notice, the code is not working (yet). I've created this repo because I need you help to make it work :) and because it could be a useful reference for others in the future.


___
### This repository should help you build a travel time matrix in 4 simple steps


##### Step 1: Install Jython 2.7 in your computer
[Here](http://www.jython.org/downloads.html) you find the executable jar for installing Jython

##### Step 2: Download files to your folder

Most of the files you need are in this repository alredy. The other files you can download from here:

* [jython-standalone.jar](http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar)

* [otp-0.19.0-SNAPSHOT-shaded.jar](http://dev.opentripplanner.org/jars/otp-0.19.0-SNAPSHOT-shaded.jar)
* [portland_oregon.osm.pbf](https://s3.amazonaws.com/metro-extracts.mapzen.com/portland_oregon.osm.pbf)


##### Step 3: Build Graph.obj
Open your Command Prompt and run this line to set the directory where you've saved the files

`cd C:\Users\rafa\Desktop\otp-travel-time-matrix2`

Now run this line to build the Graph.obj

`java –Xmx10G -jar otp-0.19.0-SNAPSHOT-shaded.jar --cache C:\Users\rafa\Desktop\otp-travel-time-matrix2 --basePath C:\Users\rafa\Desktop\otp-travel-time-matrix2 --build C:\Users\rafa\Desktop\otp-travel-time-matrix2\portland`


##### Step 4: Run the Python script

`c:\jython2.7.0\bin\jython.exe -Dpython.path=otp-0.19.0-SNAPSHOT-shaded.jar test.py`


This code is inspired by [@laurentg's code](https://github.com/opentripplanner/OpenTripPlanner/blob/master/src/test/resources/scripts/test.py) but it tries to achieve a different output, providing a travel time matrix.


More information about how to automate OTP [here](http://docs.opentripplanner.org/en/latest/Scripting/).

