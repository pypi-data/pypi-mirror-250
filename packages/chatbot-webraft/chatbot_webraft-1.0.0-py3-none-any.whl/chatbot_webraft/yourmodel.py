# -*- coding: utf-8 -*-


from collections import Counter
import json
import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader
import torch.utils.data
import math
import torch.nn.functional as F
import csv

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

device = torch.device("auto" if torch.cuda.is_available() else "cpu")



def remove_punc(string):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in string:
        if char not in punctuations:
            no_punct = no_punct + char  # space is also a character
    return no_punct.lower()


def tokenize_text(text):
    tokens = tokenizer.tokenize(text)
    return tokens





"""pairs = []

with open(dataset_name, 'r', errors='ignore') as csv_file:
    csv_reader = csv.reader(csv_file)

    header = next(csv_reader)

    input_index = header.index(input_set)
    label_index = header.index(label_set)
    for row in csv_reader:
        qa_pairs = []
        try:
            input_text = row[input_index]
            label_text = row[label_index]
            first = input_text.strip()
            second = label_text.strip()
            qa_pairs.append(encode_question(first))
            qa_pairs.append(encode_reply(second))
            pairs.append(qa_pairs)
        except IndexError:
            print(f"Skipping row: {row}")
            continue

with open('pairs_encoded.json', 'w') as p:
    json.dump(pairs, p)
"""

# rev_word_map = {v: k for k, v in word_map.items()}
# ' '.join([rev_word_map[v] for v in pairs_encoded[1][0]])

"""class Dataset(Dataset):

    def __init__(self):
        self.pairs = pairs
        self.dataset_size = len(self.pairs)

    def __getitem__(self, i):
        question = torch.LongTensor(self.pairs[i][0])
        reply = torch.LongTensor(self.pairs[i][1])

        return question, reply

    def __len__(self):
        return self.dataset_size"""


"""train_loader = torch.utils.data.DataLoader(Dataset(),
                                           batch_size=batch_size,
                                           shuffle=True,
                                           pin_memory=True)"""


# question, reply = next(iter(train_loader))

def create_masks(question, reply_input, reply_target,device):
    def subsequent_mask(size):
        mask = torch.triu(torch.ones(size, size)).transpose(0, 1).type(dtype=torch.uint8)
        return mask.unsqueeze(0)

    question_mask = question != 0
    question_mask = question_mask.to(device)
    question_mask = question_mask.unsqueeze(1).unsqueeze(1)  # (batch_size, 1, 1, max_words)

    reply_input_mask = reply_input != 0
    reply_input_mask = reply_input_mask.unsqueeze(1)  # (batch_size, 1, max_words)
    reply_input_mask = reply_input_mask & subsequent_mask(reply_input.size(-1)).type_as(reply_input_mask.data)
    reply_input_mask = reply_input_mask.unsqueeze(1)  # (batch_size, 1, max_words, max_words)
    reply_target_mask = reply_target != 0  # (batch_size, max_words)

    return question_mask, reply_input_mask, reply_target_mask


class Embeddings(nn.Module):
    """
    Implements embeddings of the words and adds their positional encodings.
    """

    def __init__(self, vocab_size, d_model, max_len=160):
        super(Embeddings, self).__init__()
        self.d_model = d_model
        self.dropout = nn.Dropout(0.1)
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pe = self.create_positinal_encoding(max_len, self.d_model)
        self.dropout = nn.Dropout(0.1)

    def create_positinal_encoding(self, max_len, d_model):
        pe = torch.zeros(max_len, d_model).to(device)
        for pos in range(max_len):  # for each position of the word
            for i in range(0, d_model, 2):  # for each dimension of the each position
                pe[pos, i] = math.sin(pos / (10000 ** ((2 * i) / d_model)))
                pe[pos, i + 1] = math.cos(pos / (10000 ** ((2 * (i + 1)) / d_model)))
        pe = pe.unsqueeze(0)  # include the batch size
        return pe

    def forward(self, encoded_words):
        embedding = self.embed(encoded_words) * math.sqrt(self.d_model)
        embedding += self.pe[:,
                     :embedding.size(1)]  # pe will automatically be expanded with the same batch size as encoded_words
        embedding = self.dropout(embedding)
        return embedding


