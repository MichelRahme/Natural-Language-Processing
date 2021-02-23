from math import log10

class BM25:

    def __init__(self, index, k, b, scraped_data, scraped_urls):
        """

        :param index: the finl index
        :param k: k value (0.5)
        :param b: b value (0.5)
        :param scraped_data: data containing the URLs and their text
        :param scraped_urls: the list of scraped URLs in order.
        """
        self.index = index
        self.scraped_urls = scraped_urls
        self.scraped_data = scraped_data
        self.k = k
        self.b = b
        self.totalLength = 0
        # Get the total length of all documents
        for doc in self.scraped_data:
            self.totalLength += len(doc['content'])

    def calculate_idf(self, term):
        if term in self.index:
            return log10(len(self.scraped_urls) / self.index[term][0])
        else:
            return 0

    def calculate_rsv(self, term, docID):
        """
        We have Every information to calculate RSV because of how the Documents were initial divided.
        The IDF is already calculated above.

        Then we calculate the numerator, denominator and finally the RSV value.
        """
        if docID in self.index[term][1]:
            tf = self.index[term][1][docID]
            Ld = len(self.scraped_data[int(docID)-1]['content'])
            Laverage = self.totalLength / len(self.scraped_urls)
            numerator = ((self.k + 1)*tf)
            denominator = ((self.k*((1-self.b) + (self.b*(Ld/Laverage)))) + tf)
            if denominator != 0:
                return self.calculate_idf(term) * numerator/denominator
            else:
                return self.calculate_idf(term) * numerator
        else:
            return 0


