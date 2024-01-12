#Import library
from chatbot import *

#set model name
model = "my-model"

#create modelsample2.csv
create_model(model)

#load CSV dataset , Mention input column (question) and label column (answer)
dataset("sample.csv","input","label",model)


#run in loop
while True:
 prompt = input("You: ")
 #run model and parse input
 print("Bot: ",model_load("rasv",prompt,model))