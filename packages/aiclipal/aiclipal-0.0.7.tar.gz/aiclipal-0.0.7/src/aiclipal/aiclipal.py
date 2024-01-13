from os import environ
from argparse import ArgumentParser
from dotenv import load_dotenv
from openai import OpenAI
from vt100logging import D, EX, E, vt100logging_init
from datetime import datetime
from signal import signal, SIGINT
import string

SYSTEM_PERSONALITY = "you are an experienced programmer and write blog posts about programming in Markdown"
SYSTEM_MODEL = "gpt-3.5-turbo-1106"
DEFAULT_FRONT_MATTER_TIME = "07:00:00 -0000"
DEFAULT_RESPONSE_FILE_NAME = "response"
DEFAULT_MAX_TOKENS = 4096


class AiCliPalDefaults:
    def __init__(self):
        load_dotenv()
        self.api_key = environ.get('AI_CLI_PAL_OPENAI_API_KEY')
        self.personality = environ.get('AI_CLI_PAL_OPENAI_ROLE')
        self.model = environ.get('AI_CLI_PAL_OPENAI_MODEL')
        self.fron_matter_time = environ.get('AI_CLI_PAL_FRONT_MATTER_TIME')
        if self.personality is None:
            self.personality = SYSTEM_PERSONALITY
        if self.model is None:
            self.model = SYSTEM_MODEL
        if self.fron_matter_time is None:
            self.fron_matter_time = DEFAULT_FRONT_MATTER_TIME


def parse_args(defaults: AiCliPalDefaults):
    parser = ArgumentParser()
    parser.add_argument('--question', '-q', type=str, default=None,
                        help="Provide your question here. If not provided, it will be asked interactively.")
    parser.add_argument('--model', '-m', type=str, default=defaults.model,
                        help=f"Provide your model here. If not provided, the model will be set to '{defaults.model}'.")
    parser.add_argument('--personality', '-r', type=str, default=defaults.personality,
                        help=f"Provide asistant's personality here. If not provided, the personality will be set to '{defaults.personality}'.")
    parser.add_argument('--api-key', '-k', type=str,
                        default=defaults.api_key,
                        help="Provide your API key here. If not provided, it will be read from the OPENAI_API_KEY environment variable.")
    parser.add_argument('--save', '-s', action='store_true', default=False,
                        help="Save the response to a file.")
    parser.add_argument('--front-matter-time', '-t', type=str, default=defaults.fron_matter_time,
                        help=f"Provide the time for the front matter here. If not provided, the time will be set to '{defaults.fron_matter_time}'.")
    parser.add_argument('--no-front-matter', action='store_true',
                        default=False, help='Do not add front matter to the saved file.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        default=False, help='Verbose output.')
    parser.add_argument('--quiet', action='store_true',
                        default=False, help='Quiet output.')
    args = parser.parse_args()
    return args


class AiCliPalEntity:
    def __init__(self, api_key: str, personality: str, model: str = SYSTEM_MODEL) -> None:
        self.api_key = api_key
        self.model = model
        self.personality = personality
        self.messages = []
        self.reset_messages()

    def __append_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def reset_messages(self) -> None:
        self.messages = []
        self.__append_message("system", self.personality)

    def add_user_message(self, content: str) -> None:
        self.__append_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        self.__append_message("assistant", content)

    def ask_question(self, question: str, quiet: bool = False) -> str:
        self.add_user_message(question)
        client = OpenAI(api_key=self.api_key)
        D("Creating a completion")
        completion = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=not quiet
        )
        response = ""
        if quiet:
            response = completion.choices[0].message.content
        else:
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content is not None:
                    response += content
                    print(content, end="")
        self.add_assistant_message(response)
        return response

    def get_last_response(self) -> str:
        return self.messages[-1]["content"]


def ask_for_front_matter(front_matter_time: str):
    title = input("Title: ")
    description = input("Brief: ")
    categories = input("Categories (comma separated): ")
    date = input(f"Date (YYYY-MM-DD) (default today): ")
    time = input(f"Time (HH:MM:SS) (default {front_matter_time}): ")
    date = date.strip().replace("/", "-").replace(".", "-").replace(" ", "-")
    time = time.strip().replace(".", ":").replace(" ", ":")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    if not time:
        time = front_matter_time
    return f"""---
title: {title}
brief: {description}
categories: [{categories}]
date: {date} {time} -0000
---
""", title, date


def compose_file_name(title: str, date: str):
    if not title:
        title = DEFAULT_RESPONSE_FILE_NAME
    else:
        translation_table = str.maketrans(
            "+", "plus", string.punctuation.replace("-", "").replace("+", ""))
        title = title.translate(translation_table)
        title = title.lower()
    return f"{date}-{title}.md"


def save_response(response, add_front_matter, front_matter_time) -> None:
    file_name = f"{DEFAULT_RESPONSE_FILE_NAME}.md"
    front_matter = ""
    if add_front_matter:
        front_matter, title, date = ask_for_front_matter(front_matter_time)
        file_name = compose_file_name(title, date)
    with open(f'{file_name}', 'w+') as f:
        f.write(front_matter)
        f.write(response)


def ctrl_c_handler(signal, frame):
    print('\n\nYou pressed Ctrl+C!')
    exit(0)


def print_help():
    print("Type '!help' to see this message.")
    print("Type '!file <file_name>' Inside your question to fetch the file content in-place.")
    print("Type '!save' to save the last output to a file.")
    print("Type '!reset' to reset the conversation.")
    print("Type '!exit' to exit the program.")


def inject_text_file_content_into_question_with_file_command(question: str) -> str:
    file_command = '!file'
    position = question.find(file_command)+len(file_command)+1
    file_name = question[position:].split(' ')[0]
    file_content = ''
    with open(file_name, 'r') as f:
        file_content = f.read()
    return question.replace(file_command, '').replace(
        file_name, f"\n{file_content}")


def main():
    try:
        signal(SIGINT, ctrl_c_handler)
        default_settings = AiCliPalDefaults()
        args = parse_args(default_settings)
        vt100logging_init('ai-cli-pal', is_verbose=args.verbose)
        if args.api_key is None:
            E("Please provide your API key.")
            exit(1)

        print("Welcome to the your friendly AI assistant.")
        print_help()
        D(f"OpenAI model is '{args.model}'")
        D(f"AI assistant personality is '{args.personality}'")

        ai = AiCliPalEntity(args.api_key, args.personality, args.model)
        if args.question is not None:
            ai.ask_question(args.question, args.quiet)
            if args.save:
                save_response(ai.get_last_response(),
                              not args.no_front_matter, args.front_matter_time)
            exit(0)
        while True:
            question = input("\n\n> ")
            if question == "!exit":
                break
            elif question == "!reset":
                ai.reset_messages()
                continue
            elif question == "!save":
                save_response(ai.get_last_response(),
                              not args.no_front_matter, args.front_matter_time)
                continue
            elif question == "!help":
                print_help()
                continue
            elif '!file' in question:
                question = inject_text_file_content_into_question_with_file_command(
                    question)
            ai.ask_question(question, args.quiet)
    except Exception as e:
        EX(e)


if __name__ == "__main__":
    main()
