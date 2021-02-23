from sortedcontainers import SortedSet
from bm25 import BM25


class Query:

    def __init__(self, query, queryType, index, documents):
        self.query = query
        self.queryType = queryType
        self.index = index
        self.documents = documents
        # Change k1, b values here
        self.okapi = BM25(self.index, self.documents, 0.5, 0.5, len(self.documents))
        if queryType == 1:
            self.single_word_query(self.query)
        elif queryType == 2:
            self.and_query(self.query)
        elif queryType == 3:
            self.or_query(self.query)
        elif queryType == 4:
            self.bm25_query(self.query)

    def single_word_query(self, query):
        """
        Simple single word query.
        Take the query and look for it in the index and get the postings list.

        All 3 ways to rank the results are implemented and commented out:
        - You can have no rank
        - You can rank by TF
        - You can rank by BM25
        """
        docs = []
        count = {}  # Where the document and its score are saved

        print("\nResulting Documents not Ranked: ")
        if query in self.index:
            docs = self.index[query]
        print(list(docs))

        print("\nResulting Documents ranked by Okapi BM25: ")
        for doc in docs:
            count[doc] = self.okapi.calculate_rsv(query, doc)
        print(sorted(count.items(), key=lambda item: item[1], reverse=True))

        # To rank by doc frequency uncomment
        # print("Resulting Documents ranked by TF: ")
        # for doc in docs:
        #     count[doc] = self.documents[str(doc)].count(query)
        # print(sorted(count.items(), key=lambda item: item[1], reverse=True))

    def and_query(self, query):
        """
        AND Query, simple implementation.
        Take the intersection of the postings list of each term in Query.

        The result is also ranked in two ways: Either in TF or BM25. You can uncomment and decide what to use since
        requirements are not clear.

        """
        docs = []
        count = {}  # Where the document and its score are saved
        query_tokens = query.split()
        for token in query_tokens:
            if token in self.index:
                docs.append(SortedSet(self.index[token]))
            if token not in self.index:
                docs.append(SortedSet())  # Empty Set
        result = docs[0]
        for entry in docs:
            result = result.intersection(list(entry))

        # print("Resulting Documents ranked by Okapi BM25: ")
        # for doc in result:
        #     for q in query_tokens:
        #         if doc not in count:
        #             count[doc] = self.okapi.calculate_rsv(q, doc)
        #         else:
        #             count[doc] += self.okapi.calculate_rsv(q, doc)
        # print(sorted(count.items(), key=lambda item: item[1], reverse=True))

        print("Resulting Documents ranked by TF: ")
        for doc in result:
            for query in query_tokens:
                if doc not in count:
                    count[doc] = self.documents[str(doc)].count(query)
                elif doc in count:
                    count[doc] += self.documents[str(doc)].count(query)
        print(sorted(count.items(), key=lambda item: item[1], reverse=True))

    def or_query(self, query):
        """
        OR Query, simple implementation.
        Take the union of the postings list of each term in Query.

        The result is however ranked only by TF as asked for in the handout.

        """
        docs = []
        count = {}  # Where the document and its score are saved
        result = SortedSet()
        query_tokens = query.split()
        for token in query_tokens:
            if token in self.index:
                docs.append(self.index[token])
            if token not in self.index:
                docs.append(SortedSet())
        for entry in docs:
            result = result.union(list(entry))

        for doc in result:
            for query in query_tokens:
                if doc not in count:
                    count[doc] = self.documents[str(doc)].count(query)
                elif doc in count:
                    count[doc] += self.documents[str(doc)].count(query)
        print("Resulting Documents ranked by TF: ")
        print(sorted(count.items(), key=lambda item: item[1], reverse=True))

    def bm25_query(self, query):
        """
        BM25 query, asked for in the new Amended project.

        Here we simply get ALL postings list for each term in the query and rank them using BM25.
        """
        docs = []
        count = {}  # Where the document and its score are saved
        query_tokens = query.split()
        for token in query_tokens:
            if token in self.index:
                docs.append(self.index[token])
            if token not in self.index:
                docs.append(SortedSet())  # Empty set
        print("Resulting Documents ranked by Okapi BM25: ")
        for postingsList in docs:
            for doc in postingsList:
                for q in query_tokens:
                    if doc not in count:
                        count[doc] = self.okapi.calculate_rsv(q, doc)
                    else:
                        count[doc] += self.okapi.calculate_rsv(q, doc)
        print(sorted(count.items(), key=lambda item: item[1], reverse=True))