class MultiHeadAttention(nn.Module):

    def __init__(self, heads, d_model):
        super(MultiHeadAttention, self).__init__()
        assert d_model % heads == 0
        self.d_k = d_model // heads
        self.heads = heads
        self.dropout = nn.Dropout(0.1)
        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)
        self.concat = nn.Linear(d_model, d_model)

    def forward(self, query, key, value, mask):
        """
        query, key, value of shape: (batch_size, max_len, 512)
        mask of shape: (batch_size, 1, 1, max_words)
        """
        # (batch_size, max_len, 512)
        query = self.query(query)
        key = self.key(key)
        value = self.value(value)

        # (batch_size, max_len, 512) --> (batch_size, max_len, h, d_k) --> (batch_size, h, max_len, d_k)
        query = query.view(query.shape[0], -1, self.heads, self.d_k).permute(0, 2, 1, 3)
        key = key.view(key.shape[0], -1, self.heads, self.d_k).permute(0, 2, 1, 3)
        value = value.view(value.shape[0], -1, self.heads, self.d_k).permute(0, 2, 1, 3)

        # (batch_size, h, max_len, d_k) matmul (batch_size, h, d_k, max_len) --> (batch_size, h, max_len, max_len)
        scores = torch.matmul(query, key.permute(0, 1, 3, 2)) / math.sqrt(query.size(-1))
        scores = scores.masked_fill(mask == 0, -1e9)  # (batch_size, h, max_len, max_len)
        weights = F.softmax(scores, dim=-1)  # (batch_size, h, max_len, max_len)
        weights = self.dropout(weights)
        # (batch_size, h, max_len, max_len) matmul (batch_size, h, max_len, d_k) --> (batch_size, h, max_len, d_k)
        context = torch.matmul(weights, value)
        # (batch_size, h, max_len, d_k) --> (batch_size, max_len, h, d_k) --> (batch_size, max_len, h * d_k)
        context = context.permute(0, 2, 1, 3).contiguous().view(context.shape[0], -1, self.heads * self.d_k)
        # (batch_size, max_len, h * d_k)
        interacted = self.concat(context)
        return interacted


