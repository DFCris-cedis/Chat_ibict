from typing import Union
import json
from fastapi import FastAPI
import pandas as pd
import json
from .vectorial_model import get_vectorial_model, pre_processing
from .k_means import get_clusters
from .sentence_transformer import set_embedding
import requests
import json
from pydantic import BaseModel
import paramiko
import boto3

app = FastAPI()

# get your instance ID from AWS dashboard

class Data(BaseModel):
    abstract: str
    title: str

def is_works(content):
    if "doi" in content:
        return True
    return False

def get_remote_works(title, abstract):

    print('entrando')

    payload_dict = {"title":[title], "abstract": abstract, "inverted_abstract":False, "journal":"", "doc_type":""}
    r2 = requests.post('http://15.228.87.227:8080/invocations', json=payload_dict)
    tags = json.loads(r2.text)[0]['tags']

    return tags

@app.post("/works")
def get_works(data: Data):
    print(data.abstract)
    print(data.title)
    concepts = get_remote_works(data.title, data.abstract)
    return get_concepts_embeddings(concepts)

def get_concepts_cluster(abstract):
    phrases = []
    journals = {}
    # journals_count = {}
    acc = 1
    with open("./works.txt",'r') as data_file:
        for line in data_file:
            work_words = ''
            # print(line)
            work = json.loads(line)
            # print(work)
            if work['concepts'] is not None:
                for concept in work['concepts']:
                    work_words = work_words + concept['display_name'] + ' '
                journals[acc] = work['primary_location']
                acc += 1
                phrases.append(work_words)

    get_clusters(phrases, abstract, journals)

def get_abstracts_clusters(abstract):
    print(abstract)

    # abstract_keywords = abstract.split(' ')

    phrases = []
    journals = {}
    journals_count = {}
    acc = 1
    with open("./works.txt",'r') as data_file:
        for line in data_file:
            work_words = ''
            # print(line)
            work = json.loads(line)
            # print(work)
            if work['abstract_inverted_index'] is not None:
                for word in work['abstract_inverted_index']:
                    qty = len(work['abstract_inverted_index'][word])
                    work_words = work_words + word + ' '
                journals[acc] = work['primary_location']
                acc += 1
                phrases.append(work_words)

    # print(phrases)
    get_clusters(phrases, abstract, journals)
    # set_embedding([abstract], phrases)

def get_abstracts_embeddings(abstract):
    print(abstract)

    # abstract_keywords = abstract.split(' ')

    phrases = []
    journals = {}
    journals_count = {}
    acc = 0
    with open("./works.txt",'r') as data_file:
        for line in data_file:
            work_words = ''
            # print(line)
            work = json.loads(line)
            # print(work)
            if work['abstract_inverted_index'] is not None:
                for word in work['abstract_inverted_index']:
                    qty = len(work['abstract_inverted_index'][word])
                    work_words = work_words + word + ' '
                journals[str(acc)] = work['primary_location']
                acc += 1
                phrases.append(work_words)

    final_ranking = set_embedding([abstract], phrases)
    final_ranking = final_ranking[:1000]

    print(journals)
    
    for index in final_ranking:
        journal_id = journals[index]
        print(journal_id)
        if journal_id in journals_count:
            journals_count[journal_id] += 1
        else:
            journals_count[journal_id] = 1

    biggest_journals = sorted(journals_count, key=journals_count.get, reverse=True)[:3]

    for i,journal in enumerate(biggest_journals):
        id = journal.split('https://openalex.org/')[1]
        url = 'https://api.openalex.org/sources/' + id
        res = requests.get(url)
        response = json.loads(res.text)
        biggest_journals[i] = response['display_name']

    return biggest_journals

