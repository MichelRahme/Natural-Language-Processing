from math import log10

from bm25_p4 import BM25


class Query:

    def __init__(self, query, queryType, index, scraped_data, scraped_urls):
        """
        :param query: query from user
        :param queryType: type of query (AND, OR, BM25)
        :param index: the final index
        :param scraped_data: data containing the URLs and their text
        :param scraped_urls: the list of scraped URLs in order.
        """
        self.query = query
        self.queryType = queryType
        self.index = index
        self.scraped_data = scraped_data
        self.scraped_urls = scraped_urls
        # Change k1, b values here
        self.okapi = BM25(self.index, 0.5, 0.5, self.scraped_data, self.scraped_urls)
        if queryType == 1:
            self.and_query(self.query)
        elif queryType == 2:
            self.or_query(self.query)
        elif queryType == 3:
            self.bm25_query(self.query)

    def and_query(self, query):
        """
        AND Query, simple implementation.
        Take the intersection of the postings list of each term in Query.

        The result is however ranked only by TF-IDF.

        """
        docs = []
        count = {}  # Where the document and its score are saved
        result = []
        query_tokens = query.split()
        for token in query_tokens:
            if token in self.index:
                docs.append(self.index[token][1])
        if len(docs) != 0 and len(docs) == len(query_tokens):
            result = docs[0].keys()
            for index in docs:
                result = result & index.keys()
        print("Resulting Documents ranked by TF-IDF: ")
        for index in docs:
            for doc in result:
                tf = index[doc]
                idf = log10((len(self.scraped_urls)) / len(index))
                tf_idf = tf * idf
                if doc not in count:
                    count[doc] = tf_idf
                else:
                    count[doc] = count[doc] + tf_idf
        count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}
        print(count)
        print("TOP 15 Webpages: ")
        counter = 0
        for entry in count:
            if counter < 15:
                counter += 1
                print("Document {}: {}".format(entry, self.scraped_urls[int(entry) - 1]))

    def or_query(self, query):
        """
        OR Query, simple implementation.
        Take the union of the postings list of each term in Query.

        The result is however ranked only by TF-IDF.

        """
        docs = []
        count = {}  # Where the document and its score are saved
        result = set()
        query_tokens = query.split()
        for token in query_tokens:
            if token in self.index:
                docs.append(self.index[token][1])
        for index in docs:
            for key in index:
                result.add(key)
        print("Resulting Documents ranked by TF-IDF: ")
        for index in docs:
            for doc in result:
                if doc in index:
                    tf = index[doc]
                    idf = log10((len(self.scraped_urls)) / len(index))
                    tf_idf = tf * idf
                    if doc not in count:
                        count[doc] = tf_idf
                    else:
                        count[doc] = count[doc] + tf_idf
        count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}
        print(count)
        print("TOP 15 Webpages: ")
        counter = 0
        for entry in count:
            if counter < 15:
                counter += 1
                print("Document {}: {}".format(entry, self.scraped_urls[int(entry) - 1]))

    def bm25_query(self, query):
        """
        BM25 query.

        Here we simply get ALL postings list for each term in the query and rank them using BM25.
        """
        docs = []
        count = {}  # Where the document and its score are saved
        result = set()
        query_tokens = query.split()
        for token in query_tokens:
            if token in self.index:
                docs.append(self.index[token][1])
        for index in docs:
            for key in index:
                result.add(key)  # Empty set
        print("Resulting Documents ranked by Okapi BM25: ")
        for doc in result:
            for q in query_tokens:
                if q in self.index:
                    if doc not in count:
                        count[doc] = self.okapi.calculate_rsv(q, doc)
                    else:
                        count[doc] += self.okapi.calculate_rsv(q, doc)
        print(sorted(count.items(), key=lambda item: item[1], reverse=True))
        print("TOP 15 Webpages: ")
        counter = 0
        for entry in count:
            if counter < 15:
                counter += 1
                print("Document {}: {}".format(entry, self.scraped_urls[int(entry) - 1]))
