from os import environ
from argparse import ArgumentParser
from dotenv import load_dotenv
from openai import OpenAI
from vt100logging import D, EX, vt100logging_init

SYSTEM_ROLE = "you are an experienced programmer and write blog posts about programming in Markdown"
SYSTEM_MODEL = "gpt-3.5-turbo"
DEFAULT_FRONT_MATTER_TIME = "07:00:00 -0000"
DEFAULT_RESPONSE_FILE_NAME = "response.md"


class Defaults:
    def __init__(self):
        load_dotenv()
        self.api_key = environ.get('AI_CLI_PAL_OPENAI_API_KEY')
        self.role = environ.get('AI_CLI_PAL_OPENAI_ROLE')
        self.model = environ.get('AI_CLI_PAL_OPENAI_MODEL')
        self.fron_matter_time = environ.get('AI_CLI_PAL_FRONT_MATTER_TIME')
        if self.role is None:
            self.role = SYSTEM_ROLE
        if self.model is None:
            self.model = SYSTEM_MODEL
        if self.fron_matter_time is None:
            self.fron_matter_time = DEFAULT_FRONT_MATTER_TIME


def parse_args(defaults: Defaults):
    parser = ArgumentParser()
    parser.add_argument('--question', '-q', type=str, default=None,
                        help="Provide your question here. If not provided, it will be asked interactively.")
    parser.add_argument('--model', '-m', type=str, default=defaults.model,
                        help=f"Provide your model here. If not provided, the model will be set to '{defaults.model}'.")
    parser.add_argument('--role', '-r', type=str, default=defaults.role,
                        help=f"Provide your role here. If not provided, the role will be set to '{defaults.role}'.")
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


def ask_question(question: str, api_key: str, model: str, role: str, quiet: bool) -> str:
    client = OpenAI(api_key=api_key)
    if not quiet:
        print("I'm thinking... In some situations this takes a while.")

    D("Creating a completion")
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": question}
        ]
    )

    return completion.choices[0].message.content


def ask_for_front_matter(front_matter_time: str):
    do_front_matter = bool(
        input("Do you wat to add front matter to the file? [y/N] ").lower() == 'y')
    if do_front_matter:
        title = input("Title: ")
        description = input("Description: ")
        categories = input("Categories (comma separated): ")
        date = input("Date (YYYY-MM-DD): ")
        date = date.strip().replace("/", "-").replace(".", "-").replace(" ", "-")
        return f"""---
title: {title}
description: {description}
categories: [{categories}]
date: {date} {front_matter_time}
---
""", title, date
    else:
        return "", None, None


def respond_to_question(response, save_to_file, dont_add_front_matter, front_matter_time, quiet) -> None:
    if not quiet:
        print("My response:")
        print(response)
    if save_to_file:
        file_name = DEFAULT_RESPONSE_FILE_NAME
        front_matter = ""
        if not dont_add_front_matter:
            front_matter, title, date = ask_for_front_matter(front_matter_time)
            title = title.replace(" ", "-")
            title = title.lower()
            if title and date:
                file_name = f"{date}-{title}.md"
            elif title:
                file_name = f"{title}.md"
            elif date:
                file_name = f"{date}-{DEFAULT_RESPONSE_FILE_NAME}.md"
        with open(f'{file_name}', 'w+') as f:
            f.write(front_matter)
            f.write(response)


def main():
    try:
        default_settings = Defaults()
        args = parse_args(default_settings)
        vt100logging_init('ai-cli-pal', is_verbose=args.verbose)
        print("Welcome to the your friendly AI assistant.")
        D(f"OpenAI model is '{args.model}'")
        D(f"AI assistant role is '{args.role}'")
        question = ""
        if args.question:
            question = args.question
        else:
            print("Ask me anything and I will try to answer it.")
            question = input("> ")
        response = ask_question(question, args.api_key,
                                args.model, args.role, args.quiet)
        respond_to_question(response, args.save,
                            args.no_front_matter, args.front_matter_time, args.quiet)
    except Exception as e:
        EX(e)


if __name__ == "__main__":
    main()
