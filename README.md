# Synonyms
An AI that can determine the synonym of a word from a list of words by learning from texts from novels

## How to use the AI
Clone this repository onto your local computer:

```
git clone https://github.com/dexter-1/Synonyms.git
```

Then change directory into the repository you just cloned
```
cd Synonyms
```

Then execute the following command:
```
python3 synonyms.py
```

This will begin to train the AI by parsing through the text files listen in the Novels folder. Once training has completed, you can select a word. Then give a list of words separated by a single space, where one of the words is the synonym of the first word you give. The AI will then print out the synonym of the word from the list of words.

To test the accuracy of the AI, uncomment lines 182-185 in synonyms.py. To increase the accuracy, add more text files into the Novels folder. However, the more training data the AI gets, the longer it takes to train.