def get_concepts_embeddings(concepts):

    print('Concepts Embeddings: ')

    phrases = []
    journals = {}
    journals_count = {}
    acc = 0
    with open("./works.txt",'r') as data_file:
        for line in data_file:
            work_words = ''
            # print(line)
            work = json.loads(line)
            # print(work)
            if work['concepts'] is not None:
                for concept in work['concepts']:
                    work_words = work_words + concept['display_name'] + ' '
                journals[acc] = work['primary_location']
                acc += 1
                phrases.append(work_words)

    final_ranking = set_embedding(concepts, phrases)
    final_ranking = final_ranking[:1000]

    print(journals)
    
    for index in final_ranking:
        journal_id = journals[int(index)]
        print(journal_id)
        if journal_id in journals_count:
            journals_count[journal_id] += 1
        else:
            journals_count[journal_id] = 1

    biggest_journals = sorted(journals_count, key=journals_count.get, reverse=True)[:10]

    for i,journal in enumerate(biggest_journals):
        id = journal.split('https://openalex.org/')[1]
        url = 'https://api.openalex.org/sources/' + id
        res = requests.get(url)
        response = json.loads(res.text)
        biggest_journals[i] = response['display_name']

    return biggest_journals

def get_works_concepts(abstract, works):

    abstract_keywords = abstract.split(' ')

    phrases = []
    journals = {}
    journals_count = {}
    acc = 1
    for line in works:
        work_words = []
        work = json.loads(line)
        print(work)
        if work['abstract_inverted_index'] is not None:
            for word in work['abstract_inverted_index']:
                qty = len(work['abstract_inverted_index'][word])
                work_words = work_words + ([word] * qty)
            journals[acc] = work['primary_location']['source']['id']
            acc += 1
            phrases.append(work_words)

    print(journals)

    final_ranking = get_vectorial_model(phrases,abstract_keywords)
    final_ranking = final_ranking[:1000]
    
    for index in final_ranking:
        journal_id = journals[index]
        if journal_id in journals_count:
            journals_count[journal_id] += 1
        else:
            journals_count[journal_id] = 1

    biggest_journals = sorted(journals_count, key=journals_count.get, reverse=True)[:3]

    for i,journal in enumerate(biggest_journals):
        id = journal.split('https://openalex.org/')[1]
        url = 'https://api.openalex.org/sources/' + id
        res = requests.get(url)
        response = json.loads(res.text)
        biggest_journals[i] = response['display_name']

    return biggest_journals

@app.get("/countries")
def read_root():
    countries = [
        'Brasil',
        'Estados Unidos',
        'Colombia',
        'Uruguai'
    ]

    return countries

def get_main_concepts():
    # with open('./concepts.json') as json_data:
    #     data = json.load(json_data)
    #     df = pd.DataFrame(data['results'])
    #     print(df.to_string())
    #     concepts = df.to_xarray()
    #     print(concepts)
        # for concept in concepts:
        #     print(concept)
    concepts = [
        "Computer science",
        "Medicine",
        "Biology",
        "Physics",
        "Political science",
        "Chemistry",
        "Philosophy",
        "Engineering",
        "Mathematics",
        "Psychology",
        "Materials science",
        "Art",
        "Geography",
        "Business",
        "Sociology",
        "Economics",
        "Geology",
        "Environmental science"
    ]

    return concepts


def get_category():
    values = []
    concepts = get_main_concepts()
    concepts_works = {}

    for c in concepts:
        concepts_works[c] = []

    print(concepts_works)

    with open("./updated_date=2023-02-07/part_000.txt",'r') as data_file:
        # data_file2 = [data_file[0]]
        # print(data_file[0])
        for line in data_file:
            concepts_in_sources = [0] * len(concepts)
            source = json.loads(line)
            # big_qty = ["",-1]
            for concept in source['x_concepts']:
                # print(concept)
                if concept['display_name'] in concepts:
                    index = concepts.index(concept['display_name'])
                    concepts_in_sources[index] = concept['score']
                # if concept['score'] > big_qty[1]:
                #     big_qty = [concept['display_name'],concept['score']]
                # elif concept['score'] == big_qty[1]:
                #     source['category'] = None
                #     big_qty[0] = None
                #     break
            # if big_qty[0] is not None:
            source['category'] = concepts_in_sources
            print(source)
            
            # print(source)
            values.append(str(source))
            break
        data_file.close()

    # print(values)

    # with open("./updated_date=2023-02-07/part_000.txt",'w') as data_file:
    #     data_file.writelines(values)
    #     data_file.close()
    
    # return values

@app.get("/sources")
def read_root():
    # get_category()
    # with open("./updated_date=2023-02-07/part_000.txt",'r') as data_file:
    #     for line in data_file:
    #         print(line)

    return [{"id": 1234, "name": "test"}]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}