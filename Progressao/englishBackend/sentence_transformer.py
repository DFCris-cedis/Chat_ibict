import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from sentence_transformers import SentenceTransformer, util

# #Our sentences we like to encode
# # sentences = ['This framework generates embeddings for each input sentence',
# #     'Sentences are passed as a list of string.',
# #     'The quick brown fox jumps over the lazy dog.']


def set_embedding(input, sentences):
    # print(sentences)
    print('entrei1')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # #Sentences are encoded by calling model.encode()
    # embeddings = model.encode(sentences)
    # #Print the embeddings
    # for sentence, embedding in zip(sentences, embeddings):
    #     print("Sentence:", sentence)
    #     print("Embedding:", embedding)
    #     print("")
    # Two lists of sentences
    print('entrei2')
    # sentences1 = ['The cat sits outside',
    #             'A man is playing guitar',
    #             'The new movie is awesome']
    
    print('input: ' + str(input))

    # sentences2 = ['The dog plays in the garden',
    #             'A woman watches TV',
    #             'The new movie is so great']

    #Compute embedding for both lists
    embeddings1 = model.encode(input, convert_to_tensor=True)
    embeddings2 = model.encode(sentences, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    print(cosine_scores)

    # max_value = -1
    # index = 0

    cos_sim = {}

    for i,val in enumerate(cosine_scores[0]):
        cos_sim[str(i)] = float(val)

    print(cos_sim)
    sorted_cos_sim = sorted(cos_sim.items(), key=lambda x:x[1], reverse=True)
    converted_dict = dict(sorted_cos_sim)
    print(converted_dict.keys())
    return list(converted_dict.keys())

    # print(max_value)
    # print(index)
    # print(sentences[index])


    #Output the pairs with their score
    # for i in range(len(sentences1)):
    #     print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))

# Fazer a mesma coisa para os concepts -> usando a colecao toda que eles tem
# Fazer cluster de concepts e tentar inserir um artigo no cluster