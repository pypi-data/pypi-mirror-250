# muscle-training

## About muscle-training
It uses a library called MediaPipe to recognize the posture of a person captured by a camera. It determines whether the arm is extended or not, and measures the number of times the arm was firmly extended and the time it was extended.
It can also be used to record training.


## How to install 

`pip install muscle-training`

## Display Contents
<img src='OK.JPG' height=270 wight=750>
<img src='NG.JPG' height=270 wight=750>

OK or NG ：　If the arms are well extended, OK is displayed; if not, NG is displayed.

Count　：The number of times the arm was extended is indicated.

Time　：　Displays the time that the arm was extended. Time is not added until the arm is lowered once.