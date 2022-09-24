import jsonlines
import os

from sen import PromptRequest
from cxr.sociomathematics.clq import roles


def create_question(a, b):
    opt_n = 'n' if (roles[a].startswith('I') or roles[a].startswith('A')) else ''
    opt_role = 'as ' + roles[b].lower() if a != b else 'in its role'
    return f"Q: How does a{opt_n} {roles[a].lower()} function {opt_role}?\n\n"


def start_role_descriptions():
    p = PromptRequest(os.environ.get("OPENAI_API_KEY"))
    for i in range(10):
        for j in range(10):
            print(i, j)
            p["prompt"] = create_question(str(i), str(j))
            p.get_completion(add_continuance=False)
            with open(f"./roles/{i}.txt", "a+") as f:
                f.write(p["prompt"] + "" + p.last_request["choices"][0]["text"].strip() + "\n\n")


def call_and_response():
    """
    Simple cli-like interface for talking to DV-002
    """
    p = PromptRequest(os.environ.get('OPENAI_API_KEY'))
    while p.continue_:
        if p.gen_next:
            p.get_completion()
            print(p.last_request["choices"][0]["text"].replace("\n\n", "\n"))
        p.process_input(input(">>> "))


def view_current_completion():
    with jsonlines.open("./involutions/clq_fine_tune2.jsonl") as reader:
        o = {}
        i, j = 0, 0
        n = 0
        for obj in reader:
            i, j = n // 10, n % 10
            if j == 0:
                o[str(i)] = {}
            o[str(i)][str(j)] = obj
            n += 1
        print(o)

    # inp = input(">>> ")


if __name__ == "__main__":
    call_and_response()
