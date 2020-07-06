import random
import os
import time
import copy
import json

def typing_speed_test(sentences_file_path, highest_scores):
    sentence = None
    with open(sentences_file_path, "r") as f:
        lines = f.readlines()
        sentence = random.choice(lines).strip()

    while True:
        if highest_scores:
            print("These are top {} scores:".format(len(highest_scores)))
            for i, s in enumerate(highest_scores):
                print("({}) ".format(i+1), s)
        start_flag = input("Please enter '1' when you're ready to start, or 'END' when you want to finish")
        if start_flag.strip() == '1':
            start_time = time.time()
            line_written = input("Enter line: '"+ sentence + "'")
            end_time = time.time()
            total_time = end_time - start_time
            if line_written == sentence:
                total_time_normalized = total_time/len(sentence)
                print("Total time: ", total_time)
                print("Total time normalized: ", total_time_normalized)
                if len(highest_scores) < 5 or total_time_normalized < highest_scores[-1]:
                    if len(highest_scores) >= 5:
                        del highest_scores[-1]
                    highest_scores.append(total_time_normalized)
                    highest_scores.sort()
                    print("Congratulations! You were added to all-starts score board!!!")
                return total_time_normalized
            else:
                print("Wrong typing, please try again...")
        elif start_flag.strip() == 'END':
            break


if __name__ == '__main__':
    sentences_file_path = "sentences.txt"
    
    highest_scores = list()
    scores_file_path = "highest_scores.json"
    
    if os.path.isfile(scores_file_path):
        highest_scores = json.load(open(scores_file_path, "r"))
    else:
        highest_scores = []

    original_scores = copy.deepcopy(highest_scores)
    typing_speed_test(sentences_file_path, highest_scores)

    # save the results
    if original_scores != highest_scores:
        json.dump(highest_scores, open(scores_file_path, "w"))

