import ast
import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()


def create_table():
    index = open("data/index.txt", 'r').read()
    inverted_index = ast.literal_eval(index)

    nonpositional_postings = 0
    nonpositional_postings_no_nums = 0
    nonpositional_postings_case_folded = 0
    nonpositional_postings_stop_30 = 0
    nonpositional_postings_stop_150 = 0
    nonpositional_postings_stemmed = 0

    # ###### Calculate Unfiltered Terms and Non-Positional Postings ######
    unfiltered_terms = len(inverted_index)
    for entry in inverted_index:
        nonpositional_postings = nonpositional_postings + inverted_index[entry][0]
    # ###### ###################################################### ######

    # ###### Calculate No Numbers Terms and Non-Positional Postings ######
    no_numbers_dict = {k: v for k, v in inverted_index.items() if
                       not any(map(str.isdigit, k)) and not re.match('^\\x7f', k)}
    no_num_terms = len(no_numbers_dict)

    for entry in no_numbers_dict:
        nonpositional_postings_no_nums = nonpositional_postings_no_nums + no_numbers_dict[entry][0]
    # ###### ###################################################### ######

    # ###### Calculate Case Folding Terms and Non-Positional Postings ######
    case_folded_dict = {}
    for entry in no_numbers_dict:
        new_entry = entry.lower()
        postings = no_numbers_dict[entry]
        if new_entry not in case_folded_dict:
            case_folded_dict[new_entry] = postings
        else:
            case_folded_dict[new_entry][1].extend(postings[1])
            case_folded_dict[new_entry][1] = list(set(case_folded_dict[new_entry][1]))
            case_folded_dict[new_entry][1].sort(key=int)
            case_folded_dict[new_entry][0] = len(case_folded_dict[new_entry][1])

    case_folded_terms = len(case_folded_dict)
    for entry in case_folded_dict:
        nonpositional_postings_case_folded = nonpositional_postings_case_folded + case_folded_dict[entry][0]
    # ###### ###################################################### ######

    # ###### Calculate 30 StopWords Terms and Non-Positional Postings ######
    stopwords_30 = open("data/stop_30.txt", 'r').read().splitlines()
    stopwords_30_dict = {k: v for k, v in case_folded_dict.items() if not k in stopwords_30}
    stop_30_terms = len(stopwords_30_dict)
    for entry in stopwords_30_dict:
        nonpositional_postings_stop_30 = nonpositional_postings_stop_30 + stopwords_30_dict[entry][0]
    # ###### ###################################################### ######

    # ###### Calculate 150 StopWords Terms and Non-Positional Postings ######
    stopwords_150 = open("data/stop_150.txt", 'r').read().splitlines()
    stopwords_150_dict = {k: v for k, v in case_folded_dict.items() if not k in stopwords_150}
    stop_150_terms = len(stopwords_150_dict)
    for entry in stopwords_150_dict:
        nonpositional_postings_stop_150 = nonpositional_postings_stop_150 + stopwords_150_dict[entry][0]
    # ###### ###################################################### ######

    # ###### Calculate Stemming Terms and Non-Positional Postings ######
    stemmed_terms = 0
    # stemmed_dict = {}
    # for e in stopwords_150_dict:
    #     new_e = ps.stem(e)
    #     postings = stopwords_150_dict[e]
    #     if new_e not in stemmed_dict:
    #         stemmed_dict[new_e] = postings
    #     else:
    #         stemmed_dict[new_e][1].extend(postings[1])
    #         stemmed_dict[new_e][1] = list(set(stemmed_dict[new_e][1]))
    #         stemmed_dict[new_e][1].sort(key=int)
    #         stemmed_dict[new_e][0] = len(stemmed_dict[new_e][1])
    # stemmed_terms = len(stemmed_dict)
    # for entry in stemmed_dict:
    #     nonpositional_postings_stemmed = nonpositional_postings_stemmed + stemmed_dict[entry][0]
    # ###### ###################################################### ######

    # ###### ###################Calculate Delta and Total %################### ######
    delta11 = str(int(((no_num_terms/unfiltered_terms)-1)*100))
    total12 = delta11
    delta13 = str(int(((nonpositional_postings_no_nums/nonpositional_postings)-1)*100))
    total14 = delta13

    delta21 = str(int(((case_folded_terms/no_num_terms)-1)*100))
    total22 = str(int(((case_folded_terms/unfiltered_terms)-1)*100))
    delta23 = str(int(((nonpositional_postings_case_folded/nonpositional_postings_no_nums) - 1) * 100))
    total24 = str(int(((nonpositional_postings_case_folded/nonpositional_postings) - 1) * 100))

    delta31 = str(int(((stop_30_terms/case_folded_terms)-1)*100))
    total32 = str(int(((stop_30_terms/unfiltered_terms)-1)*100))
    delta33 = str(int(((nonpositional_postings_stop_30/nonpositional_postings_case_folded) - 1) * 100))
    total34 = str(int(((nonpositional_postings_stop_30/nonpositional_postings) - 1) * 100))

    delta41 = str(int(((stop_150_terms/case_folded_terms) - 1) * 100))
    total42 = str(int(((stop_150_terms/unfiltered_terms) - 1) * 100))
    delta43 = str(int(((nonpositional_postings_stop_150/nonpositional_postings_case_folded) - 1) * 100))
    total44 = str(int(((nonpositional_postings_stop_150/nonpositional_postings) - 1) * 100))

    delta51 = str(int(((stemmed_terms/stop_150_terms) - 1) * 100))
    total52 = str(int(((stemmed_terms/unfiltered_terms) - 1) * 100))
    delta53 = str(int(((nonpositional_postings_stemmed/nonpositional_postings_stop_150) - 1) * 100))
    total54 = str(int(((nonpositional_postings_stemmed/nonpositional_postings) - 1) * 100))
    # ###### ###################################################### ######

    # ###### #####################Build Table###################### ######
    table = "\t\t\t\t\t\t\t\tTerms\t\t\t\t\tNP Postings\n"
    table = table + "-----------------------------------------------------------------------------------\n"
    table = table + "\t\t\t\t\t\tnumber     D%     T%\t\tnumber     D%     T%\t\t\n"
    table = table + "-----------------------------------------------------------------------------------\n"
    table = table + "%s\t\t\t\t%s       %s     %s\t\t%s     %s     %s\t\t\n" % ('unfiltered', unfiltered_terms, "   ", "   ", nonpositional_postings, " ", " ")
    table = table + "%s\t\t\t\t%s       %s     %s\t\t%s     %s     %s\t\t\n" % ('no numbers', no_num_terms, delta11, total12, nonpositional_postings_no_nums, delta13, total14)
    table = table + "%s\t\t\t%s       %s     %s\t\t%s     %s     %s\t\t\n" % ('case folding', case_folded_terms, delta21, total22, nonpositional_postings_case_folded, delta23, total24)
    table = table + "%s\t\t\t%s         %s     %s\t\t%s     %s    %s\t\t\n" % ('30 stopwords', stop_30_terms, delta31, total32, nonpositional_postings_stop_30, delta33, total34)
    table = table + "%s\t\t\t%s         %s     %s\t\t%s     %s    %s\t\t\n" % ('150 stopwords', stop_150_terms, delta41, total42, nonpositional_postings_stop_150, delta43, total44)
    table = table + "%s\t\t\t\t%s       %s     %s\t\t%s     %s     %s\t\t\n" % ('stemming', stemmed_terms, delta51, total52, nonpositional_postings_stemmed, delta53, total54)
    table = table + "-----------------------------------------------------------------------------------\n"
    # ###### ###################################################### ######
    print(case_folded_dict, file=open("data/index_compressed.txt", 'w'))
    return table
