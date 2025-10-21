import spacy
import json
import random
from spacy.tokens import DocBin

def prepare_training_data(json_file_path):
    print("Carregando e preparando os dados de treinamento...")
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo {json_file_path} não foi encontrado.")
        return None

    train_data = []
    all_tags = set()
    for intent in data.get('intents', []):
        tag = intent.get('tag')
        if not tag:
            continue
        all_tags.add(tag)
        for pattern in intent.get('patterns', []):
            train_data.append((pattern, {"cats": {tag: True}}))

    if not train_data:
        print("Nenhum dado de treinamento válido encontrado no arquivo JSON.")
        return None

    print(f"Dados carregados. Total de exemplos: {len(train_data)}. Tags: {all_tags}")
    return train_data, list(all_tags)

def create_spacy_corpus(data, tags, file_path):
    print(f"Criando o corpus spaCy em '{file_path}'...")
    nlp = spacy.blank("pt")
    db = DocBin()

    random.shuffle(data)

    for text, annot in data:
        doc = nlp.make_doc(text)
        # Garante que todas as tags possíveis sejam inicializadas para cada exemplo
        cats = {tag: 0 for tag in tags}
        cats.update(annot['cats'])
        doc.cats = cats
        db.add(doc)

    db.to_disk(file_path)
    print("Corpus criado com sucesso.")

if __name__ == "__main__":
    train_data, all_tags = prepare_training_data('training/intents.json')

    if train_data:
        split = int(len(train_data) * 0.8)
        train_set = train_data[:split]
        dev_set = train_data[split:]

        create_spacy_corpus(train_set, all_tags, "training/train.spacy")
        create_spacy_corpus(dev_set, all_tags, "training/dev.spacy")
        print("\nArquivos de dados 'train.spacy' e 'dev.spacy' gerados na pasta 'training'.")
        print("Agora você está pronto para o próximo passo: o treinamento.")