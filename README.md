**UDATE**: you got interested in the repo, you should know that we have developed much easier and much more efficient ways of calculating travel time matrices in [python using the r5py package](https://r5py.readthedocs.io/en/stable/), and in [R using the r5r package](https://ipeagit.github.io/r5r/).

# Tutorial with reproducible example to estimate a travel time matrix using OpenTripPlanner and Python
This repository aims to provide a reproducible example of how to build an Origin-Destination travel time matrix using [OpenTripPlanner (OTP)](http://docs.opentripplanner.org/en/latest/) and Python. The Python scripts presented here can still be improved and it would be great to have your contributions, specially if you have ideas on how to improve the speed/efficiency of the code, or include a progress bar etc !

**Input**
* An Open Street Map of the region in `.pbf` format
* GTFS dataset
* The OTP java application `.jar` file
*  Jython standalone application `.jar` file
* A  `.csv` file with long lat of your points of interest (trip origins and destinations)
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


#### Step 1: Install Jython 2.7 in your computer
[Here](http://www.jython.org/downloads.html) you find the executable jar for installing Jython

#### Step 2: Download files to your folder

Most of the files you need are in this repository already. The other files you can download from here:

* [jython-standalone.jar](http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar)
* [otp-1.3.0-shaded.jar](https://repo1.maven.org/maven2/org/opentripplanner/otp/1.3.0/otp-1.3.0-shaded.jar)
* [portland_oregon.osm.pbf](https://s3.amazonaws.com/metro-extracts.mapzen.com/portland_oregon.osm.pbf)


#### Step 3: Build Graph.obj
Open your Command Prompt and run this line to set the directory where you've saved the files

`cd C:\Users\rafa\Desktop\otp-travel-time-matrix`

Now run this line to build the Graph.obj. Once OTP has built the Graph.obj, move it to the subdirectory `portland`.

`java –Xmx10G -jar otp-1.3.0-shaded.jar --cache C:\Users\rafa\Desktop\otp-travel-time-matrix --basePath C:\Users\rafa\Desktop\otp-travel-time-matrix --build C:\Users\rafa\Desktop\otp-travel-time-matrix`


#### Step 4: Run the Python script

Three options here:

**4.1** A simple script like `python_script.py` will return a travel time matrix for one single deaprture time (e.g. at 10:00:00 on  15-November-2015)

`c:\jython2.7.0\bin\jython.exe -J-XX:-UseGCOverheadLimit -J-Xmx10G -Dpython.path=otp-1.3.0-shaded.jar python_script.py`

**4.2** The second option is to use a script like `python_script_loopHM.py`, which will create a different travel time matrix departing every ten minutes, say between 10am and 6pm, and save each matix in a separete `.csv` file

`c:\jython2.7.0\bin\jython.exe -J-XX:-UseGCOverheadLimit -J-Xmx10G -Dpython.path=otp-1.3.0-shaded.jar python_script_loopHM.py`


**4.3** The third option uses the python script named `python_script_loopHM_parallel.py`, and it allows one to estimate various travel time matrices for different departure times (similarly to the second option) but using parallel computing. This makes things much faster because each computer processor will compute the travel-time matrix of a different departure time in parallel.

`c:\jython2.7.0\bin\jython.exe -J-XX:-UseGCOverheadLimit -J-Xmx10G -Dpython.path=otp-1.3.0-shaded.jar python_script_loopHM_parallel.py`


This code is inspired by [@laurentg's code](https://github.com/opentripplanner/OpenTripPlanner/blob/master/src/test/resources/scripts/test.py) but it tries to achieve a different output, providing a travel time matrix. @laurentg has also made important contributions to this repository, to which I am grateful. The two python scripts that use multiple threads to run in parallel were  developed in collaboration with [Nate Wessel](https://github.com/Nate-Wessel) and Jader Martins. Nate and Jader did most of the heavy lifting, really.


More information about how to automate OTP [here](http://docs.opentripplanner.org/en/latest/Scripting/).


## Citation

If you have used this script in your work and you would like to cite it, you can use the following reference:
[![DOI](https://zenodo.org/badge/44453629.svg)](https://zenodo.org/badge/latestdoi/44453629)
 
```
Pereira, R. H. M.; Grégoire, L.; Wessel, N.; Martins, J. (2019). Tutorial with reproducible example to estimate a travel time matrix
using OpenTripPlanner and Python. Retrieved from https://github.com/rafapereirabr/otp-travel-time-matrix. 
doi:10.5281/zenodo.3242134
```


