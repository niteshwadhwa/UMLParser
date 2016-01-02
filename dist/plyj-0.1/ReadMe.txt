README.
Download dist folder from google drive.

These Descriptions are for running the UMLParser on Windows Operating System Only:
 
step 1:
As i have chosen python as programming lanaguage. so,python should be up and running with following Packages:
os,sys,types,glob,requests,urllib

Step 2:
Goto MyComputer->Properties->Advanced System Setting ->Environment Variable -> Click on Path and Edit
 append path as followed: ;<Path till dist folder>\dist\plyj-0.1\

Step 3: 
Goto MyComputer->Properties->Advanced System Setting ->Environment Variable -> Click on New
 Add Variable Name = Uml_Parser
 Add Variable_Value = <Path till dist folder then>\dist\plyj-0.1\

Step 4: 
Open a New command Prompt 
 
Step 5: 
Now you Can run UML Parser by passing two arguments:
First Argument : Path for Java Files
Second Argument : Name of class diagram image

Note : Image will be generated at the same location given in first argument and if any image with the same name exist,New Image will overwrite it. 
