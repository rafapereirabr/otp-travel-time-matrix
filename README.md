# otp-travel-time-matrix
This repository aims to provide a reproducible example of how to build an Origin-Destination matrix using OpenTripPlanner (OTP). The Python script still can be improved, for example to increase speed/efficiency of the code. Contributions are welcomed !

**Input**
* An Open Street Map of the region in `.pbf` format
* GTFS dataset
* The OTP java application `.jar` file
*  Jython standalone application `.jar` file
* A  `.csv` file with long lat of the points i

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

#### Python Version

##### Step 1: Install Jython 2.7 in your computer
[Here](http://www.jython.org/downloads.html) you find the executable jar for installing Jython

##### Step 2: Download files to your folder

Most of the files you need are in this repository alredy. The other files you can download from here:

* [jython-standalone.jar](http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar)

* [otp-0.19.0-SNAPSHOT-shaded.jar](http://dev.opentripplanner.org/jars/otp-0.19.0-SNAPSHOT-shaded.jar)
* [portland_oregon.osm.pbf](https://s3.amazonaws.com/metro-extracts.mapzen.com/portland_oregon.osm.pbf)


##### Step 3: Build Graph.obj
Open your Command Prompt and run this line to set the directory where you've saved the files

`cd C:\Users\rafa\Desktop\otp-travel-time-matrix`

Now run this line to build the Graph.obj

`java –Xmx10G -jar otp-0.19.0-SNAPSHOT-shaded.jar --cache C:\Users\rafa\Desktop\otp-travel-time-matrix --basePath C:\Users\rafa\Desktop\otp-travel-time-matrix --build C:\Users\rafa\Desktop\otp-travel-time-matrix`


##### Step 4: Run the Python script

`c:\jython2.7.0\bin\jython.exe -J-XX:-UseGCOverheadLimit -J-Xmx10G -Dpython.path=otp-0.19.0-SNAPSHOT-shaded.jar test.py`

#### Lisp Version

##### Step 1: Get ABCL

1. Go to <http://abcl.org>, download the binary distribution and put it somewhere you can get to it.

2. Then go to <https://www.quicklisp.org> and download "quicklisp.lisp". 

3. Get quicklisp: `java -jar abcl-bin-1.3.3/abcl.jar --load ~/quicklisp.lisp --eval '(quicklisp-quickstart:install)' --eval '(quit)'`

##### Step2: Download files

As in the python version, except the Jython jar file is unnecessary.

##### Step3: Build Graph.obj

As in the pyhon version

##### Step4: Run the Lisp Script

`java -d64 -XX:MaxPermSize=1g -XX:+CMSClassUnloadingEnabled -Xmx10G -XX:-UseGCOverheadLimit -Djava.library.path=. -cp otp-0.19.0-SNAPSHOT-shaded.jar:abcl-bin-1.3.3/abcl.jar org.armedbear.lisp.Main  --load ~/quicklisp/setup.lisp --load test.lisp --eval '(quit)'`


This code is inspired by [@laurentg's code](https://github.com/opentripplanner/OpenTripPlanner/blob/master/src/test/resources/scripts/test.py) but it tries to achieve a different output, providing a travel time matrix. @laurentg has also made important contributions to this repository, to which I am grateful.

More information about how to automate OTP [here](http://docs.opentripplanner.org/en/latest/Scripting/).