class FeedForward(nn.Module):

    def __init__(self, d_model, middle_dim=2048):
        super(FeedForward, self).__init__()

        self.fc1 = nn.Linear(d_model, middle_dim)
        self.fc2 = nn.Linear(middle_dim, d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        out = F.relu(self.fc1(x))
        out = self.fc2(self.dropout(out))
        return out


class EncoderLayer(nn.Module):

    def __init__(self, d_model, heads):
        super(EncoderLayer, self).__init__()
        self.layernorm = nn.LayerNorm(d_model)
        self.self_multihead = MultiHeadAttention(heads, d_model)
        self.feed_forward = FeedForward(d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, embeddings, mask):
        interacted = self.dropout(self.self_multihead(embeddings, embeddings, embeddings, mask))
        interacted = self.layernorm(interacted + embeddings)
        feed_forward_out = self.dropout(self.feed_forward(interacted))
        encoded = self.layernorm(feed_forward_out + interacted)
        return encoded


class DecoderLayer(nn.Module):

    def __init__(self, d_model, heads):
        super(DecoderLayer, self).__init__()
        self.layernorm = nn.LayerNorm(d_model)
        self.self_multihead = MultiHeadAttention(heads, d_model)
        self.src_multihead = MultiHeadAttention(heads, d_model)
        self.feed_forward = FeedForward(d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, embeddings, encoded, src_mask, target_mask):
        query = self.dropout(self.self_multihead(embeddings, embeddings, embeddings, target_mask))
        query = self.layernorm(query + embeddings)
        interacted = self.dropout(self.src_multihead(query, encoded, encoded, src_mask))
        interacted = self.layernorm(interacted + query)
        feed_forward_out = self.dropout(self.feed_forward(interacted))
        decoded = self.layernorm(feed_forward_out + interacted)
        return decoded


class Transformer(nn.Module):

    def __init__(self, d_model, heads, num_layers, word_map):
        super(Transformer, self).__init__()

        self.d_model = d_model
        self.vocab_size = len(word_map)
        self.embed = Embeddings(self.vocab_size, d_model)
        self.encoder = nn.ModuleList([EncoderLayer(d_model, heads) for _ in range(num_layers)])
        self.decoder = nn.ModuleList([DecoderLayer(d_model, heads) for _ in range(num_layers)])
        self.logit = nn.Linear(d_model, self.vocab_size)

    def encode(self, src_words, src_mask):
        src_embeddings = self.embed(src_words)
        for layer in self.encoder:
            src_embeddings = layer(src_embeddings, src_mask)
        return src_embeddings

    def decode(self, target_words, target_mask, src_embeddings, src_mask):
        tgt_embeddings = self.embed(target_words)
        for layer in self.decoder:
            tgt_embeddings = layer(tgt_embeddings, src_embeddings, src_mask, target_mask)
        return tgt_embeddings

    def forward(self, src_words, src_mask, target_words, target_mask):
        encoded = self.encode(src_words, src_mask)
        decoded = self.decode(target_words, target_mask, encoded, src_mask)
        out = F.log_softmax(self.logit(decoded), dim=2)
        return out


class AdamWarmup:

    def __init__(self, model_size, warmup_steps, optimizer):
        self.model_size = model_size
        self.warmup_steps = warmup_steps
        self.optimizer = optimizer
        self.current_step = 0
        self.lr = 0

    def get_lr(self):
        return self.model_size ** (-0.5) * min(self.current_step ** (-0.5),
                                               self.current_step * self.warmup_steps ** (-1.5))

    def step(self):
        # Increment the number of steps each time we call the step function
        self.current_step += 1
        lr = self.get_lr()
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
        # update the learning rate
        self.lr = lr
        self.optimizer.step()

    def state_dict(self):
        return self.optimizer.state_dict()

    def load_state_dict(self, state_dict):
        self.optimizer.load_state_dict(state_dict)


class LossWithLS(nn.Module):

    def __init__(self, size, smooth):
        super(LossWithLS, self).__init__()
        self.criterion = nn.KLDivLoss(size_average=False, reduce=False)
        self.confidence = 1.0 - smooth
        self.smooth = smooth
        self.size = size

    def forward(self, prediction, target, mask):
        """
        prediction of shape: (batch_size, max_words, vocab_size)
        target and mask of shape: (batch_size, max_words)
        """
        prediction = prediction.view(-1, prediction.size(-1))  # (batch_size * max_words, vocab_size)
        target = target.contiguous().view(-1)  # (batch_size * max_words)
        mask = mask.float()
        mask = mask.view(-1)  # (batch_size * max_words)
        labels = prediction.data.clone()
        labels.fill_(self.smooth / (self.size - 1))
        labels.scatter_(1, target.data.unsqueeze(1), self.confidence)
        loss = self.criterion(prediction, labels)  # (batch_size * max_words, vocab_size)
        loss = (loss.sum(1) * mask).sum() / mask.sum()
        return loss


def evaluate(transformer, question, question_mask, max_len):
    transformer.eval()
    start_token = tokenizer.cls_token_id
    encoded = transformer.encode(question, question_mask)
    words = torch.LongTensor([[start_token]]).to(device)

    for step in range(max_len - 1):
        size = words.shape[1]
        target_mask = torch.triu(torch.ones(size, size)).transpose(0, 1).type(dtype=torch.uint8)
        target_mask = target_mask.to(device).unsqueeze(0).unsqueeze(0)
        decoded = transformer.decode(words, target_mask, encoded, question_mask)
        predictions = transformer.logit(decoded[:, -1])
        _, next_word = torch.max(predictions, dim=1)
        next_word = next_word.item()
        if next_word == tokenizer.sep_token_id:
            break
        words = torch.cat([words, torch.LongTensor([[next_word]]).to(device)], dim=1)

    # Convert tensor to list of token ids
    words = words.squeeze(0).tolist()

    # Convert token ids to tokens
    tokens = tokenizer.convert_ids_to_tokens(words)

    # Remove special tokens and join the tokens into a sentence
    sentence = ' '.join(tokens).replace(tokenizer.pad_token, '').strip()

    return sentence


"""transformer = Transformer(d_model = d_model, heads = heads, num_layers = num_layers, word_map = tokenizer.vocab)
transformer = transformer.to(device)
adam_optimizer = torch.optim.Adam(transformer.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9)
transformer_optimizer = AdamWarmup(model_size = d_model, warmup_steps = 2000, optimizer = adam_optimizer)
criterion = LossWithLS(len(tokenizer.vocab), 0.1)
total_params = sum(p.numel() for p in transformer.parameters())

print(f"Total number of parameters: {total_params}")


def train(train_loader, transformer, criterion, epoch):
    transformer.train()
    sum_loss = 0
    count = 0

    for i, (question, reply) in enumerate(train_loader):
        samples = question.shape[0]

        # Move to device
        question = question.to(device)
        reply = reply.to(device)

        # Prepare Target Data
        reply_input = reply[:, :-1]
        reply_target = reply[:, 1:]

        # Create mask and add dimensions
        question_mask, reply_input_mask, reply_target_mask = create_masks(question, reply_input, reply_target)

        # Get the transformer outputs
        out = transformer(question, question_mask, reply_input, reply_input_mask)

        # Compute the loss
        loss = criterion(out, reply_target, reply_target_mask)

        # Backprop
        transformer_optimizer.optimizer.zero_grad()
        loss.backward()
        transformer_optimizer.step()

        sum_loss += loss.item() * samples
        count += samples

        if i % 100 == 0:
            print("Epoch [{}][{}/{}]\tLoss: {:.3f}".format(epoch + 1, i, len(train_loader), sum_loss / count))


for epoch in range(epochs):

    train(train_loader, transformer, criterion, epoch)

    state = {'epoch': epoch+1, 'transformer': transformer, 'transformer_optimizer': transformer_optimizer,'train_state': transformer.state_dict(),'optimizer_state_dict': transformer_optimizer.state_dict()}
    torch.save(state, model_name+'_' + str(epoch+1) + '.pth.tar')



model_weights_path = ""
state = {'epoch': epochs, 'transformer': transformer, 'transformer_optimizer': transformer_optimizer,'train_state': transformer.state_dict(),'optimizer_state_dict': transformer_optimizer.state_dict()}

torch.save(transformer.state_dict(), model_weights_path)

checkpoint = torch.load(model_name)
transformer = checkpoint['transformer']

def inference(transformer,max_len,question):


    enc_qus = tokenizer.encode(question, add_special_tokens=True, max_length=max_len, truncation=True)
    question = torch.LongTensor(enc_qus).to(device).unsqueeze(0)
    question_mask = (question != tokenizer.pad_token_id).to(device).unsqueeze(1).unsqueeze(1)
    sentence = evaluate(transformer, question, question_mask, max_len)
    print(sentence)

# Implementation of tokenizer till here
"""


class CustomDataset(Dataset):
    def __init__(self, pairs):
        self.pairs = pairs
        self.dataset_size = len(self.pairs)

    def __getitem__(self, i):
        question = torch.LongTensor(self.pairs[i][0])
        reply = torch.LongTensor(self.pairs[i][1])
        return question, reply

    def __len__(self):
        return self.dataset_size


class TransformerModel:
    def __init__(self, d_model, dataset_name, input_set, label_set, batch_size, heads, num_layers, device, epochs,
                 model_name, max_len=50):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.max_len = max_len
        self.dataset_name = dataset_name
        self.input_set = input_set
        self.label_set = label_set
        self.batch_size = batch_size
        self.d_model = d_model
        self.heads = heads
        self.num_layers = num_layers
        self.device = device
        self.epochs = epochs
        self.model_name = model_name
        self.pairs = self.load_and_process_data()
        self.train_loader = self.create_data_loader()
        self.transformer = self.create_transformer()
        self.criterion = LossWithLS(len(self.tokenizer.vocab), 0.1)
        self.optimizer = self.create_optimizer()

    def load_and_process_data(self):
        pairs = []
        with open(self.dataset_name, 'r', errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            input_index = header.index(self.input_set)
            label_index = header.index(self.label_set)
            for row in csv_reader:
                try:
                    input_text = row[input_index].strip()
                    label_text = row[label_index].strip()
                    qa_pairs = [self.encode_question(input_text), self.encode_reply(label_text)]
                    pairs.append(qa_pairs)
                except IndexError:
                    print(f"Skipping row: {row}")
                    continue
        return pairs

    def create_data_loader(self):
        dataset = CustomDataset(self.pairs)
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=True, pin_memory=True)

    def create_transformer(self):
        transformer = Transformer(self.d_model, self.heads, self.num_layers, self.tokenizer.vocab)
        return transformer.to(self.device)

    def create_optimizer(self):
        adam_optimizer = torch.optim.Adam(self.transformer.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9)
        return AdamWarmup(model_size=self.d_model, warmup_steps=2000, optimizer=adam_optimizer)

    def encode_question(self, text):
        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        token_ids += [self.tokenizer.pad_token_id] * (self.max_len - len(token_ids))
        return token_ids

    def encode_reply(self, text):
        tokens = self.tokenizer.tokenize(text)
        token_ids = [self.tokenizer.cls_token_id] + self.tokenizer.convert_tokens_to_ids(tokens) + [
            self.tokenizer.sep_token_id]
        token_ids += [self.tokenizer.pad_token_id] * (self.max_len - len(token_ids))
        return token_ids

    def train(self):
        for epoch in range(self.epochs):
            self.transformer.train()
            sum_loss = 0
            count = 0
            for i, (question, reply) in enumerate(self.train_loader):
                samples = question.shape[0]
                question = question.to(self.device)
                reply = reply.to(self.device)
                reply_input = reply[:, :-1]
                reply_target = reply[:, 1:]
                question_mask, reply_input_mask, reply_target_mask = create_masks(question, reply_input, reply_target,
                                                                                  self.device)
                out = self.transformer(question, question_mask, reply_input, reply_input_mask)
                loss = self.criterion(out, reply_target, reply_target_mask)
                self.optimizer.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                sum_loss += loss.item() * samples
                count += samples
                if i % 100 == 0:
                    print(f"Epoch [{epoch + 1}][{i}/{len(self.train_loader)}]\tLoss: {sum_loss / count:.3f}")
            state = {
                'epoch': epoch + 1,
                'transformer': self.transformer,
                'transformer_optimizer': self.optimizer,
                'train_state': self.transformer.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict()
            }
            torch.save(state, f"{self.model_name}_{epoch + 1}.pth.tar")
        state = {
            'epoch': self.epochs,
            'transformer': self.transformer,
            'transformer_optimizer': self.optimizer,
            'train_state': self.transformer.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict()
        }
        torch.save(state, f"{self.model_name}_final.pth.tar")

    def inference(self, question):
        self.transformer.eval()
        enc_qus = self.tokenizer.encode(question, add_special_tokens=True, max_length=self.max_len, truncation=True)
        question_tensor = torch.LongTensor(enc_qus).unsqueeze(0)
        question_mask = (question_tensor != self.tokenizer.pad_token_id).unsqueeze(1).unsqueeze(1)
        question_tensor = question_tensor.to(self.device)
        question_mask = question_mask.to(self.device)
        sentence = evaluate(self.transformer, question_tensor, question_mask, self.max_len)
        print(sentence)