import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    matches = []

    N = len(gender_id)
    n = N // 2
    unprocessed_rankings = []
    matched = [None] * N

    preferences_dict = {
        "Women": ["Female"],
        "Men": ["Male"],
        "Bisexual": ["Female", "Male"]
    }

    # update scores to account for gender preferences
    for i in range(N):
        for j in range(N):
            if i != j:
                if (gender_id[i] not in preferences_dict[gender_pref[j]]) or (gender_id[j] not in preferences_dict[gender_pref[i]]):
                    scores[i][j] = 0
    
    # get rankings for each person
    for i in range(N):
        unprocessed_rankings.append(np.argsort(-np.array(scores[i])))

    # process rankings
    rankings = []
    for row in unprocessed_rankings:
        new_row = []
        for elt in row:
            if elt >= n:
                new_row.append(elt)
        rankings.append(new_row)
    
    # let the first half of people be proposers and the second half be receivers
    unmatched_proposers = n
    
    # while some proposer is free and hasn't proposed to every receiver
    while unmatched_proposers > 0:
       
        # choose such a proposer
        proposer = 0
        while proposer < n and matched[proposer] != None:
            proposer += 1
        
        # iterate through receivers on their list
        ind = 0
        while ind < N and matched[proposer] == None:
            receiver = rankings[proposer][ind]

            # if free, match them
            if matched[receiver] == None:
                matched[receiver] = proposer
                matched[proposer] = receiver
                unmatched_proposers -= 1
            
            else:
                # if receiver prefers this proposer, match them
                prev_proposer = matched[receiver]
                if rankings[receiver][proposer] > rankings[receiver][prev_proposer]:
                    matched[receiver] = proposer
                    matched[proposer] = receiver
                    matched[prev_proposer] = None

            # otherwise, rejected
            ind += 1

    # update list of matches
    for i in range(n):
        matches.append((i, matched[i]))

    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
