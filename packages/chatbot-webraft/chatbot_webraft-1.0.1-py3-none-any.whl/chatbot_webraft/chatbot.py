# Library Created By Webraft on 9/2/22
import csv
import ast
import textwrap
import os.path
import difflib
import os.path
import random

def create_model(name):
    global model_name
    model_name = name


def importerror(filename,cmd):
    if os.path.exists(filename):
        return
    else:
        print("Error 3: No File Found with Name ",filename," in ",cmd)
        exit()


def nameerror(name,FUNCTION):
    global model_name
    if model_name == name:
        return
    else:
        print("Error 1: Model ",name, " NOT Found in ",FUNCTION)
        exit()


def dataset(filepath, input, label, model):
    global model_name
    nameerror(model,"chatbot.dataset()")
    importerror(filepath, "chatbot.dataset()")
    filename = open(filepath, 'r')
    file = csv.DictReader(filename)
    global words_list1
    global words_list2
    words_list1 = []
    words_list2 = []
    # creating dictreader object
    for col in file:
        words_list1.append(col[input])
        words_list2.append(col[label])
    for i in range(len(words_list1)):
        words_list1[i] = words_list1[i].lower()
    for i in range(len(words_list2)):
        words_list2[i] = words_list2[i].lower()

def add_data(model, input, label):
    global words_list1
    global words_list2
    nameerror(model,"chatbot.add_data()")
    words_list1.append(input)
    words_list2.append(label)


def spim(word, model,words_list1,words_list2):

    nameerror(model,"chatbot.model_run")

    closest_index = -1
    closest_distance = float("inf")
    for i, w in enumerate(words_list1):
        distance = abs(len(word) - len(w))
        if distance < closest_distance:
            closest_index = i
            closest_distance = distance
    return words_list2[closest_index]
def spimx3(word,model,words_list1,words_list2):
    import re
    import nltk
    import random
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer

    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    def preprocess_text(text):
        # Convert to lowercase

        # Remove special characters and numbers
        text = re.sub(r'[^a-z]+', ' ', text)
        # Tokenize the text
        words = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        # Stem the words
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        return words

    def load_data(words_list1, words_list2):
        input_data = words_list1
        label_data = words_list2
        return input_data, label_data

    def get_similarity(word, words_list):
        # Preprocess the input word
        word = preprocess_text(word)
        # Initialize a list to store the similarity scores
        similarity_scores = []
        # Iterate through each word in the words list
        for w in words_list:
            # Preprocess the word in the words list
            w_processed = preprocess_text(w)
            # Calculate the similarity score between the two words
            if len(set(w_processed).union(set(word))) == 0:
                score = random.randint(0, 20)
            else:
                score = len(set(word).intersection(w_processed)) / len(set(w_processed).union(set(word)))
            similarity_scores.append(score)
        # Return the index of the most similar word
        return similarity_scores.index(max(similarity_scores))

    # Load the data from the CSV file
    input_data, label_data = load_data(words_list1, words_list2)

    # Get the user input
    input_word = word

    # Find the index of the most similar word in the input data
    index = get_similarity(input_word, input_data)

    # Output the corresponding label from the label data
    return label_data[index]


def spimx2(word,model,words_list1,words_list2):
    import re
    import nltk
    import random
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer

    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    def preprocess_text(text):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-z]+', ' ', text)
        # Tokenize the text
        words = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        # Stem the words
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        return words

    def load_data(words_list1, words_list2):
        input_data = words_list1
        label_data = words_list2
        return input_data, label_data

    def get_similarity(word, words_list):
        # Preprocess the input word
        word = preprocess_text(word)
        # Initialize a list to store the similarity scores
        similarity_scores = []
        # Iterate through each word in the words list
        for w in words_list:
            # Preprocess the word in the words list
            w_processed = preprocess_text(w)
            # Calculate the similarity score between the two words
            if len(set(w_processed).union(set(word))) == 0:
                score = random.randint(0, 20)
            else:
                score = len(set(word).intersection(w_processed)) / len(set(w_processed).union(set(word)))
            similarity_scores.append(score)
        # Return the index of the most similar word
        return similarity_scores.index(max(similarity_scores))

    # Load the data from the CSV file
    input_data, label_data = load_data(words_list1, words_list2)

    # Get the user input
    input_word = word

    # Find the index of the most similar word in the input data
    index = get_similarity(input_word, input_data)

    # Output the corresponding label from the label data
    return label_data[index]


