import os
import sys
sys.path.insert(0,os.environ['Uml_Parser']+"plyj")
#sys.path.insert(0,'C:/PythonDirectory/dist/plyj-0.1/plyj/')
import plyj.parser as plyj
import types
import glob, os
import requests
import urllib
os.chdir(str(sys.argv[1]))
data_string = ""
referenceType={"name":"","className":"","relation":""}
referenceVariables=list()
methodParameters=list()
interfaceList=set()
variableList = set()
access=""
methods_name = set()
classList = list()

def classModifiers(classorinterface,data_string):
	try:
		modifier_list=classorinterface.modifiers
		for modifier_count in range(len(modifier_list)):
			pass
		return ""
	except ValueError:
		return ""	
		
def type_declarations(classorinterface,data_string):
	try:
		if str(type(classorinterface))=="<class 'plyj.model.InterfaceDeclaration'>" :
			interfaceList.add(classorinterface.name)
			data_string+="[<<interface>>;"+classorinterface.name
		else:

			classList.append(classorinterface.name)
			data_string+="["+classorinterface.name
		return data_string	
	except ValueError:
		return data_string	

def interfaceImplementation(classorinterface,data_string):
	try:
		if str(type(classorinterface))=="<class 'plyj.model.InterfaceDeclaration'>" :
			pass
		else :
			if classorinterface.implements:
				implements_list=classorinterface.implements
				for implements_count in range(len(implements_list)):
					referenceVariables.append({"name":implements_list[implements_count].name.value,"className":classorinterface.name,"relation":"^-.-"})
		return data_string		
	except ValueError:
		return data_string
		
def extendsClasses(classorinterface,data_string):
	try:
		if classorinterface.extends:
			extends=classorinterface.extends
			if str(type(classorinterface))=="<class 'plyj.model.InterfaceDeclaration'>" :
				referenceVariables.append({"name":extends.name.value,"className":classorinterface.name,"relation":"-.->"})
			else :
				referenceVariables.append({"name":extends.name.value,"className":classorinterface.name,"relation":"^-"})

		return data_string
	except ValueError:
		return data_string	

def modifier(body,access):
	try:
		modifier=body.modifiers
		for modifier_count in range(len(modifier)):
			if(modifier[modifier_count] == "private"):
				access='-'
			if(modifier[modifier_count] == "public"):
				access='+'
			if(modifier[modifier_count] == "protected"):
				access='#'
		return access
	except ValueError:
		return access		

def setModifierOfVariables(name):
	try:
		get = 0;
		set = 0;
		for methods_name_count in methods_name:
			if methods_name_count.lower()=="get"+name.lower():
				get=1
			if methods_name_count.lower()=="set"+name.lower():
				set=1
		return (get,set)		
	except ValueError:
		return (get,set)
		
def data_members(body,data_string):	
	global count_variable
	if count_variable == 0:			
		try:
			if str(type(body.type))=="<class 'plyj.model.Type'>" :
				data_string=type_arguments_list(body,data_string)
			else :
				variable_declarators_list=body.variable_declarators
				for variable_count in range(len(variable_declarators_list)):
					variableList.add(variable_declarators_list[variable_count].variable.name)
					name=variable_declarators_list[variable_count].variable.name
					(get,set)=setModifierOfVariables(name)
					if (get == 1 and set == 1):
						data_string+="|+"+name+":"+str(body.type)+";"
						count_variable+=1
					else:
						data_string+="|"+access+name+":"+str(body.type)+";"
						count_variable+=1
			return data_string
		except ValueError:
			return data_string
	else:			
		try:
			if str(type(body.type))=="<class 'plyj.model.Type'>" :
				data_string=type_arguments_list(body,data_string)
			else :
				variable_declarators_list=body.variable_declarators
				for variable_count in range(len(variable_declarators_list)):
					variableList.add(variable_declarators_list[variable_count].variable.name)
					name=variable_declarators_list[variable_count].variable.name
					(get,set)=setModifierOfVariables(name)
					if (get == 1 and set == 1):
						data_string+="+"+name+":"+str(body.type)+";"
					else:
						data_string+=access+name+":"+str(body.type)+";"
			return data_string
		except ValueError:
			return data_string			
					
