@echo off
echo.Welcome to UML Parser,

if "%~1"=="" (
	echo please enter command in the following format :
	echo umlparser D:/Nitesh/ ImageName
	goto :eof
)

if "%~2"=="" (
	echo please enter command in the following format :
	echo umlparser D:/Nitesh/ ImageName
	goto :eof
)

if not "%~3"=="" (
    echo No more than two arguments, please
	echo for eg: umlparser D:/Nitesh/ ImageName
    goto :eof
) 
echo Class Diagram Image will generate on path %1 with name as %2
python %Uml_Parser%Uml_Parser.py %1 %2	