def spimx(word,model,words_list1,words_list2):
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    nltk.download('stopwords',quiet=True)
    nltk.download('punkt',quiet=True)

    def preprocess_text(text):
            # Convert to lowercase
        text = text.lower()
            # Remove special characters and numbers
        text = re.sub(r'[^a-z]+', ' ', text)
            # Tokenize the text
        words = word_tokenize(text)
            # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
            # Stem the words
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        return words

    def load_data(words_list1, words_list2):
            # Open the CSV file

        input_data = words_list1
        label_data = words_list2
            # Iterate through each row

        return input_data, label_data

    def get_similarity(word, words_list):
            # Preprocess the input word
         word = preprocess_text(word)
            # Initialize a list to store the similarity scores
         similarity_scores = []
            # Iterate through each word in the words list
         for w in words_list:
                # Preprocess the word in the words list
             w_processed = preprocess_text(w)
                # Calculate the similarity score between the two words
             if len(set(w_processed).union(w)) == 0:
                 score = random.randint(0, 20)
             else:
                 score = len(set(word).intersection(w_processed)) / len(set(word).union(w_processed))

             similarity_scores.append(score)
            # Return the index of the most similar word
         return similarity_scores.index(max(similarity_scores))

            # Load the data from the CSV file

    input_data, label_data = load_data(words_list1, words_list2)
        # Get the user input
    input_word = word
        # Find the index of the most similar word in the input data
    index = get_similarity(input_word, input_data)
        # Output the corresponding label from the label data
    return label_data[index]

def spimx4(word,model,words_list1,words_list2):
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    nltk.download('stopwords',quiet=True)
    nltk.download('punkt',quiet=True)

    def preprocess_text(text):
            # Convert to lowercase

            # Remove special characters and numbers
        text = re.sub(r'[^a-z]+', ' ', text)
            # Tokenize the text
        words = word_tokenize(text)
            # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
            # Stem the words
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        return words

    def load_data(words_list1, words_list2):
        # Preprocess input data
        input_data = [preprocess_text(text) for text in words_list1]
        # Preprocess label data
        label_data = [preprocess_text(text) for text in words_list2]
        return input_data, label_data

    def get_similarity(word, words_list):
            # Preprocess the input word
        word = ' '.join(word)

        word = preprocess_text(word)[0]
            # Initialize a list to store the similarity scores
        similarity_scores = []
            # Iterate through each word in the words list
        for w in words_list:
                # Preprocess the word in the words list
            w_processed = w
                # Calculate the similarity score between the two words
            if len(set(w_processed).union(w)) == 0:
               score = random.randint(0, 20)
            else:
               score = len(set(word).intersection(w_processed)) / len(set(word).union(w_processed))

            similarity_scores.append(score)
            # Return the index of the most similar word
        return similarity_scores.index(max(similarity_scores))

            # Load the data from the CSV file

    input_data, label_data = load_data(words_list1, words_list2)
        # Get the user input
    input_word = word
        # Find the index of the most similar word in the input data
    index = get_similarity(input_word, input_data)
        # Output the corresponding label from the label data
    return label_data[index]

def rasv(word,model,words_list1,words_list2,thresold=0.6,logic=False,logicmsg="Sorry , I dont know that"):
    def get_similar_word2(input_word, words_list):
        match = difflib.get_close_matches(input_word, words_list, n=1, cutoff=thresold)
        if match:
            return match[0]
        else:
            return None

    def get_answer(input_word, words_list1, words_list2):
        similar_word = get_similar_word2(input_word, words_list1)
        if similar_word:
            index = words_list1.index(similar_word)
            return words_list2[index]
        else:
            if logic == False:
                closest_index = -1
                closest_distance = float("inf")
                for i, w in enumerate(words_list1):
                    distance = abs(len(word) - len(w))
                    if distance < closest_distance:
                        closest_index = i
                        closest_distance = distance
                return words_list2[closest_index]
            else:
                return logicmsg
            #from googlesearch import search
            #import requests
            #from bs4 import BeautifulSoup

            # Take input from user

            #query = input_word
            # Search for the query on Google and get the first website
            #search_results = search(query)
            #first_website = next(iter(search_results))

            # Request the first website's content and parse it using BeautifulSoup
            #response = requests.get(first_website)
            #soup = BeautifulSoup(response.content, "html.parser")

            # Extract the first four lines of text from the website's content (without HTML tags)
            #text_lines = []
            #for p_tag in soup.find_all('\n'):
             #   stripped_line = p_tag.get_text().strip()
              #  if stripped_line:
               #     text_lines.append(stripped_line)
                #    if len(text_lines) == 50:
                 #       break

            # Print the first four lines of text (without HTML tags)
           # a = "\n".join(text_lines)
            #return a




    return get_answer(word, words_list1, words_list2)
def bert(word,model,words_list1,words_list2):
    from sentence_transformers import SentenceTransformer, util

    # Load the pre-trained BERT model
    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    # Define your sentences
    sentences = words_list1

    # Encode the sentences into sentence embeddings
    sentence_embeddings = model.encode(sentences)

    # Define your user input
    user_input = word

    # Encode the user input into a sentence embedding
    user_embedding = model.encode(user_input)

    # Calculate the cosine similarity between the user input embedding and the sentence embeddings
    similarity_scores = util.pytorch_cos_sim(user_embedding, sentence_embeddings)

    # Find the index of the most similar sentence
    most_similar_sentence_index = similarity_scores.argmax().item()

    # Print the index of the most similar sentence
    return words_list2[most_similar_sentence_index]