def type_arguments_list(body,data_string):
	try:
		if body.type.type_arguments:				
			argument_list=body.type.type_arguments
			for argument_count in range(len(argument_list)):
				variableList.add(argument_list[argument_count].name.value)
				referenceVariables.append({"name":argument_list[argument_count].name.value,"className":classorinterface.name,"relation":"*"})
		else:
			data_string=variable_declarators_list(body,data_string)
			if str(type(body.type.name))=="<class 'plyj.model.Name'>":
				list1=body.type.name
				if list1.value != 'String' :
					variableList.add(list1.value)
					referenceVariables.append({"name":list1.value,"className":classorinterface.name,"relation":"1"})
		return data_string		
	except ValueError:
		return data_string			
		

def variable_declarators_list(body,data_string):
	global count_variable
	
	if count_variable == 0:
		try:
			variable_list=body.variable_declarators
			for variable_count in range(len(variable_list)):			
				if body.type.dimensions:
					if (body.type.dimensions)==1:
						variable_dimensions='*'
					if (body.type.dimensions)==2:	
						variable_dimensions='**'
					variableList.add(variable_list[variable_count].variable.name)	
					name=variable_list[variable_count].variable.name
					(get,set)=setModifierOfVariables(name)
					if (get == 1 and set == 1):
						data_string+="|+"+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"	
						count_variable+=1	
					else:
						data_string+="|"+access+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"	
						count_variable+=1	
				else:
					variableList.add(variable_list[variable_count].variable.name)	
					name=variable_list[variable_count].variable.name
					(get,set)=setModifierOfVariables(name)
					if (get == 1 and set == 1):
						data_string+="|+"+name+":"+str(body.type.name.value)+";"
						count_variable+=1
					else:
						if body.type.name.value=="String":
							data_string+="|"+access+name+":"+str(body.type.name.value)+";"
							count_variable+=1
			return data_string
		except ValueError:
			return data_string	

	else:
		try:
			variable_list=body.variable_declarators
			for variable_count in range(len(variable_list)):			
				if body.type.dimensions:
					if (body.type.dimensions)==1:
						variable_dimensions='*'
					if (body.type.dimensions)==2:	
						variable_dimensions='**'
					variableList.add(variable_list[variable_count].variable.name)	
					name=variable_list[variable_count].variable.name
					(get,set)=setModifierOfVariables(name)
					if (get == 1 and set == 1):
						data_string+="+"+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"		
					else:
						data_string+=access+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"		
				else:
					variableList.add(variable_list[variable_count].variable.name)	
					name=variable_list[variable_count].variable.name
					(get,set)=setModifierOfVariables(name)
					if (get == 1 and set == 1):
						data_string+="+"+name+":"+str(body.type.name.value)+";"
					else:
						if body.type.name.value=="String":
							data_string+=access+name+":"+str(body.type.name.value)+";"
			return data_string
		except ValueError:
			return data_string	
		
def constructionDeclaration(body,data_string):
	global count_method
	if count_method == 0:
		try:
			data_string+="|+"+body.name+"("
			if body.parameters:
				parameters_list=body.parameters
				data_string=parameters(parameters_list,data_string)
			data_string+=");"
			count_method+=1
			return data_string	
		except ValueError:
			return data_string
	else:
		try:
			data_string+="+"+body.name+"("
			if body.parameters:
				parameters_list=body.parameters
				data_string=parameters(parameters_list,data_string)
			data_string+=");"
			return data_string	
		except ValueError:
			return data_string

		
def method(body,data_string):
	global count_method
	if count_method == 0:
		try:
			methods_name.add(body.name)
			data_string+="|"+access+body.name+"("
			if body.parameters:
				parameters_list=body.parameters
				data_string=parameters(parameters_list,data_string)
			
			data_string=return_type(body,data_string)
			count_method+=1
			body_list=body.body
			for body_count in range(len(body_list)):
				body=body_list[body_count]	
				if str(type(body))=="<class 'plyj.model.VariableDeclaration'>":	
					if body.type.name.value != "String":
						methodParameters.append({"name":body.type.name.value,"className":classorinterface.name,"relation":"1"})
			return data_string
		except ValueError:
			return data_string


	else:
		try:
			methods_name.add(body.name)
			data_string+=access+body.name+"("
			if body.parameters:
				parameters_list=body.parameters
				data_string=parameters(parameters_list,data_string)
			data_string=return_type(body,data_string)	
			if str(type(body.body))=="<class 'plyj.model.VariableDeclaration'>" :
				if body.type.name.value != "String":
						methodParameters.append({"name":body.type.name.value,"className":classorinterface.name,"relation":"1"})
			return data_string
		except ValueError:
			return data_string

