from nltk.tokenize import regexp_tokenize


result_tokens = []
filename = input().strip()

token_exp = r"\S+"
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        result_tokens.extend(regexp_tokenize(line, token_exp))

result_set = set(result_tokens)

print("Corpus statistics")
print(f"All tokens: {len(result_tokens)}")
print(f"Unique tokens: {len(result_set)}")
print()

while True:
    inp = input()
    if inp == 'exit':
        break
    try:
        pos = int(inp)
        print(result_tokens[pos])
    except (TypeError, ValueError):
        print("Type Error. Please input an integer.")
    except IndexError:
        print("Index Error. Please input an integer that is in the range of the corpus.")