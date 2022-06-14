import torch
import transformers

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
MAX_LEN = 64
TRAIN_BATCH_SIZE = 8
VALID_BATCH_SIZE = 4
START = 50
EPOCHS = 100
BERT_PATH = "bert-base-uncased"
MODEL_PATH = "model.pt"
TRAINING_FILE = "../input/imdb.csv"
TOKENIZER = transformers.BertTokenizer.from_pretrained(BERT_PATH, do_lower_case=True)