def return_type(body1,data_string):
	try:
		if str(type(body1.return_type))=="<class 'plyj.model.Type'>" :				
			data_string+="):"+str(body1.return_type.name.value)+";"
			#if body1.body:
				#print body1.body
			#	method_body1=body1.body
			#	data_string=method_body(method_body1,data_string)
		else:
			data_string+="):"+body1.return_type+";"						
		return data_string
	except ValueError:
		return data_string
		
def method_body(method_body1,data_string):
	try:
		#for method_count in range(len(method_body1)):
		#	if str(type(method_body1[method_count])) == "<class 'plyj.model.Return'>" :
		#		if str(type(method_body1[method_count].result)) == "<class 'plyj.model.MethodInvocation'>" :
		#			data_string+="):"+str(method_body1[method_count].result.name)+";"
		return data_string
	except ValueError:
		return data_string		
		
def parameters(parameters_list,data_string):
	try:
		
		for parameters_count in range(len(parameters_list)):
			if str(type(parameters_list[parameters_count].type))== "<class 'plyj.model.Type'>" :
				if parameters_list[parameters_count].type.type_arguments:				
					argument_list=parameters_list[parameters_count].type.type_arguments
					for argument_count in range(len(argument_list)):
						data_string+= parameters_list[parameters_count].variable.name+":"+argument_list[argument_count].name.value
						methodParameters.append({"name":argument_list[argument_count].name.value,"className":classorinterface.name,"relation":"*"})
				else:
					data_string+= parameters_list[parameters_count].variable.name+":"+parameters_list[parameters_count].type.name.value
					if parameters_list[parameters_count].type.name.value != 'String' :
						methodParameters.append({"name":parameters_list[parameters_count].type.name.value,"className":classorinterface.name,"relation":"1"})
			else :	
				data_string+= parameters_list[parameters_count].variable.name+":"+parameters_list[parameters_count].type
		return data_string
	except ValueError:
		return data_string	

		
def searchforfirst(data_string,first,first_start,last,last_start):
	try:
		
		data=""
		begin_index = data_string.index( first,first_start )
		first_start=begin_index
		(begin_index,last_index,data)=searchForLastAndCompare(data_string,first,first_start,last,last_start)
		if(begin_index=="0" and last_index=="0"):
			last_start=0
			first_start=first_start+len(first)
			(begin_index,last_index,data)=searchforfirst(data_string,first,first_start,last,last_start)
			return (begin_index,last_index,data)
		else:
			return(begin_index,last_index,data)
	except ValueError:
		begin_index="0"
		last_index="0"
		data=""
		return (begin_index,last_index,data)	

def searchForLastAndCompare(data_string,first,first_start,last,last_start):
	try:
		data=""
		last_index = data_string.index(last,last_start)
		last_start=last_index
		if (last_start>first_start and last_start>first_start+len(first)):
			
			if (data_string[first_start+len(first):last_start]=="uses -.->" ):
				data="uses -.->"
				return (first_start,last_start,data)
			elif (
				last_start-(first_start+len(first)) <=3 and data_string[first_start+len(first):last_start]!="," and data_string[first_start+len(first):last_start]!="^-.-" and data_string[first_start+len(first):last_start]!="-.->" and data_string[first_start+len(first):last_start]!="^-" 
				):
				data="FL"
				return (first_start,last_start,data)
			else:
				last_start=last_start+len(last)
				(begin_index,last_index,data)=searchForLastAndCompare(data_string,first,first_start,last,last_start)
				return (begin_index,last_index,data)
		
		if (last_start<first_start and first_start>(last_start+len(last))):
			if (
				first_start-(last_start+len(last)) <=3 and data_string[last_start+len(last):first_start]!="," and data_string[last_start+len(last):first_start]!="^-" and data_string[last_start+len(last):first_start]!="-.->" and data_string[last_start+len(last):first_start]!="^-.-"
				):	
				data="LF"
				return (last_start,first_start,data)
			else:
				last_start=last_start+len(last)
				(begin_index,last_index,data)=searchForLastAndCompare(data_string,first,first_start,last,last_start)
				return (begin_index,last_index,data)
			
	except ValueError:
		begin_index="0"
		last_index="0"
		data=""
		return (begin_index,last_index,data)		
		
		
