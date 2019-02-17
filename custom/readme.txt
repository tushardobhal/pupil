Main Components - 

1. gaze_glass.py - This is the mian class that starts the program. The following ar ethe parameters that can be tuned - 
	a. port_glass_1 - This is the lisening port for data of Glass 1. The default is 50020.
    b. port_glass_2 = This is the lisening port for data of Glass 1. The default is 50021.
    c. confidence_threshold - The confidence used for when merging the gaze dots from both eyes. The default is 0.80.
    d. num_objects - The number o fobjects to be detected.  The default is 6.
    e. use_both_eyes - This decides whether to use both eyes. Default is True and t doesnt really impact the performance.
    f. debug - This decides whether toshow the output image from YOLO. The default is True.

2. world_listener.py - This receives the world frames, its frame index and the timestamp. These along with the glass_id is stored in a proxy object.

3. eye_listener.py - Two processes, one for each eye per glass, of this listener is started when use_both_eyes is True. It receives the gaze information for both the eyes (separately), the timestamp and the confidence score of the gaze dot. Next it is passed through kalman filter and the output is recorded in a proxy object.

4. do_stuff.py (to be renamed) - This is the important class that does all the heavy lifting. This process is started twice, one for each glass, and it aggregated the latest world frames and pupil proxy objects stored by the listeners. It then computes the pupil location from the confidence score, passes the frame_data for object detectionand then passes the result to the run length filter. Finally, the data that is needed (run_length_output, timestamp, frame_index) is stored in a proxy object.

5. do_stuff_with_combined_eye.py - This is similar to above and is only used when use_both_eyes is False. It then receives information from only one eu=ye_listener process (as it receives data for both eyes in a single listener).

6. do_stuff_together (to be renamed) - This is class aggreagtes the proxy objects stored by the do_stuff processes for coth the glass, checks the run_length filter and plays a ticking sound when they match for a particular object.

Algorithm Implementing classes - 

1. kalman.py - This implements the kalman filter and takes pupil_location and timestamp as the input. The following parameters can be tweeked - 
	a. max_vel - This is the tolerance for change in x and y with time. Higher this value, more we are tolerant to the inputs.
	b. noise - This controls the jitter. The highe the value, the lower the jitter is, but might smoothen the gaze dot too much.
	c. time - This parameter is dependent on the frame_rate.

2. object_detect.py - This is the class that implements Yolov3-tiny object detection algorithm. Two separate proxies are started, one for each glass. Main parameter to tweek is the thresh parameter, which is the threshold for the confidence of the object detection algorithm.

3. run_length_filter - This detects whether a look is detected or not. It has a paramter called total_num_states, which controls after how many frames alook is detected. The output of this fiter is an array of one-hot code where ` being the output when the gaze dot falls within the particular object.

Objects - 

1. world.py - This contains the parameters that are received for the world frames.
2. pupil.py - This contains theparameters that are received for the pupil information.
3. common_data.py - This is the object that is created to store common data from both the glasses, which will be compared in do_stuff_together.

Running the code - 

 - ./start.sh - This will start the program and will initialize all the processes and the Yolov3-tiny object detector. This will display the layers of the object detector that is being loaded. Press any button after the layers are loaded for both object detectors. 

The logs are stored in the file gaze_glasses.log - The lines are recorded as follows - 
2018-11-30 15:11:39,897 | [gaze_1_glass_1] | [kalman.py predict] | [INFO] - Received - (94.88047217632311, 693.0068082153607, 15775.377153), Predicted - (94.88047217632311, 693.0068082153607)

	a. 2018-11-30 15:11:39,897 - time when the log is recorded
	b. [gaze_1_glass_1] - the thread name that is printitng this log line. The names of the thread can be seen when we define the process in gaze_glass.py
	c. kalman.py - this is the python file where the log line is printed
	d. predict - this is the method name where the log line is located
	e. INFO - this refers to information. Others include, DEBUG and WARN and ERROR
	f. Next the line is printed.

To search for the information that is processed from both glasses after the run_length filter - 
grep "do_stuff_together" gaze_glasses.log

- Then start both the processes of both glasses by running the following command in separate kernel - 
python3 main.py
Next, in the pupi labs' 'world frame' that is started second, change it's port number to 50021. The code assumes the ports to be 50020 and 50021. Once all 3 programs are up, we can see the world frames and the pupil dots with the objects' bounding boxes. 

Running the Android App and Listener - 

1. Launch the app called PushButton. 
2. To launch the receiver, go to ~/gaze_glasses/MQReceiver
3. Launch ./start.sh to start the MQReceiver, ./stop.sh to stop it
4. The logs are stored in console.log. The application is started when the following log is printed - 
	2018-14-11 23:14:12.638 [main] INFO  com.ece.ucsd.rabbitmq.Receiver - Connecting to RabbitMQ server - amqp://vgocndla:xP3XY98IZenywMYEVGcg3TDl-Hqie-h6@otter.rmq.cloudamqp.com/vgocndla
	2018-14-11 23:14:12.858 [main] INFO  com.ece.ucsd.rabbitmq.Receiver - Listener started. Waiting for messages...
   

