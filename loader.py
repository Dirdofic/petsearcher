import pickle
from parser import kinpet_parser
from smart_search import SmartSearch
data_parser = kinpet_parser()
searcher = SmartSearch(data_parser.get_lost_pets_database())

# Save data_parser to a pickle file
with open('data_parser.pickle', 'wb') as f:
    pickle.dump(data_parser, f)

# Save searcher to a pickle file
with open('searcher.pickle', 'wb') as f:
    pickle.dump(searcher, f)