import config
import torch
from flask import Flask, request, jsonify
from time import perf_counter
from model import BERTBaseUncased

app = Flask(__name__)

MODEL = None
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def sentence_prediction(sentence):
    tokenizer = config.TOKENIZER
    max_len = config.MAX_LEN

    inputs = tokenizer.encode_plus(sentence, None, add_special_tokens=True, max_length=max_len)

    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]
    token_type_ids = inputs["token_type_ids"]

    padding_length = max_len - len(ids)
    ids = ids + ([0] * padding_length)
    mask = mask + ([0] * padding_length)
    token_type_ids = token_type_ids + ([0] * padding_length)

    ids = torch.tensor(ids, dtype=torch.long).unsqueeze(0)
    mask = torch.tensor(mask, dtype=torch.long).unsqueeze(0)
    token_type_ids = torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0)

    ids = ids.to(DEVICE, dtype=torch.long)
    token_type_ids = token_type_ids.to(DEVICE, dtype=torch.long)
    mask = mask.to(DEVICE, dtype=torch.long)

    outputs = MODEL(ids, mask, token_type_ids)

    outputs = torch.sigmoid(outputs).cpu().detach().numpy()
    return outputs[0][0]


@app.route("/predict", methods=["GET"])
def predict():
    sentence = request.args.get("sentence")
    start_time = perf_counter()
    positive_prediction = sentence_prediction(sentence)
    negative_prediction = 1 - positive_prediction
    response = {
        "response": {
            "positive": str(positive_prediction),
            "negative": str(negative_prediction),
            "sentence": str(sentence),
            "time_taken": str(perf_counter() - start_time),
        }
    }
    return jsonify(response)


if __name__ == "__main__":
    MODEL = BERTBaseUncased()
    MODEL.load_state_dict(torch.load(config.MODEL_PATH))
    MODEL.to(DEVICE)
    MODEL.eval()
    app.run(host="0.0.0.0", port="9999", debug=True)