import ast
from datetime import datetime
import json
import os
import requests


def get_num(date):
    o = 0
    for file in os.listdir("./chats"):
        if file.startswith(date):
            o += 1
    return o


class PromptRequest:
    def __init__(  # Probably shoulda used **kwargs, but whatever
            self,
            api_key,
            model="text-davinci-002",
            prompt="",
            suffix="[/]",
            max_tokens=64,
            temperature=0.7,
            top_p=1,
            n=1,
            stream=False,
            logprobs=None,
            echo=False,
            stop=None,
            presence_penalty=0,
            frequency_penalty=0,
            best_of=1,
            logit_bias={},
            user="Conrad"
    ):
        self.api_key = api_key
        self.request_body = {
            "model": model,
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens":  max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "logprobs": logprobs,
            "echo": echo,
            "stop": stop,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "best_of": best_of,
            "logit_bias": logit_bias,
            "user": user
        }
        self.logprobs = []
        self.last_request = {}
        self.continue_ = True
        self.gen_next = False
        self.date = datetime.now().strftime("%Y-%m-%d")

    def __getitem__(self, item):
        return self.request_body[item]

    def __setitem__(self, key, value):
        self.request_body[key] = value

    def __iter__(self):
        return iter(self.request_body.keys())

    def __str__(self):
        return str(self.request_body)

    def get_completion(self, add_continuance=True):
        endpoint = "https://api.openai.com/v1/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        r = requests.post(
            endpoint,
            data=json.dumps(self.request_body),
            headers=headers
        )
        completion = r.json()
        if self["n"] == 1 and add_continuance:
            self["prompt"] += completion["choices"][0]["text"]
        if self["n"] == 1 and self["logprobs"]:
            self.logprobs.append(completion["choices"][0]["logprobs"])
        self.last_request = r.json()
        self.gen_next = False

    def process_input(self, inp):
        if inp.startswith("/"):
            spl = inp.split(" ", 1)
            cmd = spl[0][1:]
            val = spl[1] if len(spl) > 1 else ""

            if cmd == "help":
                with open("./colloquialisations/help.txt", "r") as f:
                    print(f.read())

            elif cmd == "new":  # Reset prompt to optional new value
                self["prompt"] = val

            elif cmd == "exit":  # Exit the program
                self.continue_ = False
                try:
                    file = f"./chats/{self.date}-{get_num(self.date)}.txt"
                    print(file)
                    with open(file, "w+") as f:
                        f.write(self["prompt"] + "\n")
                except FileNotFoundError:
                    print("Oops! You forgot to create a /chats/ folder")

            elif cmd == "inject":  # Inject the contents of a file into the prompt
                try:
                    with open(f"./{val}", "r") as f:
                        self["prompt"] += "\n\n" + f.read()
                except FileNotFoundError:
                    print(f"Oops! ./{val} does not exist.")

            elif cmd == "clq":  # Add a tagged colloquialisation to the prompt
                tag, file = val.split(" ", 1)
                try:
                    with open(f"./{file}", "r") as f:
                        self["prompt"] += f"\n\n[{tag}]\n\n" + f.read() + f"\n\n[/{tag}]\n\n"
                except FileNotFoundError:
                    print(f"Oops! ./{file} does not exist.")

            elif cmd in self:  # Alter a parameter of the request
                new_val = ast.literal_eval(val)
                self[cmd] = new_val
                print(f"Amended {cmd} to {type(new_val)} {new_val}")

            else:  # Ya done did it now
                print(f"Invalid command '{cmd}'")

        else:
            self["prompt"] += "\n\n" + inp
            self.gen_next = True