def spimxr(word,model,words_list1,words_list2):
    closest_indices = [-1, -1]
    closest_distances = [float("inf"), float("inf")]
    for i, w in enumerate(words_list1):
        distance = abs(len(word) - len(w))
        if distance < closest_distances[0]:
            closest_indices[1] = closest_indices[0]
            closest_distances[1] = closest_distances[0]
            closest_indices[0] = i
            closest_distances[0] = distance
        elif distance < closest_distances[1]:
            closest_indices[1] = i
            closest_distances[1] = distance
    return words_list2[closest_indices[0]], words_list2[closest_indices[1]]
def mask(prompt,answer,list1,list2):
    #filename = open(maskdataset1, 'r')
    #file = csv.DictReader(filename)
    global mask_list1
    global mask_list2
    mask_list1 = list1
    mask_list2 = list2
    # creating dictreader object
    #for col in file:
        #mask_list1.append(col["mask"])
        #mask_list2.append(col["return"])
    #for i in range(len(mask_list1)):
       # mask_list1[i] = mask_list1[i].lower()
    #for i in range(len(mask_list2)):
        #mask_list2[i] = mask_list2[i].lower()

    def find_word_replace_sentence(list1, list2, sentence, prompt):
        """
        This function takes in two lists and a sentence, and replaces any instance of "[mask]"
        in the sentence with the word from list2 at the same index as the word in list1 that matches
        the given prompt. It then returns the modified sentence.
        """
        # Find the index of the first word in list1 that matches the given prompt
        for i, word in enumerate(list1):
            if word in prompt:
                index = i
                break
        else:
            # If no word in list1 matches the given prompt, return the original sentence
            return sentence

        # Use the index to get the word from list2
        word_to_replace = list2[index]

        # Replace any instance of "[mask]" in the sentence with the word from list2
        new_sentence = sentence.replace("[mask]", word_to_replace)

        # Return the modified sentence
        return new_sentence

    return  find_word_replace_sentence(list1, list2, answer, prompt)
def masker(word,model,words_list1,words_list2,masklist1,masklist2):
    def get_similar_word2(input_word, words_list):
        match = difflib.get_close_matches(input_word, words_list, n=1, cutoff=0.6)
        if match:
            return match[0]
        else:
            return None

    def get_answer(input_word, words_list1, words_list2):
        similar_word = get_similar_word2(input_word, words_list1)
        if similar_word:
            index = words_list1.index(similar_word)
            return mask(word,words_list2[index],masklist1,masklist2)
        else:
            closest_index = -1
            closest_distance = float("inf")
            for i, w in enumerate(words_list1):
                distance = abs(len(word) - len(w))
                if distance < closest_distance:
                    closest_index = i
                    closest_distance = distance
            return mask(word, words_list2[closest_index], masklist1, masklist2)
def load_file_as_function(file_path):
    # Open the file for reading
    importerror(file_path, "model_load()")
    with open(file_path, 'r') as file:
        # Read the contents of the file
        file_contents = file.read()

    # Define a function with the contents of the file as its body

    exec(f'def loaded_function(word,wordslist1,wordslist2):\n{textwrap.indent(file_contents, "    ")}', locals())

    # Return the newly defined function
    return locals()['loaded_function']
