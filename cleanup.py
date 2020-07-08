import csv
import re
import datetime
java = ("After completing the intro programming classes I applied those skills to produce games in Java. After several projects, I gained proficiency in setting project milestones, "
       
"searching for solutions and user design. I also learned the importance of perseverance and resolving problems.\n")
API = ("As a researcher under Dr Kate Starbird, I worked on understanding disinformation campaigns by examining Twitter accounts and their postings. "
       "I scraped around 20,000 accounts using the Twitter API. These projects made me confident in working independently, presenting in front of an audience, and knowing how to get help.\n")
REACT = ("In my last year of college, I was part of a team to develop a web page for Puget Sound Energy using AGILE development. Using REACT we created tables display the status of various transformers, graphs "
       "and interfaced with Google maps to display the transformer's location. This project showed me the importance of communication with the end-user and the power of having a diverse team.\n")
andriod = ("During a hackathon, I produced an app than listen to user voice commands to read out parts of a recipe. I used Google’s built-in speech to text and text to speech libraries to accomplish this. "
           "This work helped me get familiar with the Android SDK, rapid prototyping and making a product that has a demand.\n")
SQL=("As part of a three-man team we built an app that would select a user and display nearby businesses based on common search criteria like type and location. The storing and retrieval of information was done using PostgreSQL "
     "while the GUI was built in C#. During this project I also learned about database design theory.\n")
Cplus=("Aa a Teaching Assistant teaching data structures in C++ at WSU, I was responsible for giving a more personal touch to teaching. Not only did I run a lab section and graded exams I also mentored my students. "
       "While teaching I learned how to be an inspiration to my students and to meet classroom goals in a timely manner.\n")
Csharpe=("After completing the intro programming classes I applied those skills learned to produce games in Unity with C#. After several projects, I gained proficiency in setting project milestones, "
       
"searching for solutions and user design. I also learned the importance of perseverance and resolving problems.\n")

python=("For a personal project I wrote python code to scrape LinkedIn jobs. I accomplished this by using automated testing software called Selenium since "
        "you cannot grab the HTML using common web scrappers like Beautiful Soup. I also have done visualizations with MATLAB and NumPy, used PyEDA for electronic design automation and natural language processing with spaCy"
        ".\n")

multithreading=("As a test of my understanding of Parallel Programming I built a multithreaded pseudo-random number generator. Each thread would calculate a portion of "
                
"the number sequence which would then be combined using an All to All. I also got this system to work in a distributed system where each node was treated as a separate computer.\n")
communicationSkills=("I managed four other programmers as we used the AGILE process to develop an Android App that would retrieve recipes based on what ingredients the user put in. "
                    
"As the project lead, I scheduled meetings, assigned jobs, and guided teammates\n")
tensorflow=("Using TensorFlow and some of their sample data I constructed a classifier to distinguish between dogs and cats. I then set about messing with the learning rate and model type"
            "to see if the accuracy could be further improved. While I could not make a statistically significant change I do have a good basic understanding of TensorFlow.\n")
NLP=("Using spaCy and Python I pulled names from text. I started using the preloaded training model but found it insufficient for my work. I then added more training data and fiddled with the learning rates to get a more accurate result. \n")
machinelearning = ("Using WEKA and loan data provided by Kaggle I predicted the rating an individual got for a loan based on features like amount, income, homeownership. "
                  
"I tested several models like Multilayer Perceptron and J48 decision trees and ultimately got the accuracy to 98.8% on the testing set.\n")
git=("As part of club activities I was a member of a team that volunteered to create visualizations for air pollution. Using publicly available data and R on the back end with CSS on the front we built the app. "
     "To keep the project under control we used GitHub and AGILE development principles.\n")


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
                    #print(element)
                skills.append(element.replace('"',''))

        #print(companyName)
        #print(jobTitle)
        #print(language)
        #print(skills)
        try:
            if language[0]=="":
                #print("not enough skills")
                continue
            topics.append(language[0].strip())
            topics.append(skills[0].strip())
            topics.append(skills[1].strip())
            
            print(topics)
        except:
            #print("not enough skills")
            continue
        
        file = open(companyName +"_CoverLetter.txt","w")
        file.write("24848 SE Mirromont Way\n")
        file.write("Issaquah, Washington 98027\n")
        #file.write("425-736-7325\n")
        file.write(datetime.datetime.today().strftime("%m/%d/%Y")+"\n")
        file.write("agathyrsi1024@gmail.com\n")
        
        file.write("\n")
        file.write(companyName+"\n")
        file.write(location+"\n")
        file.write("\n")
        if(contact != ""):
            file.write("Dear "+contact+",\n")
        else:
            file.write("Dear "+companyName+" team,\n")
        file.write("\n")
        file.write("I would like to introduce myself as a WSU Computer Science major graduating in December with an emphasis on Data Science. ")
        file.write("I am excited to be applying for the "  + jobTitle + " position at " +companyName+" which I found on LinkedIn. ")
        file.write("As someone who is highly focused and attentive to detail, I thrive on building quality systems that surpass end-users' expectations. ")
        file.write("I am thrilled at the opportunity to show off my technical expertise and leadership skills as part of " +companyName+"'s expert team. ")
        
        file.write("\n")
        file.write("\n")
        for x in topics:
            #print(x)
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
        #file.write("This cover letter was auto generated. ")
        file.write("I am looking forward to learning more details about the " + jobTitle + " position at " +companyName+". ")
        file.write("As we move further through the hiring process I am eager to demonstrate my commitment to developing world-class software solutions for " +companyName+". \n")
        
        file.write("\n")
        file.write("Sincerely,\n")
        file.write("\n")
        file.write("Gordon Duncan")
        file.close()    