def variable_linking(referenceVariables,methodParameters,data_string):
	try:
		
		for methodParameters_count in range(len(methodParameters)):
			methodParameters_Relation=methodParameters[methodParameters_count]["relation"]
			methodParameters_Name=methodParameters[methodParameters_count]["name"]
			methodParameters_ClassName=methodParameters[methodParameters_count]["className"]
			for interfaceList_Count in interfaceList:
				interfaceName=interfaceList_Count
				if interfaceName==methodParameters_Name:
					element1="["+methodParameters_ClassName+"]"
					element2="[<<interface>>;"+methodParameters_Name+"]"
					first_start=0
					last_start=0
					data=""
					(first_start,last_start,data)=searchforfirst(data_string,element1,first_start,element2,last_start)
					if (first_start=="0" and last_start=="0" and data=="" ):
						data_string+=element1+"uses -.->"+element2+","
						break
					else:
						pass
						break
					
					
		for referenceVariables_count in range(len(referenceVariables)):
			relation_1=referenceVariables[referenceVariables_count]["relation"]
			name=referenceVariables[referenceVariables_count]["name"]
			className=referenceVariables[referenceVariables_count]["className"]
			count = 0
			classOrNot=0
			
			#if relation_1=="^-.-" or relation_1=="-.->":
			#	for classList_count in range(len(classList)):
			#			class_1=classList[classList_count]
			#			if name==class_1:
			#				classOrNot=1
			#	if (relation_1=="^-.-" and classOrNot==1):
			#		data_string+="[<<interface>>;"+name+"]"+"^-.-"+"["+className+"]"+","
			#	if (relation_1=="-.->" and classOrNot==1):
			#		data_string+="["+name+"]"+"-.->"+"[<<interface>>;"+className+"]"+","
			#elif relation_1=="^-":
			#	for interfaceList_Count in range(len(interfaceList)):
			#		interfaceName=interfaceList[interfaceList_Count]
			#		if interfaceName==name:
			#			count = 1
			#	if(relation_1=="^-" and count==1)
			#		data_string+="["+name+"]"+"^-"+"["+className+"]"+","
			
			if relation_1=="^-.-":
				data_string+="[<<interface>>;"+name+"]"+"^-.-"+"["+className+"]"+","
			elif relation_1=="-.->":
				data_string+="["+name+"]"+"-.->"+"[<<interface>>;"+className+"]"+","
			elif relation_1=="^-":
				data_string+="["+name+"]"+"^-"+"["+className+"]"+","
			else:
				for interfaceList_Count in interfaceList:
					interfaceName=interfaceList_Count
					if interfaceName==name:
						count = 1
						element1="["+className+"]"
						element2="[<<interface>>;"+name+"]"
						first_start=0
						last_start=0
						data=""
						(first_start,last_start,data)=searchforfirst(data_string,element1,first_start,element2,last_start)
						if (data=="uses -.->"):
							data_string+=element1+"-"+relation_1+element2+","
						elif (data=="FL"):
							data_string=data_string[:first_start+len(element1)]+data_string[first_start+len(element1):last_start]+relation_1+data_string[last_start:]
						elif (data=="LF"):
							data_string=data_string[:first_start+len(element2)]+relation_1+data_string[first_start+len(element2):last_start]+data_string[last_start:]
						
						
						
						
						
						
						#start,end=relation(data_string,element2,element1,relation_1)
						#if (start==0 or end==0):
						#	data_string+=element1+"uses -.->"+element2+","
						#elif data_string[start:end] == ',':
						#	pass
						#else:
						#	data_string=data_string[:start]+data_string[start:end]+data_string[end:]
				
				
				
				if count == 0:
					first_start=0
					last_start=0
					data=""
					for classList_count in range(len(classList)):
						class_1=classList[classList_count]
						if name==class_1:
							classOrNot=1
					
					if classOrNot==1:
						element1="["+className+"]"
						element2="["+name+"]"
						(first_start,last_start,data)=searchforfirst(data_string,element1,first_start,element2,last_start)
						if (first_start=="0" and last_start=="0" and data==""):
							data_string+=element1+"-"+relation_1+element2+","
						elif (data=="FL"):
							data_string=data_string[:first_start+len(element1)]+data_string[first_start+len(element1):last_start]+relation_1+data_string[last_start:]
						elif (data=="LF"):
							data_string=data_string[:first_start+len(element2)]+relation_1+data_string[first_start+len(element2):last_start]+data_string[last_start:]
		return data_string		
	except ValueError:
		return data_string		
		
		