def generate_pycode(text):
    text = text.lower()
    lines = text.strip().split('.')
    code = ""
    indent_level = 0
    for line in lines:
        if "define function" in line:
            # generate function definition
            parts = line.split("function")[1].strip().split("taking")
            function_name = parts[0].strip()
            args = parts[1].strip().split(",")
            args = [arg.strip() for arg in args]
            args = ", ".join(args)
            code = f"{' ' * 4 * indent_level}def {function_name}({args}):\n"
            indent_level += 1
        elif "print" in line:
            # generate print statement
            code +=" " * 4 * indent_level + "print(" + line.split("print")[1].strip() + ")\n"
        elif "define" in line:
            # generate variable definition
            parts = line.split("define")[1].strip().split("as")
            variable_name = parts[0].strip()
            variable_value = parts[1].strip()
            if "input" in variable_value:
                variable_value2 = "input(" + variable_value.split("print")[1].strip() + ")"
                code += f"{' ' * 4 * indent_level}{variable_name} = {variable_value2}\n"
            else:
                code += f"{' ' * 4 * indent_level}{variable_name} = {variable_value}\n"
        elif "if" in line:
            # generate if statement
            if "is not" in line:
                parts = line.split("if")[1].strip().split("is not")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}if {variable_name} != {variable_value}\n"
                indent_level += 1
            elif "is" in line:
                parts = line.split("if")[1].strip().split("is")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}if {variable_name} == {variable_value}\n"
                indent_level += 1
            else:
                code += f"{' ' * 4 * indent_level}if {line.split('if')[1].strip()}:\n"
                indent_level += 1
        elif "else" in line:
            # generate else statement

            code += f"{' ' * 4 * indent_level}else:\n"
            indent_level += 1
        elif "otherwise" in line:
            # generate else statement

            code += f"{' ' * 4 * indent_level}else:\n"
            indent_level += 1
        elif "elif" in line:
            # generate elif statement
            if "is not" in line:

                parts = line.split("elif")[1].strip().split("is not")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}elif {variable_name} != {variable_value}\n"
                indent_level += 1
            elif "is" in line:

                parts = line.split("elif")[1].strip().split("is")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}elif {variable_name} == {variable_value}\n"
                indent_level += 1
            else:
                indent_level += 1
                code += f"{' ' * 4 * indent_level}elif {line.split('elif')[1].strip()}:\n"


        elif "also if" in line:
            # generate elif statement
            if "is not" in line:

                parts = line.split("also if")[1].strip().split("is not")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}elif {variable_name} != {variable_value}\n"
                indent_level += 1
            elif "is" in line:

                parts = line.split("also if")[1].strip().split("is")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}elif {variable_name} == {variable_value}\n"
                indent_level += 1
            else:

                code += f"{' ' * 4 * indent_level}elif {line.split('elif')[1].strip()}:\n"
                indent_level += 1
        elif "else if" in line:
            # generate elif statement
            if "is not" in line:

                parts = line.split("else if")[1].strip().split("is not")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}elif {variable_name} != {variable_value}\n"
                indent_level += 1
            elif "is" in line:

                parts = line.split("else if")[1].strip().split("is")
                variable_name = parts[0].strip()
                variable_value = parts[1].strip()
                code += f"{' ' * 4 * indent_level}elif {variable_name} == {variable_value}\n"
                indent_level += 1
            else:

                code += f"{' ' * 4 * indent_level}elif {line.split('elif')[1].strip()}:\n"
                indent_level += 1
        elif "end" in line:
            # end if/else statement
            indent_level -= 1
        elif "for" in line:
            # generate for loop
            parts = line.split("for")[1].strip().split("in")
            variable_name = parts[0].strip()
            iterable = parts[1].strip()
            code = f"{' ' * 4 * indent_level}for {variable_name} in {iterable}:\n"
            indent_level += 1
        elif "while" in line:
            # generate while loop
            code += f"{' ' * 4 * indent_level}while {line.split('while')[1].strip()}:\n"
            indent_level += 1
        elif "break" in line:
            # generate break statement
            code += f"{' ' * 4 * indent_level}break\n"
        elif "continue" in line:
            # generate continue statement
            code += f"{' ' * 4 * indent_level}continue\n"
        elif "pass" in line:
            # generate pass statement
            code += f"{' ' * 4 * indent_level}pass\n"
        elif "function" in line:
            # generate function definition
            parts = line.split("function")[1].strip().split("taking")
            function_name = parts[0].strip()
            args = parts[1].strip().split(",")
            args = [arg.strip() for arg in args]
            args = ", ".join(args)
            code += f"{' ' * 4 * indent_level}def {function_name}({args}):\n"
            indent_level += 1
        elif "return" in line:
            # generate return statement
            code += f"{' ' * 4 * indent_level}return {line.split('return')[1].strip()}\n"
        else:
            code += "Error 2: Writer unable to convert this text to code."
    return code
