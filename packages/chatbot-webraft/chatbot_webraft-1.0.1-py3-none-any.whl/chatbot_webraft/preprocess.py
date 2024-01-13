from collections import Counter
import json
import csv

max_len = 25

def remove_punc(string):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in string:
        if char not in punctuations:
            no_punct = no_punct + char  # space is also a character
    return no_punct.lower()


pairs = []
# Open the CSV file for reading
with open('file.csv', 'r' ,errors='ignore') as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file)

    # Get the header row
    header = next(csv_reader)

    # Find the index of the 'input' and 'label' columns
    input_index = header.index('input')
    label_index = header.index('label')

    # Loop through each row in the CSV file
    for row in csv_reader:
        qa_pairs = []
        # Extract the text from the 'input' and 'label' columns at the same index
        input_text = row[input_index]
        label_text = row[label_index]
        first = remove_punc(input_text.strip())
        second = remove_punc(label_text.strip())
        qa_pairs.append(first.split()[:max_len])
        qa_pairs.append(second.split()[:max_len])
        pairs.append(qa_pairs)
        # Do something with the text

# print(pairs)
word_freq = Counter()
for pair in pairs:
    word_freq.update(pair[0])
    word_freq.update(pair[1])

min_word_freq = 1
words = [w for w in word_freq.keys() if word_freq[w] > min_word_freq]
word_map = {k: v + 1 for v, k in enumerate(words)}
word_map['<unk>'] = len(word_map) + 1
word_map['<start>'] = len(word_map) + 1
word_map['<end>'] = len(word_map) + 1
word_map['<pad>'] = 0

print("Total words are: {}".format(len(word_map)))

with open('WORDMAP_corpus.json', 'w') as j:
    json.dump(word_map, j)


def encode_question(words, word_map):
    enc_c = [word_map.get(word, word_map['<unk>']) for word in words] + [word_map['<pad>']] * (max_len - len(words))
    return enc_c


def encode_reply(words, word_map):
    enc_c = [word_map['<start>']] + [word_map.get(word, word_map['<unk>']) for word in words] + [word_map['<end>']] + [
        word_map['<pad>']] * (max_len - len(words))
    return enc_c


pairs_encoded = []
for pair in pairs:
    qus = encode_question(pair[0], word_map)
    ans = encode_reply(pair[1], word_map)
    pairs_encoded.append([qus, ans])

with open('pairs_encoded.json', 'w') as p:
    json.dump(pairs_encoded, p)
