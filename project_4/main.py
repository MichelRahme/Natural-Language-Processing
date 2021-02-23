from scraper import start_crawl
from index_builder import Spimi
from query_p4 import Query


def ask_for_query():
    """
    Helper static function that handles user input for submitting queries.
    """
    while True:
        queryType = input('\n\nPlease select query type: [1] AND (TF-IDF) [2] OR (TF-IDF) [3] BM25: ')
        if queryType not in {'1', '2', '3'}:
            print('We expect you to enter a valid integer')
        else:
            num = int(queryType)
            query = input("Please enter query: ")
            return [num, query.lower()]


if __name__ == '__main__':
    """
    Main Method
    
    Change the value in start_crawl to limit the number of scraped urls, line 26.
    """
    scraped_urls = start_crawl(5000)
    spimi = Spimi()
    while True:
        user_input = ask_for_query()
        query_module = Query(user_input[1], int(user_input[0]), spimi.finalIndex, spimi.scraped_data, scraped_urls)
        entry = input("\nWould you like to run another query? [T/F] : ")
        if entry.lower() == "t":
            continue
        if entry.lower() == "f":
            print("Thanks, Goodbye!")
            break