def generate_phpcode(text):
    text = text.lower()
    lines = text.strip().split(".")
    code = ""
    indent_level = 0
    for line in lines:
        if "print" in line:
            # generate print statement
            code += " " * 4 * indent_level + "echo " + line.split("print")[1].strip() + ";\n"
        elif "define" in line:
            # generate variable definition
            parts = line.split("define")[1].strip().split("as")
            variable_name = parts[0].strip()
            variable_value = parts[1].strip()
            if "input" in variable_value:
                variable_value = "$" + variable_name + " = readline();\n"
                code += f"{' ' * 4 * indent_level}{variable_value}"
            else:
                variable_value = "$" + variable_name + " = " + variable_value + ";\n"
                code += f"{' ' * 4 * indent_level}{variable_value}"
        elif "if" in line:
            # generate if statement
            code += f"{' ' * 4 * indent_level}if ({line.split('if')[1].strip()}) {{\n"
            indent_level += 1
        elif "else" in line:
            # generate else statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}}} else {{\n"
            indent_level += 1
        elif "elif" in line:
            # generate elif statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}}} elseif ({line.split('elif')[1].strip()}) {{\n"
            indent_level += 1
        elif "end" in line:
            # end if/else statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}}}\n"
        elif "for" in line:
            # generate for loop
            code += f"{' ' * 4 * indent_level}for ({line.split('for')[1].strip()}) {{\n"
            indent_level += 1
        elif "while" in line:
            # generate while loop
            code += f"{' ' * 4 * indent_level}while ({line.split('while')[1].strip()}) {{\n"
            indent_level += 1
        elif "break" in line:
            # generate break statement
            code += f"{' ' * 4 * indent_level}break;\n"
        elif "continue" in line:
            # generate continue statement
            code += f"{' ' * 4 * indent_level}continue;\n"
        elif "pass" in line:
            # generate pass statement
            code += f"{' ' * 4 * indent_level}\n"
        elif "function" in line:
            # generate function definition
            parts = line.split("function")[1].strip().split("taking")
            function_name = parts[0].strip()
            args = parts[1].strip().split(",")
            args = [arg.strip() for arg in args]
            args = ", ".join(args)
            code += f"{' ' * 4 * indent_level}function {function_name}({args})\n"
            indent_level += 1
        elif "return" in line:
            # generate return statement
            code += f"{' ' * 4 * indent_level}return {line.split('return')[1].strip()};\n"
        else:
            code += "Error 2: Writer unable to convert this text to code."
    return code
def generate_js_code(text):
    text = text.lower()
    lines = text.strip().split(".")
    code = ""
    indent_level = 0
    for line in lines:
        if "console.log" in line:
            # generate console.log statement
            code += " " * 4 * indent_level + "console.log(" + line.split("console.log")[1].strip() + ");\n"
        elif "var" in line:
            # generate variable definition
            parts = line.split("var")[1].strip().split("=")
            variable_name = parts[0].strip()
            variable_value = parts[1].strip()
            if "prompt" in variable_value:
                variable_value2 = "prompt(" + variable_value.split("prompt")[1].strip() + ")"
                code += f"{' ' * 4 * indent_level}var {variable_name} = {variable_value2};\n"
            else:
                code += f"{' ' * 4 * indent_level}var {variable_name} = {variable_value};\n"
        elif "if" in line:
            # generate if statement
            code += f"{' ' * 4 * indent_level}if ({line.split('if')[1].strip()}) {{\n"
            indent_level += 1
        elif "else" in line:
            # generate else statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}}} else {{\n"
            indent_level += 1
        elif "elif" in line:
            # generate else if statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}}} else if ({line.split('elif')[1].strip()}) {{\n"
            indent_level += 1
        elif "end" in line:
            # end if/else statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}}}\n"
        elif "for" in line:
            # generate for loop
            parts = line.split("for")[1].strip().split(";")
            init = parts[0].strip()
            condition = parts[1].strip()
            increment = parts[2].strip()
            code += f"{' ' * 4 * indent_level}for ({init}; {condition}; {increment}) {{\n"
            indent_level += 1
        elif "while" in line:
            # generate while loop
            code += f"{' ' * 4 * indent_level}while ({line.split('while')[1].strip()}) {{\n"
            indent_level += 1
        elif "break" in line:
            # generate break statement
            code += f"{' ' * 4 * indent_level}break;\n"
        elif "continue" in line:
            # generate continue statement
            code += f"{' ' * 4 * indent_level}continue;\n"
        else:
            code += "Error 2: Writer unable to convert this text to code."
    return code
def pywriter(text,filepath,input,label):
    filename = open(filepath, 'r')
    file = csv.DictReader(filename)
    global py_list1
    global py_list2
    py_list1 = []
    py_list2= []
    # creating dictreader object
    for col in file:
        py_list1.append(col[input])
        py_list2.append(col[label])
    closest_index = -1
    closest_distance = float("inf")
    for i, w in enumerate(py_list1):
        distance = abs(len(text) - len(w))
        if distance < closest_distance:
            closest_index = i
            closest_distance = distance
        x = py_list2[closest_index]
    return generate_pycode(x)
def codewriter(language,text,model):
    nameerror(model,"codewriter()")
    if language=="python":
        code = generate_pycode(text) # pywriter(text,"code.csv","in","out")
        return code
    elif language=="php":
        code = generate_phpcode(text)
        return code
    elif language=="js":
        code = generate_js_code(text)
        return code
    else:
        return "Language not supported"

def modeltype_load(modelfile,word,wordslist1,wordslist2):
    global words_list1
    global words_list2

    loaded_func = load_file_as_function(modelfile)
    return loaded_func(word,wordslist1,wordslist2)

