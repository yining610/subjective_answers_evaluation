from thefuzz import fuzz
from thefuzz import process

# simple ratio
print(fuzz.ratio("this is a test", "this is a test"))

# partial ratio
print(fuzz.partial_ratio("this is a test", "this is a test"))

# Token sort ratio
print(fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"))
print(fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"))

# Token set ratio
print(fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear"))
print(fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear"))

# process
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
print(process.extract("new york jets", choices, limit=2))

print(process.extractOne("cowboys", choices))