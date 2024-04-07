"""
    Sentence Transformer 연결하여 문장 별로 비교하고 결과물 도출.
"""
import time
import numpy as np
from sentence_transformers import SentenceTransformer, util
from crawler import scrap_pion_world

def textToArr(text):
    data_val = text.replace('<', '').replace('>', '').replace('\n', '*').replace('. ', '*')
    txt_arr = data_val.split('*')
    txt_arr = [l.strip() for l in txt_arr]
    txt_arr = [v for v in txt_arr if v]
    return txt_arr

def StartMachine(inner, data):
    time.sleep(1)
    model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
    top_k = 5
    embeddings = model.encode(data, convert_to_tensor=True)
    query = inner
    query_embeddings = model.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embeddings, embeddings)[0]
    cos_scores = cos_scores.cpu()
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")
    for idx in top_results[0:top_k]:
        print(data[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))


if __name__ == "__main__":
    text = scrap_pion_world(show_screen=True)
    data = textToArr(text)
    for inner in data:
        StartMachine(inner, data)