def nlpm(word,model,words_list1,words_list2,modelname):
    def rephrase_sentence(sentence, synonyms):
        # Split the sentence into words
        words = sentence.split()

        # Loop through each word in the sentence
        new_words = []
        for word in words:
            # If the word has a synonym in the dictionary, replace it with a random synonym from the selected list
            if word in synonyms:
                synonym_list = synonyms[word]
                new_word = random.choice(synonym_list)
            # Otherwise, keep the original word
            else:
                new_word = word
            new_words.append(new_word)

        # Join the new words into a rephrased sentence
        return ' '.join(new_words)

    # Define lists of custom synonyms for each word
    #happy_synonyms = ['glad', 'joyful', 'elated']
    #angry_synonyms = ['upset', 'mad', 'irate']
    #run_synonyms = ['jog', 'sprint', 'dash']
    #big_synonyms = ['large', 'huge', 'enormous']
    #small_synonyms = ['tiny', 'micro', 'microscopic']
    #hot_synonyms = ['warm', 'toasty', 'boiling']
    #good_synonyms = ['great', 'excellent', 'superb']
    #bad_synonyms = ['terrible', 'awful', 'dreadful']
    #beautiful_synonyms = ['gorgeous', 'stunning', 'elegant']
    happy_synonyms = ['glad', 'joyful', 'elated', 'pleased', 'content', 'cheerful', 'ecstatic', 'overjoyed', 'thrilled','delighted', 'satisfied']
    angry_synonyms = ['upset', 'mad', 'irate', 'furious', 'enraged', 'incensed', 'outraged', 'livid', 'exasperated','aggravated', 'infuriated']
    run_synonyms = ['jog', 'sprint', 'dash', 'gallop', 'jogging', 'trot', 'race', 'jogged', 'running', 'sprinted', 'dashing']
    big_synonyms = ['large', 'huge', 'enormous', 'gigantic', 'massive', 'colossal', 'vast', 'immense', 'monstrous', 'tremendous', 'substantial']
    small_synonyms = ['tiny', 'minuscule', 'microscopic', 'miniature', 'little', 'diminutive', 'petite', 'pocket-sized',
                      'dinky', 'wee', 'puny']
    hot_synonyms = ['warm', 'toasty', 'boiling', 'scorching', 'sweltering', 'blistering', 'roasting', 'sizzling',
                    'burning', 'fiery', 'heated']
    good_synonyms = ['great', 'excellent', 'superb', 'wonderful', 'fantastic', 'terrific', 'splendid', 'amazing',
                     'marvelous', 'outstanding', 'exceptional']
    bad_synonyms = ['terrible', 'awful', 'dreadful', 'horrible', 'atrocious', 'abysmal', 'miserable', 'lousy', 'poor',
                    'unsatisfactory', 'inferior']
    beautiful_synonyms = ['gorgeous', 'stunning', 'elegant', 'lovely', 'pretty', 'charming', 'attractive', 'alluring','fascinating', 'exquisite', 'radiant']
    algorithm_synonyms = ['procedure', 'method', 'computation', 'logic', 'program', 'calculation', 'formula', 'process','heuristic', 'routine', 'rule']
    protocol_synonyms = ['guideline', 'standard', 'convention', 'procedure', 'practice', 'code', 'regulation', 'policy', 'instruction', 'custom', 'norm']
    encryption_synonyms = ['encoding', 'ciphering', 'scrambling', 'codification', 'obfuscation', 'concealment', 'secret writing', 'security', 'protection', 'cryptography']
    decryption_synonyms = ['decoding', 'deciphering', 'unscrambling', 'decodification', 'clarification','disentanglement', 'solving', 'decipherment', 'solution', 'decrypting']
    debugging_synonyms = ['troubleshooting', 'problem-solving', 'diagnosis', 'debug', 'de-bugging', 'fault-finding','bug-hunting', 'investigation', 'testing', 'maintenance']
    automation_synonyms = ['mechanization', 'computerization', 'robotics', 'industrialization', 'modernization','efficiency', 'streamlining', 'optimization', 'autonomation', 'artificial intelligence']
    virtualization_synonyms = ['emulation', 'simulation', 'abstraction', 'virtual reality', 'virtualisation']
    hope = ['optimism', 'aspiration', 'confidence']
    despair=[ 'hopelessness', 'discouragement', 'resignation']
    envy=  ['jealousy', 'covetousness', 'resentment']
    surprise = [ 'astonishment', 'amazement', 'shock']
    disgust= [ 'revulsion', 'repugnance', 'loathing']
    curiosity= [ 'inquisitiveness', 'fascination', 'exploration']
    compassion= [ 'empathy', 'kindness', 'sympathy']
    aggression= [ 'hostility', 'violence', 'belligerence']
    trust= [ 'believe', 'faith']
    doubt= [ 'uncertainty', 'skepticism', 'hesitation']
    # Combine the synonym lists into a dictionary
    fast = ['quick', 'speedy', 'swift', 'rapid', 'expeditious']
    slow = ['leisurely', 'unhurried', 'gradual', 'plodding', 'sluggish']
    loud= ['noisy', 'boisterous', 'raucous', 'clamorous', 'vociferous']
    quiet = ['silent', 'peaceful', 'serene', 'tranquil', 'calm']
    rich = ['wealthy', 'affluent', 'prosperous', 'well-off', 'loaded']
    poor = ['impoverished', 'destitute', 'needy', 'broke', 'penniless']
    old = ['ancient', 'elderly', 'senior', 'venerable', 'aged']
    young = ['youthful', 'juvenile', 'adolescent', 'teenage', 'inexperienced']
    tall = ['high', 'towering', 'lofty', 'elevated', 'statuesque']
    short = ['brief', 'concise', 'succinct', 'abridged', 'curtailed']
    wide = ['broad', 'spacious', 'vast', 'extensive', 'expansive']
    narrow = ['cramped', 'confined', 'tight', 'limited', 'constricted']
    sadness= [ 'dejected', 'miserable', 'crestfallen']
    fear= [' scared', 'terrified', 'panicky']
    excitement= [ 'thrilled', 'ecstatic', 'pumped']
    confusion= [ 'puzzled', 'bewildered', 'perplexed']
    hate =['despise', 'detest', 'loathe']
    tiredness= [ 'exhausted', 'fatigued', 'weary']
    hunger= [ 'famished', 'ravenous', 'starving']
    thirst= [ 'parched', 'dehydrated', 'thirsty']
    sight= [ 'glimpse', 'glance', 'view']
    sound= [ 'noise', 'din', 'racket']
    smell= [ 'fragrance', 'aroma', 'scent']
    touch= [ 'feel', 'grasp', 'hold']
    taste= [ 'flavor', 'savor', 'relish']
    testing = ['verification', 'validation', 'quality assurance', 'trials', 'experimentation', 'assessment', 'inspection', 'checking', 'evaluation', 'analysis']
    database = ['data repository', 'information system', 'data storage', 'database management system', 'DBMS','data warehouse', 'data lake', 'data center']
    networking = ['communication', 'interconnectivity', 'inter-networking', 'telecommunications', 'internet','intranet', 'LAN', 'WAN', 'routing', 'switching']
    security = ['protection', 'safety', 'defense', 'safeguarding', 'fortification', 'guarding', 'prevention','security measures', 'risk management']
    cloud = ['cloud computing', 'cloud services', 'cloud storage', 'cloud-based', 'cloud infrastructure', 'cloud platform', 'cloud computing technology']
    machine_learning = ['ML', 'artificial intelligence', 'AI', 'neural networks', 'deep learning', 'supervised learning', 'unsupervised learning', 'reinforcement learning']
    data_science = ['big data', 'data analytics', 'data mining', 'machine learning', 'artificial intelligence','statistics', 'visualization', 'data modeling']
    web_development = ['web design', 'front-end development', 'back-end development', 'full-stack development','website creation', 'web application development']
    mobile_development = ['mobile app development', 'iOS app development', 'Android app development','cross-platform development', 'native app development']
    UI = ['user interface', 'UI design', 'interface design', 'user experience', 'UX design','graphical user interface', 'GUI']
    UX = ['user experience', 'UX design', 'user-centered design', 'interaction design', 'user interface','UI design']
    AI = ['artificial intelligence', 'machine intelligence', 'automation', 'robotics', 'expert system', 'neural network', 'deep learning', 'computer intelligence', 'cognitive computing']
    data = ['information', 'facts', 'statistics', 'figures', 'details', 'records', 'data points', 'metrics', 'intelligence']
    network = ['networking', 'interconnectivity', 'communication', 'connectivity', 'links', 'interoperability','data exchange', 'collaboration']
    software = ['program', 'application', 'code', 'app', 'script', 'software package', 'system', 'platform', 'suite', 'tool']
    hardware = ['computer equipment', 'machinery', 'devices', 'apparatus', 'gear', 'tools', 'instruments', 'components', 'peripherals', 'electronics']
    ugly = ['unattractive', 'unsightly', 'repulsive', 'hideous', 'grotesque', 'disgusting', 'unappealing','deformed', 'monstrous', 'foul', 'vile']
    happy2 = ['blissful', 'upbeat', 'jubilant', 'gleeful', 'merry', 'sanguine', 'exultant', 'contented', 'gratified', 'pleasurable', 'thriving']
    sad = ['miserable', 'sorrowful', 'downcast', 'heartbroken', 'despondent', 'dejected', 'disheartened', 'blue', 'unhappy', 'gloomy', 'melancholy']
    laugh = ['giggle', 'chuckle', 'snicker', 'cackle', 'roar', 'snort', 'chortle', 'laughing', 'guffaw','hearty', 'hilarious']
    cry = ['weep', 'sob', 'whimper', 'sniffle', 'blubber', 'tear', 'wail', 'bawl', 'lament', 'mourn', 'sorrow']
    vps = ['virtual private server', 'cloud server', 'hosting server', 'remote server']
    node = ['computing node', 'node', 'server node', 'workstation','server']
    synonyms = {
        'server':node,
        'hosting server':vps,
        'node':node,
        'virtual private server':vps,
        'cloud server':vps,
        'vps':vps,
        'sorrow':cry,
        'communication':network,
        'blissful':happy2,
        'unhappy':sad,
        'disheartened':sad,
        'repulsive':ugly,
        'electronics':hardware,
        'devices':hardware,
        'sob':cry,
        'tear':cry,
        'giggle':laugh,
        'ugly':ugly,
        'sad':sad,
        'laugh':laugh,
        'cry':cry,
        'ai':AI,
        'artificial intelligence': AI,
        'data':data,
        'network':network,
        'software':software,
        'hardware':hardware,
        'security':security,
        'cloud':cloud,
        'machine learning':machine_learning,
        'data science':data_science,
        'web development':web_development,
        'mobile development':mobile_development,
        'ui': UI,
        'ux':UX,
        'testing':testing,
        'database':database,
        'tiredness':tiredness,
        'networking':networking,
        'hunger':hunger,
        'thirst':thirst,
        'sight':sight,
        'sound':sound,
        'smell':smell,
        'touch':touch,
        'sadness':sadness,
        'taste':taste,
        'fear':fear,
        'excitement':excitement,
        'confusion':confusion,
        'hate':hate,
        'fast':fast,
        'slow':slow,
        'loud':loud,
        'quiet':quiet,
        'rich':rich,
        'poor':poor,
        'old':old,
        'young':young,
        'tall':tall,
        'short':short,
        'wide':wide,
        'narrow':narrow,
        'despair':despair,
        'envy':envy,
        'surprise':surprise,
        'disgust':disgust,
        'curiosity':curiosity,
        'compassion':compassion,
        'aggression':aggression,
        'trust':trust,
        'doubt':doubt,
        'happy': happy_synonyms,
        'angry': angry_synonyms,
        'run': run_synonyms,
        'big': big_synonyms,
        'small': small_synonyms,
        'hot': hot_synonyms,
        'good': good_synonyms,
        'bad': bad_synonyms,
        'beautiful': beautiful_synonyms,
        'algorithm':algorithm_synonyms,
        'protocol':protocol_synonyms,
        'encryption':encryption_synonyms,
        'decryption':decryption_synonyms,
        'debug':debugging_synonyms,
        'debugging':debugging_synonyms,
        'automation':automation_synonyms,
        'automate':automation_synonyms,
        'virtualization':virtualization_synonyms,
        'glad':happy_synonyms,
        'joyful':happy_synonyms,
        'cheerful':happy_synonyms,
        'mad':angry_synonyms,
        'upset':angry_synonyms,
        'warm':hot_synonyms,
        'toasty':hot_synonyms,
        'awful':bad_synonyms,
        'terrible':bad_synonyms,
        'horrible':bad_synonyms,
        'great':good_synonyms,
        'excellent':good_synonyms,
        'nice':good_synonyms,
        'wonderful':good_synonyms,
        'superb':good_synonyms,
        'fantastic':good_synonyms,
        'hope':hope
    }
    def run(modelname,word,model):
        x = model_load(modelname,word,model,modelname)
        output = rephrase_sentence(x, synonyms)
        return output
    return run(modelname,word,model)
