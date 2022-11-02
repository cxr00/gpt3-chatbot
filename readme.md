# GPT3 chatbot by Complexor

## Quickstart

* Add your OpenAI API Key to your system environment variables with the name "OPENAI_API_KEY"
* Run `main.py`
* Chat with GPT3!
* Type `/exit` to end your chat and save the results to `/chats/`. It will automatically name it using `YYYY-MM-DD-#.txt` format

## Customisation

In `main.py`, you can add keyword arguments to the constructor for your `PromptRequest` object to change the parameters of GPT3. The parameters are as follows:

* model="text-davinci-002",
* prompt
* suffix
* max_tokens=64
* temperature=0.7
* top_p
* n=1
* logprobs=None
* echo
* stop
* presence_penalty
* frequency_penalty
* best_of
* logit_bias
* user="Conrad"

## Colloquialisations

A **colloquialisation** is a set of preliminary information which you want the bot to have in advance of your communication. It can be definitions, writing prompts, instructions on how to process input, you name it. Use the command `/clq [filename]` and it will pull the appropriate file from the `/colloquialisations/` folder.

## Commands

You can type `/help` to see a full list of available commands. Included are general commands to change the model's variables. For example, you can type `/log_probs True` to have the model start returning probabilities, or `/temperature 1.0` to adjust randomness/determinism.
