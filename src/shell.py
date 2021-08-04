import processor
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Process StoryScript statements")
    parser.add_argument("-i", "--input", help="The file you wanted to process")
    parser.add_argument("--simulate-input-from-text-file", "-textsiminput", help="Simulate input using the specified file.")
    parser.add_argument("--release-mode", action="store_false" ,help="Enable release mode")
    args = parser.parse_args()
    processor.STORYSCRIPT_INTERPRETER_DEBUG_MODE = args.release_mode
    if args.input:
        processor.parse_file(args.input, args.simulate_input_from_text_file)
    else:

        class RequestExit(Exception):
            pass

        print("// StoryScript Shell //")
        print('Use "exit ()" (Without double quotes) or Press CTRL+C to exit')

        printNone = False

        try:
            while True:
                command = input("StoryScript > ")
                if command.endswith("/*"):
                    while True:
                        if input("... > ").endswith("*/"):
                            break
                if command.startswith("exit ("):
                    raise RequestExit
                if command.startswith("#define"):
                    scommand = command.split()
                    try:
                        if (
                            scommand[1] == "shellSettings"
                            and scommand[2] == "printWhenReturnNone"
                        ):
                            if scommand[3] == "true":
                                printNone = True
                                continue
                            if scommand[3] == "false":
                                printNone = False
                                continue
                    except IndexError:
                        print(
                            "InvalidSyntax: The Option you wanted to settings is required."
                        )
                out = processor.execute(command)
                if not printNone:
                    if out is not None:
                        print(out)
                else:
                    print(out)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt recieved. Exiting...")
        except RequestExit:
            print("Exiting requested. Exiting...")
        except Exception:  # skipcq: PYL-W0703
            from traceback import print_exc

            print_exc()
