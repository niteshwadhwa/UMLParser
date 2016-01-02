# UMLParser 

• Designed a UML Parser to Reverse Engineer the Java Code back to UML Class Diagrams.                                                 
• It generates UML Class Diagram in PNG, JPEG and PDF formats, which can be easily downloaded.  

Compiling Instructions: 

Download dist folder (source code is present in this folder) from google drive present in Java Source Code Zip Folder 
These Descriptions are for using the UMLParser on Windows Operating System Only: 

Step 1: 
As I have chosen python-2.7 as programming lanaguage. so,python should be up and running with following Packages: 
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
Now you can run UML Parser by passing two arguments: 
First argument: Path for Java Files 
Second argument: Name of class diagram image 

Note: Image will be generated at the same location given in first argument and if any image with the same name exist, New Image will overwrite it

Cheers :)
