from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from random import randint
import re

PATH = "test/corpus.txt"

def preprocess():
    with open(PATH, "r", encoding="utf-8") as f:
        corpus = f.read().split()
    res = list()
    for i in range(len(corpus) - 1):
        res.append((corpus[i], corpus[i + 1]))
    return res


class TextGeneratorTests(StageTest):
    def generate(self):
        test_input1 = PATH + "\nexit\n"
        test_input2 = PATH + "\n0\n1\n2\n-1\nten\n43256236577\nexit\n"
        test_input3 = PATH + "\n" + "\n".join(
            [str(randint(0, 300000)) for _ in range(10)]) + "\nexit\n"

        return [
            TestCase(stdin=test_input1, attach=test_input1),
            TestCase(stdin=test_input2, attach=test_input2),
            TestCase(stdin=test_input3, attach=test_input3)
        ]

    def check(self, reply, attach):
        try:
            corpus = preprocess()
        except FileNotFoundError:
            return CheckResult.wrong("File not found at {}. Make sure the file "
                                     "has not been deleted or moved.".format(PATH))

        # check output format
        if not reply:
            return CheckResult.wrong("The output cannot be empty! Make "
                                     "sure to output the results of your program!")

        lines = re.split("\n+", reply)
        if len(lines) < 1:
            return CheckResult.wrong("The output should consist of at least a line!")

        stats, res = lines[0:1], lines[1:-1]

        # check corpus statistics
        try:
            if (cres := int(stats[0].split()[-1])) != (clen := len(corpus)):
                if cres > clen:
                    return CheckResult.wrong(
                        "The number of outputted tokens is greater then the "
                        "number of tokens in the corpus. You should tokenize "
                        "the corpus by whitespaces and leave punctuation marks intact.")
                else:
                    return CheckResult.wrong(
                        "The number of outputted tokens is smaller then "
                        "the number of tokens in the corpus. You should "
                        "tokenize the corpus by whitespaces and leave punctuation marks intact.")
        except IndexError:
            return CheckResult.wrong("Invalid format. Make sure "
                                     "'Corpus statistics' is in a valid format.")
        except ValueError:
            return CheckResult.wrong("Value error. Make sure that each line in "
                                     "the corpus statistics section ends with an integer.")

        # see if for every inputted seed there is an output present
        seeds = attach.split('\n')[1:-2]
        if len(seeds) != len(res):
            return CheckResult.wrong("The number of inputted seeds should match "
                                     "the number of outputted results from the corpus.")

        for j, elem in enumerate(seeds):
            try:
                i = int(elem)
                out_tokens = re.split(r"\s+", res[j])
                if len(out_tokens) < 4:
                    return CheckResult.wrong(
                        "The output should be in the following format: "
                        "'Head: [head] Tail: [tail]' or it should be an error message")
                if corpus[i][0] != out_tokens[1] and corpus[i][1] != out_tokens[3]:
                    return CheckResult.wrong(
                        "Incorrect output ({0}). An other output ({1}) "
                        "is expected at index {2}".format(res[i], corpus[i], i))
            except IndexError:
                line = re.sub(r'\s', '', res[j].lower())
                if "indexerror" not in line:
                    return CheckResult.wrong(
                        "Error messages should contain the types of "
                        "errors (Index Error, Type Error, etc.)")
            except (ValueError, TypeError):
                line = re.sub(r'\s', '', res[j].lower())
                if "typerror" not in line:
                    return CheckResult.wrong("Error messages should contain the "
                                             "types of errors (Index Error, Type Error, etc.)")

        return CheckResult.correct()


if __name__ == '__main__':
    TextGeneratorTests('text_generator.text_generator').run_tests()
