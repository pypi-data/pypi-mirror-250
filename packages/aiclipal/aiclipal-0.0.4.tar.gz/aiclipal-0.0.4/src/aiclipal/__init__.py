from .aiclipal import main, ask_question


def ai_cli_pal_ask_question(question, api_key, model, role, quiet):
    return ask_question(question, api_key, model, role, quiet)


def ai_cli_pal_main():
    main()
