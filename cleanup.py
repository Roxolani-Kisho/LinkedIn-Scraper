import csv
import re
import datetime

with open('test.txt') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    regex = re.compile('[^a-zA-Z\s#-]')
    for row in readCSV:
        lan = 0
        tool=0
        companyName = ""
        skills = []
        language = []
        topics = []
        jobTitle=""
        location=""
        contact=""
        for element in row:
            
            if element.find("location") != -1:
                
                location=regex.sub('',element.split(":",1)[1]).strip().replace("-",",")
                
            if element.find("contact info") != -1:
                contact= regex.sub('',element.split(":",1)[1]).strip().title()
                
            if element.find("company") != -1:
                companyName= regex.sub('',element.split(":",1)[1]).strip().title()
                
            if element.find("job_title") != -1:
                jobTitle= regex.sub('',element.split(":",1)[1].strip()).title()
                                
            elif element.find("Language") != -1:
                
                language.append(regex.sub('',element.split(":",1)[1]).strip())
                lan=1
            if lan:
                if(element.find("]")!=-1):
                    
                    element = regex.sub('',element.split(":",1)[0]).strip()
                    lan=0
                language.append(element.replace('"',''))
            elif element.find("Tools-") != -1:
                
                skills.append(regex.sub('',element.split(":",1)[1]))
                
                tool=1
            elif tool:
                if(element.find("]")!=-1):
                    element = regex.sub('',element.split(":",1)[0]).strip()
                    tool=0

                skills.append(element.replace('"',''))

        try:
            if language[0]=="":
           
                continue
            topics.append(language[0].strip())
            topics.append(skills[0].strip())
            topics.append(skills[1].strip())
            
            print(topics)
        except:
    
            continue
        
        file = open(companyName +"_CoverLetter.txt","w")
        file.write(datetime.datetime.today().strftime("%m/%d/%Y")+"\n")
        
        
        file.write("\n")
        file.write(companyName+"\n")
        file.write(location+"\n")
        file.write("\n")
        if(contact != ""):
            file.write("Dear "+contact+",\n")
        else:
            file.write("Dear "+companyName+" team,\n")
        file.write("\n")
        file.write("I would like to introduce myself as a Computer Science major  with an emphasis on Data Science. ")
        file.write("I am excited to be applying for the "  + jobTitle + " position at " +companyName+" which I found on LinkedIn. ")
        file.write("As someone who is highly focused and attentive to detail, I thrive on building quality systems that surpass end-users' expectations. ")
        file.write("I am thrilled at the opportunity to show off my technical expertise and leadership skills as part of " +companyName+"'s expert team. ")
        
        file.write("\n")
        file.write("\n")
        for x in topics:
            if(x == "Java"):
               file.write(str(java))
            elif(x == "Git"):
               file.write(str(git))
            elif(x == "API"):
               file.write(str(API))
            elif(x == "React"):
               file.write(str(REACT))
            elif(x == "Python"):
               file.write(str(python))
            elif(x == "Andriod"):
                file.write(str(andriod))
            elif(x == "C++")or (x=="C"):
               file.write(str(Cplus))
            elif(x == "SQL"):
               file.write(str(SQL))
            elif(x == "C#"):
               file.write(str(Csharpe))
            elif(x == "TensorFlow"):
               file.write(str(tensorflow))
            elif(x == "Machine Learning"):
               file.write(str(machinelearning))
            elif(x == "Multi-Threading"):
               file.write(str(multithreading))
            elif(x == "NLP"):
               file.write(str(NLP))
            elif(x == "Communication Skills"):
               file.write(str(communicationSkills))
            file.write("\n")
                
        file.write("Thank you for your time and consideration. ")
        file.write("This cover letter was auto generated. ")
        file.write("I am looking forward to learning more details about the " + jobTitle + " position at " +companyName+". ")
        file.write("As we move further through the hiring process I am eager to demonstrate my commitment to developing world-class software solutions for " +companyName+". \n")
        
        file.write("\n")
        file.write("Sincerely,\n")
        file.write("\n")
        
        file.close()    
