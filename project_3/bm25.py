from math import log10

class BM25:

    def __init__(self, index, documents, k, b, n):
        self.index = index
        self.documents = documents
        self.k = k
        self.b = b
        self.n = n
        self.totalLength = 0
        # Get the total length of all documents
        for doc in self.documents:
            self.totalLength += len(self.documents[doc])

    def calculate_idf(self, term):
        if term in self.index:
            return log10(self.n/len(self.index[term]))
        else:
            return 0

    def calculate_rsv(self, term, docID):
        """
        We have Every information to calculate RSV because of how the Documents were initial divided.
        The IDF is already calculated above.

        Then we calculate the numerator, denominator and finally the RSV value.
        """
        tf = self.documents[str(docID)].count(term)
        Ld = len(self.documents[str(docID)])
        Laverage = self.totalLength / self.n
        numerator = ((self.k + 1)*tf)
        denominator = ((self.k*((1-self.b) + (self.b*(Ld/Laverage)))) + tf)
        if denominator != 0:
            return self.calculate_idf(term) * numerator/denominator
        else:
            return self.calculate_idf(term) * numerator