def genareteImage(data_string):
	try:
		print data_string	
		r = requests.get('http://yuml.me/diagram/scruffy/class/%2F%2F Cool Class Diagram,' +data_string)
		print r.status_code
		if r.status_code == 200:
			urllib.urlretrieve ('http://yuml.me/diagram/scruffy/class/%2F%2F Cool Class Diagram,' +data_string, os.path.join(str(sys.argv[1]),str(sys.argv[2])+'.png'))
	except requests.ConnectionError:
		print("failed to connect with YUML")		
			

def processFile(classorinterface,data_string):	
	try:
		
		data_string=type_declarations(classorinterface,data_string)
		if str(type(classorinterface))!="<class 'plyj.model.InterfaceDeclaration'>":
			body_list=classorinterface.body
			for body_count in range(len(body_list)):
				body=body_list[body_count]	
				validMethod = 1
				
				if str(type(body))=="<class 'plyj.model.ConstructorDeclaration'>":	
					data_string=constructionDeclaration(body,data_string)
				global access
				access=modifier(body,access)
				if access == "+":		
					if str(type(body))=="<class 'plyj.model.MethodDeclaration'>" :
						global variableList
						for variableList_count in variableList:
							if (
									"get"+variableList_count.lower()== body.name.lower() or "set"+variableList_count.lower()==body.name.lower()
								):
								validMethod = 0 
		
						if validMethod == 1:
							data_string=method(body,data_string)	
						
				#if (access == "+" or	access == "-"):
				if str(type(body))=="<class 'plyj.model.FieldDeclaration'>" :			
					data_string=data_members(body,data_string)
				access=""
		data_string+="]"+","
		variableList = set()
		data_string=interfaceImplementation(classorinterface,data_string)
		data_string=extendsClasses(classorinterface,data_string)
		return data_string
	
	except ValueError:
		return data_string	

def extractingContent(classorinterface,data_string):
	try:
		data_string=type_declarations(classorinterface,data_string)
		if str(type(classorinterface))!="<class 'plyj.model.InterfaceDeclaration'>" :
			body_list=classorinterface.body
			for body_count in range(len(body_list)):
				body=body_list[body_count]	
				global access
				access=modifier(body,access)
				if access == "+":		
					if str(type(body))=="<class 'plyj.model.MethodDeclaration'>" :
						data_string=method(body,data_string)
				access=""		
		return data_string				
	except ValueError:
		return data_string			
		
	
for file in glob.glob("*.java"):
	tree=plyj.Parser().parse_file(file)

	type_delaration_list = tree.type_declarations
	for type_delaration_count in range(len(type_delaration_list)):
		count_method =0
		count_variable=0

		classorinterface=type_delaration_list[type_delaration_count]
		data_string_1=extractingContent(classorinterface,data_string)
		data_string_1=""
	for type_delaration_count in range(len(type_delaration_list)):
		count_method =0
		classorinterface=type_delaration_list[type_delaration_count]
		data_string=processFile(classorinterface,data_string)
	methods_name = set()	
data_string=variable_linking(referenceVariables,methodParameters,data_string)		
genareteImage(data_string)