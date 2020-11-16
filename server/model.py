import tensorflow as tf
import tensorflow_hub as hub
from transformers import BertTokenizer

def initModel():
    #This model is a pretrained model made by see--
    #Source code is provided here: https://github.com/see--/natural-question-answering
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = hub.load("https://tfhub.dev/see--/bert-uncased-tf2-qa/1")
    return tokenizer, model

def computeAnswer(question, context, tokenizer, model):
    startPoint = 1
    endPoint = 1
    # Tokenizes the question and context inputs
    question_tokens = tokenizer.tokenize(question)
    context_tokens = tokenizer.tokenize(context)
    tokens = ['[CLS]'] + question_tokens + ['[SEP]'] + context_tokens
    if len(tokens) > 511:
        tokens = tokens[:511] + ['[SEP]']
    else:
        tokens = tokens + ['[SEP]']
    input_word_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_mask = [1] * len(input_word_ids)
    input_type_ids = [0] * (1 + len(question_tokens) + 1) + [1] * (len(tokens) - len(question_tokens) - 2)
    #Converts the tokenize inputs to TensorFlow Objects
    input_word_ids, input_mask, input_type_ids = map(lambda t: tf.expand_dims(tf.convert_to_tensor(t, dtype=tf.int32), 0), (input_word_ids, input_mask, input_type_ids))
    outputs = model([input_word_ids, input_mask, input_type_ids])
    # using `[1:]` will enforce an answer. `outputs[0][0][0]` is the ignored '[CLS]' token logit
    #From the output, we gather the tokens for the start and end of the short answer
    short_start = tf.argmax(outputs[0][0][1:]) + startPoint    
    short_end = tf.argmax(outputs[1][0][1:]) + endPoint

    answer_tokens = tokens[short_start: short_end + 1]
    #We then convert the tokens back to strings and provide the question and the answer.
    answer = tokenizer.convert_tokens_to_string(answer_tokens)

    if answer == question[:-1].lower() or answer == question[:-1].lower() + ' ?':
        answer = ''
  
    return answer

    
