from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from stop_words import get_stop_words
from statistics import mode


def get_clusters(comb_frame, abstract, journals=[]):
    print(comb_frame)
    vectorizer = TfidfVectorizer(stop_words=get_stop_words())
    X = vectorizer.fit_transform(comb_frame)
    print('vectorizer:')
    print(X)

    # Quantidade de clusters
    true_k = 4

    # 19 clusters
    # Computer science
    # Medicine
    # Biology
    # Physics
    # Political science
    # Chemistry
    # Philosophy
    # Engineering
    # Mathematics
    # Psychology
    # Materials science
    # Art
    # Geography
    # Business
    # Sociology
    # Economics
    # Geology
    # History
    # Environmental science

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=15)
    model.fit(X)
    # print(model)

    # Top terms in each clusters.
    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    print(order_centroids)
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :15]:
            print(' %s' % terms[ind]),
        print

    # Continuing after vectorization step
    # data-structure to store Sum-Of-Square-Errors
    sse = {}
    comb_frame_dict = {}
    # Looping over multiple values of k from 1 to 30
    for k in range(1, 40):
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=100).fit(X)
        comb_frame_dict["clusters"] = kmeans.labels_
        sse[k] = kmeans.inertia_

    # print(sse)
    # # Plotting the curve with 'k'-value vs SSE
    # plt.plot(list(sse.keys()), list(sse.values()))
    # plt.xlabel("Number of cluster")
    # plt.ylabel("SSE")
    # # Save the Plot in current directory
    # plt.savefig('elbow_method.png')

    # print(model.predict(X))

    clusters = {}

    for i, work in enumerate(comb_frame):
        Y = vectorizer.transform([work])
        prediction = model.predict(Y)
        print(f'{i} - {prediction}')
        if prediction[0] not in clusters:
            clusters[prediction[0]] = {}
            clusters[prediction[0]][journals[i+1]] = 1
        else:
            if journals[i+1] not in clusters[prediction[0]]:
                clusters[prediction[0]][journals[i+1]] = 1
            else:
                clusters[prediction[0]][journals[i+1]] += 1

    print(clusters)

    def cluster_predict(str_input):
        # str_input eh e
        # str_input = str_input.split(' ')
        # print(str_input)
        Y = vectorizer.transform([str_input])
        prediction = model.predict(Y)
        return prediction
    
    prediction = cluster_predict(abstract)
    print(prediction)
    print(sorted(clusters[prediction[0]].keys(), key=lambda x:x[1], reverse=True))
    # print(mode(clusters[prediction[0]]))