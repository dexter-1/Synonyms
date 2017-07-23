'''Semantic Similarity AI
	An AI that can determine the synonym of a word from a list of word. The AI is trained from sample text novels. It learns by building semantic descriptor dictionaries
These dictionaries may look like this:
{animal: {the: 22, walks: 12, over: 2, to: owner, ...}, dog : {bark: 12, sits: 10, ...} , ...}
	The keys of the outer dictionary are all that appear in the novels given to the AI. The keys of the inner dictionary are all the other words that appear in the novels. The values of the dictionary
are the number of times two words appear in the same sentence. For example, "animal" and "the" appear in the same sentence 22 times.
	Once the dictionaries are built from the novels, three similarity functions can be used to determine if two words are similar. The idea is that if two words are similar, they should appear
in the same sentence with similar words. The three similarity functions, cosine_similarity, euc_similarity and euc_norm_similarity use this idea to try and compare two words and their semantic descriptor dictionaries to generate a
similarity score.
'''

import math

def unique_words(list):
    words = []
    for i in list:
        if i not in words:
            words.append(i)

    return words


def build_semantic_descriptors(sentences):
    #Training the AI from novels by building the semantic descriptor dictionaries
    semantic_descriptors = {}
    print("Training AI from Text Files ...")
    for a in range(len(sentences)):
        q = 1
        for b in unique_words(sentences[a]):
            if b not in semantic_descriptors.keys():
                semantic_descriptors[b] ={}


            for c in unique_words(sentences[a])[q:]:
                if c not in semantic_descriptors[b].keys():
                    semantic_descriptors[b][c] = 1
                    if c not in semantic_descriptors.keys():
                        semantic_descriptors[c] = {}

                    semantic_descriptors[c][b] = semantic_descriptors[b][c]

                else:
                    semantic_descriptors[b][c] += 1
                    if c not in semantic_descriptors.keys():
                        semantic_descriptors[c] = {}

                    semantic_descriptors[c][b] = semantic_descriptors[b][c]


            q += 1



    return semantic_descriptors


def build_semantic_descriptors_from_files(filenames):
	#Parsing the text from novels into arrays
    all_sentences = []
    for a in range(len(filenames)):
        f = open(filenames[a], "r", encoding="utf-8")
        text = f.read()
        text = text.lower()
        text = text.replace("!", ".")
        text = text.replace("?", ".")
        text = text.replace("-", "")
        text = text.replace("--", "")
        text = text.replace(",", "")
        text = text.replace(":", "")
        text = text.replace("'", "")
        text = text.replace(";", "")
        text = text.replace('"', '')
        text = text.replace("`", "")
        sentences = text.split(".")
        for i in range(len(sentences)-1):
        	sentences[i] = sentences[i].split()

        all_sentences += sentences


    return build_semantic_descriptors(all_sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
	# function used to determine the synonym of a word from a list of words. Tries to find the highest
	# similarity score between the word and the given choices using the similarity_fn
    if word not in semantic_descriptors.keys():
        return -1

    else:
        vec1 = semantic_descriptors[word]
        max_similarity = None
        best_choice = None
        for i in choices:
            if i in semantic_descriptors.keys():
                vec2 = semantic_descriptors[i]

                if max_similarity == None:
                    max_similarity = similarity_fn(vec1, vec2)
                    best_choice = i

                if similarity_fn(vec1, vec2) > max_similarity:
                    max_similarity = similarity_fn(vec1, vec2)
                    best_choice = i



        return best_choice


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def dot_product(vec1, vec2):
    dp = 0
    for i in vec1:
        if i in vec2:
            dp += vec1[i]*vec2[i]

    return dp

'''
The three similarity metrics used to determine if two words are synonyms: cosine_similarity, euc_similarity and euc_norm_similarity
'''

def cosine_similarity(vec1, vec2):
    return dot_product(vec1, vec2)/(norm(vec1)*norm(vec2))

def euc_similarity(vec1, vec2):
    vec3 = {}
    for i in vec1:
        if i in vec2:
            vec3[i] = vec1[i] - vec2[i]

    return -norm(vec3)

def euc_norm_similarity(vec1, vec2):
    vec3 = {}
    for i in vec1:
        if i in vec2:
            vec3[i] = vec1[i]/norm(vec1) - vec2[i]/norm(vec2)

    return -norm(vec3)

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''
    function for testing the accuracy of the AI. Each line in test.txt contains four words. The first
    word is the test word, second word is the answer, and the last two words are the choices. This function
    returns the accuracy of the AI in a percentage
    '''
    f = open(filename, encoding="utf-8")
    text = f.read()
    text = text.lower()
    sentence = text.split("\n")
    del(sentence[-1])
    for i in range(len(sentence)):
        sentence[i] = sentence[i].split()

    counter = 0
    for j in sentence:
        if j[1] == most_similar_word(j[0], j[2:], semantic_descriptors, similarity_fn):
            counter += 1


    return (counter/len(sentence))*100

if __name__ == '__main__':
    import os
    path = os.getcwd() + '/Novels'
    os.chdir(path)
    filenames = ["spook_stories.txt", "the_little_world.txt", "visible_and_invisible.txt", "war_and_passion.txt", "alicewonderland.txt", "time_machine.txt"]
    semantic_descriptors = build_semantic_descriptors_from_files(filenames)

    # #Uncomment the code below to run tests and see the accuracy of the AI
    # print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))
    # print(run_similarity_test("test.txt", semantic_descriptors, euc_similarity))
    # print(run_similarity_test("test.txt", semantic_descriptors, euc_norm_similarity))

    while True:
        word = input("Choose a word: ")
        choices = input("Give a list of words seperated by spaces (i.e. car wheel window): ")
        choices = choices.split(" ")
        print("The synonym of the word {} is : {}".format(word, most_similar_word(word, choices, semantic_descriptors, euc_norm_similarity)))
