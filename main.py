import os
from sen import PromptRequest


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


if __name__ == "__main__":
    call_and_response()