def model_load(modeltype,input, model,modelname="rasv"):
    global words_list1
    global words_list2
    global model_name
    input = input.lower()
    nameerror(model,"chatbot.model_load()")
    if modeltype == "spim":
        return spim(input,model,words_list1,words_list2)
    elif modeltype == "spimx":
        return spimx(input, model, words_list1, words_list2)
    elif modeltype == "spimx2":
        return spimx2(input, model, words_list1, words_list2)
    elif modeltype == "spimx3":
        return spimx3(input, model, words_list1, words_list2)
    elif modeltype == "spimx4":
        return spimx4(input, model, words_list1, words_list2)
    elif modeltype == "bert":
        return bert(input, model, words_list1, words_list2)
    elif modeltype == "rasv":
        return rasv(input,model,words_list1,words_list2)
    elif modeltype == "spimxr":
        return spimxr(input,model,words_list1,words_list2)
    elif modeltype == "pywriter":
        return codewriter("python", input, model)
    elif modeltype == "phpwriter":
        return codewriter("php", input, model)
    elif modeltype == "jswriter":
        return codewriter("js", input, model)
    elif modeltype == "nlpm":
        return nlpm(input,model,words_list1,words_list2,modelname)
    else:
        print("Modeltype not found , looking in local directory....")
        return modeltype_load(modeltype,input,words_list1,words_list2)





