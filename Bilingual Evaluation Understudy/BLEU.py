# Bilingual Evaluation Understudy Score (BLEU)
# Ranges from 0 to 1
# Proposed at 2002
# THe approach workd by counting matching n-grams in the candidate translation to n-grams in the reference text

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import corpus_bleu # for calculating the BLEU score for multiple sentences
reference = [["this", "is", "a", "test"],["this","is","test"]]
reference_corpus = [[["this", "is", "a", "test"],["this","is","test"]]]
candidate = ["this", "is", "a", "test"]
candidate_corpus = [["this", "is", "a", "test"]]

score = sentence_bleu(reference, candidate)
corpus_score = corpus_bleu(reference_corpus, candidate_corpus)
individual_score = sentence_bleu(reference, candidate, weights=(1,0,0,0)) # Calculate the BLEU score only for 1-gram matches
cumulative_score = sentence_bleu(reference, candidate, weights=(0.25,0.25,0.25,0.25))

print(score)
print(corpus_score)
print(individual_score)
print(cumulative_score)
