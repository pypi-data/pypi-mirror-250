#!/usr/bin/env python3
import argparse
import json
import logging
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Union

from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

# Get the environment variable, with a fallback default value
partial_config_path = os.getenv("PARTIAL_CONFIG_PATH", "~/.config/partial/")

# Expand the user's home directory (`~`) to an absolute path
config_path = Path(os.path.expanduser(partial_config_path))

# Create folder if it does not exist
if not os.path.exists(config_path):
    os.makedirs(config_path)

code_base_path = config_path / Path("./codes")
pipeline_base_path = config_path / Path("./pipelines")


# Check if OPENAI_API_KEY is set
if "OPENAI_API_KEY" not in os.environ:
    print(
        "OPENAI_API_KEY environment variable need to be set with the API key\nCommand: export OPENAI_API_KEY=<API_KEY>"
    )
    sys.exit(1)


llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.8)


class Modes(Enum):
    LLM = "LLM"
    CODE = "CODE"


class InstructionMetadata(BaseModel):
    instruction: str
    mode: Union[Modes, None] = None


class PipelineConfig(BaseModel):
    instructions: list[InstructionMetadata]
    codes: dict[str, str]
    repeat: int = 1


class ImplementationMode(BaseModel):
    mode: str = Field(description="The mode to use: LLM or CODE")


def detect_mode_chain() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a system to transform data, you have the choice between two mode: LLM mode or Code mode.
            Some instructions can be hard to implement it as code, so in the case it does not suits for code mode, you can use LLM mode.
            The LLM mode is more approriate for instructions that are not deterministic. Chose the correct mode for the instruction.
                """,
            ),
            ("human", "INSTRUCTION: {instruction}"),
            ("human", "DATA: {data}"),
            ("human", "Chose the MODE:"),
        ]
    )
    chain = create_structured_output_chain(
        ImplementationMode,
        llm,
        prompt,
        verbose=False,
    )
    return chain


class PythonCode(BaseModel):
    code: str = Field(description="The code generated to transform the data")


def gen_code_chain() -> ChatPromptTemplate:
    # instruction: str, data: str, header: Union[str, None]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a system to transform data and you have to write the code for it",
            ),
            (
                "system",
                "You have access to the following data: data is a dictionary with the data to transform",
            ),
            (
                "system",
                "Put all the import of the libraries you need inside the function",
            ),
            (
                "system",
                "Dont't write the code inside backticks",
            ),
            (
                "system",
                "Write the code to transform the data based on the instruction, generate just the code to transform the data inplace.",
            ),
            (
                "system",
                """Output only the code like that:
                CODE TO RETURN EXAMPLE:
                name_parts = data['name'].split()
                data['first_name'] = name_parts[0]
                data['last_name'] = name_parts[1]
                del data['name']
                """,
            ),
            (
                "system",
                "The created data should always be returned in the variable data, create new fields or modify existing fields if required.",
            ),
            ("human", "DATA: {data}"),
            ("human", "INSTRUCTION: {instruction}"),
        ]
    )
    # prompt.partial(data=data, instruction=instruction)

    chain = create_structured_output_chain(
        PythonCode,
        llm,
        prompt,
        verbose=False,
    )
    return chain


def gen_code(chain, instruction: str, data: str):
    res = chain.invoke({"data": data, "instruction": instruction})
    code = res["function"].code
    return code


def transform_chain(
    instruction: str, data: str, header: Union[str, None], prev: str
) -> ChatPromptTemplate:
    messages = [
        (
            "system",
            "Act as a system to transform data, always print the full data, only output the data. No comment or exaplanation. Just the data transformed. Respect the order, do not print again the header",
        ),
        (
            "system",
            "If the data is the header just print the header with the instruction applied. Just output the header no prefix or suffix text",
        ),
        (
            "system",
            "Be consistent with data format and field name that you already generated, in the previous steps. But you have to answer the instruction for the current step. Only be based on the previous data to enforce the format not the content.",
        ),
        ("ai", "PREVIOUS DATA KEYS: {prev}"),
        ("human", "DATA: {data}"),
        ("human", "INSTRUCTION: {instruction}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    if header is not None:
        messages.extend(("human", "HEADER: {header}"))
        prompt = prompt.partial(
            data=data, instruction=instruction, header=header, prev=prev
        )
    else:
        prompt = prompt.partial(data=data, instruction=instruction, prev=prev)
    return prompt


def execute_step(
    instruction: str, data: str, header: str | None, prev: str | None
) -> str:
    prompt = transform_chain(instruction, data, header, prev)
    chain = prompt | llm
    output = chain.invoke({})
    content = output.content
    return content


def lowercase_and_replace(s):
    s = s.lower().replace(" ", "_")
    # Remove special characters except for underscore
    return re.sub(r"[^a-z0-9_]", "", s)


def get_args():
    parser = argparse.ArgumentParser(description="LLM Pipe")

    subparser = parser.add_subparsers(dest="command", help="Available commands")

    subparser.add_parser("store", help="Display the functions in the store")
    subparser.add_parser("config", help="Display the configuration location")

    # Pipelines
    pipelines_parser = subparser.add_parser(
        "pipelines", help="Display the available pipelines"
    )
    pipelines_subparser = pipelines_parser.add_subparsers(
        dest="pipelines_command", help="Available commands"
    )
    pipelines_subparser.add_parser("ls", help="Display the available pipelines")
    pipelines_rm_parser = pipelines_subparser.add_parser("rm", help="Remove a pipeline")
    pipelines_rm_parser.add_argument("pipeline", help="The pipeline to remove")
    pipeline_show_parser = pipelines_subparser.add_parser(
        "show", help="Display the pipeline"
    )
    pipeline_show_parser.add_argument("pipeline", help="The pipeline to display")

    parser.add_argument(
        "--instructions",
        "-i",
        required=False,
        action="append",
        help="Instruction for the LLM",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Debug mode, write to debug file",
    )
    parser.add_argument(
        "--code",
        "-c",
        action="store_true",
        help="Generate code to execute the transformation",
    )
    parser.add_argument(
        "--llm",
        "-l",
        action="store_true",
        help="Use LLM to execute the transformation",
    )
    parser.add_argument(
        "--pipeline",
        "-p",
        help="Use a pipeline over the data",
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Read the input data from a file",
    )
    parser.add_argument(
        "--repeat",
        "-r",
        type=int,
        choices=range(1, 10),
        default=1,
        help="Repeat the instruction multiple time",
    )
    return parser, parser.parse_args()


def write_code_file(code, instruction):
    code_filename = lowercase_and_replace(instruction) + ".py"

    # Create folder if it does not exist
    if not os.path.exists(code_base_path):
        os.makedirs(code_base_path)

    with open(code_base_path / code_filename, "w") as f:
        f.write(code)


def is_code_file_exists(instruction):
    code_filename = lowercase_and_replace(instruction) + ".py"
    return os.path.exists(code_base_path / code_filename)


def read_code_file(instruction):
    code_filename = lowercase_and_replace(instruction) + ".py"
    with open(code_base_path / code_filename, "r") as f:
        code = f.read()
    return code


def show_store():
    print("Codes:", code_base_path)
    for filename in os.listdir(code_base_path):
        if filename.endswith(".py"):
            print("- ", filename[:-3])
    print("")
    print("Pipelines:", pipeline_base_path)
    for filename in os.listdir(pipeline_base_path):
        if filename.endswith(".json"):
            print("- ", filename[:-5])


def list_pipelines():
    print("Pipelines:", pipeline_base_path)
    for filename in os.listdir(pipeline_base_path):
        if filename.endswith(".json"):
            print("- ", filename[:-5])


def show_config():
    print("Location:", config_path)
    print("")
    print("Environment variables:")
    print(
        "- PARTIAL_CONFIG_PATH",
        "\tis set" if os.getenv("PARTIAL_CONFIG_PATH") else "\tnot set",
        "\tcurrent:",
        partial_config_path,
    )
    print(
        "- OPENAI_API_KEY", "\tis set" if os.getenv("OPENAI_API_KEY") else "\tnot set"
    )


def create_pipeline(instructions: list[InstructionMetadata], codes: dict = {}):
    if not os.path.exists(pipeline_base_path):
        os.makedirs(pipeline_base_path)

    filename = instructions[0].instruction
    pipeline_filename = lowercase_and_replace(filename) + ".json"

    pipeline = PipelineConfig(instructions=instructions, codes=codes)

    with open(pipeline_base_path / pipeline_filename, "w") as f:
        f.write(pipeline.json(indent=4))


def write_to_code_store(store, code, instruction):
    code_name = lowercase_and_replace(instruction)
    store[code_name] = code
    return store


def get_code_store(store, instruction):
    code_name = lowercase_and_replace(instruction)
    return store.get(code_name)


def parse_incremental(data):
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(data):
        try:
            obj, pos = decoder.raw_decode(data, pos)
            yield obj
        except json.JSONDecodeError:
            pos += 1


def validate_args(args):
    valid_args = args.instructions or args.pipeline
    if not valid_args:
        return False
    return True


def read_input(args):
    """
    Read input data based on the arguments.
    """

    if args.file:
        with open(args.file, "r") as f:
            return parse_incremental(f.read())
    else:
        return parse_incremental(sys.stdin.read())


def init_pipeline(args):
    code_store = {}
    if args.llm:
        mode = Modes.LLM
    elif args.code:
        mode = Modes.CODE
    else:
        mode = None
    instructions = [
        InstructionMetadata(instruction=i, mode=mode) for i in args.instructions
    ]
    repeat = args.repeat

    return PipelineConfig(codes=code_store, instructions=instructions, repeat=repeat)


def load_pipeline(pipeline):
    if pipeline.endswith(".json"):
        pipeline_file = pipeline
    else:
        pipeline_file = pipeline_base_path / (pipeline + ".json")
    if not os.path.exists(pipeline_file):
        print("Pipeline file not found:", pipeline_file)
        sys.exit(1)
    pipeline = PipelineConfig.parse_file(pipeline_file)
    return pipeline


def detect_instruction_mode(instruction, data):
    detect_mode = detect_mode_chain()
    mode_detected = detect_mode.invoke({"instruction": instruction, "data": data})
    mode = Modes.LLM if mode_detected["function"].mode.upper() == "LLM" else Modes.CODE
    return mode


def execute_llm(prev_data, line, instruction):
    prev_data = prev_data or line
    prev_keys = ",".join(prev_data.keys())
    line = json.dumps(line)
    output = execute_step(
        instruction=instruction, data=line, header=None, prev=prev_keys
    )
    logging.debug(f"OUTPUT LLM: {output}")

    if "{" in output:
        output = output[output.index("{") :]
    else:
        output = json.dumps({"output": output})
    return output


def execute_code(pipeline, line, instruction):
    # lookup for the code in the store or generate it
    if get_code_store(pipeline.codes, instruction) is None and not is_code_file_exists(
        instruction
    ):
        logging.debug("Generating code")
        chain = gen_code_chain()
        code = gen_code(chain, instruction, line)

        write_code_file(code, instruction)
        write_to_code_store(pipeline.codes, code, instruction)
        logging.debug("Code generated and saved")

    code = get_code_store(pipeline.codes, instruction) or read_code_file(instruction)
    logging.debug(f"CODE: {code}")

    # save the code in the store
    pipeline.codes[lowercase_and_replace(instruction)] = code

    # peprare data for the code execution
    line_data = json.loads(line) if isinstance(line, str) else line
    vars = {"data": line_data}

    # execute the code
    try:
        logging.debug(
            f"Executing code: {code}",
        )
        exec(code, vars)
    except Exception:
        logging.exception(
            "Error while executing the code:\n"
            + "INSTRUCTION: "
            + instruction
            + "\n"
            + "DATA: "
            + str(line_data)
            + "\n"
            + "CODE:\n"
            + code
            + "\n\n"
        )

        sys.stderr.write(
            "Error while executing the code:\n"
            + "INSTRUCTION: "
            + instruction
            + "\n"
            + "DATA: "
            + str(line_data)
            + "\n"
            + "CODE:\n"
            + code
            + "\n\n"
        )
        sys.exit(1)
    output_dict = vars["data"]
    output = json.dumps(output_dict)
    return output


def print_output(output):
    # Check if last char is a new line
    if output[-1] == "\n":
        sys.stdout.write(output)
    else:
        sys.stdout.write(output + "\n")


def process_line(line, pipeline):
    prev_data = None

    for instruciton in pipeline.instructions:
        mode = instruciton.mode or detect_instruction_mode(
            instruciton.instruction, line
        )
        instruciton.mode = mode

        logging.debug(
            f"INPUT: {line} INSTRUCTION: {instruciton.instruction} MODE: {mode.value}"
        )

        if mode == Modes.LLM:
            output = execute_llm(prev_data, line, instruciton.instruction)
        else:
            output = execute_code(pipeline, line, instruciton.instruction)

        logging.debug(f"OUTPUT: {output}")
        # Pass the output to the next step
        line = output
        # Help the next step by passing the previous data
        prev_data = json.loads(output)

    return output


def process_data(lines, pipeline):
    for line in lines:
        for ri in range(pipeline.repeat):
            logging.debug(f"REPEAT ITERATION: {ri}")
            output = process_line(line, pipeline)
            print_output(output)


def resolve_pipeline(pipeline):
    if pipeline.endswith(".json"):
        pipeline_file = pipeline
    else:
        pipeline_file = pipeline_base_path / (pipeline + ".json")
    if not os.path.exists(pipeline_file):
        print("Pipeline file not found:", pipeline_file)
        sys.exit(1)
    return pipeline_file


def remove_pipeline(pipeline):
    print("Remove pipeline:", pipeline)
    pipeline_file = resolve_pipeline(pipeline)
    os.remove(pipeline_file)
    print("Pipeline removed")


def show_pipeline(pipeline):
    pipeline_file = resolve_pipeline(pipeline)
    with open(pipeline_file, "r") as f:
        pipeline_data = json.loads(f.read())
        display_pipeline(pipeline, pipeline_file, pipeline_data)


def display_pipeline(name, filepath, pipeline_data):
    print(f"Pipeline: {name}\nFile: {filepath}\n-------------------")

    # Print instructions
    print("Instructions:")
    for i, instruction in enumerate(pipeline_data["instructions"], 1):
        print(f"  {i}. {instruction['instruction']} (Mode: {instruction['mode']})")

    # Print codes
    print("\nCodes:")
    for name, code in pipeline_data["codes"].items():
        print(f"- {name}:\n\n    {code.replace('\n', '\n    ')}")

    # Other details
    print(f"\nRepeat: {pipeline_data['repeat']}")


def pipeline_command(args):
    if args.pipelines_command == "rm":
        remove_pipeline(args.pipeline)
    elif args.pipelines_command == "ls":
        list_pipelines()
    elif args.pipelines_command == "show":
        show_pipeline(args.pipeline)
    else:
        list_pipelines()


def main():
    parser, args = get_args()

    if args.command == "store":
        show_store()
        return
    elif args.command == "pipelines":
        pipeline_command(args)
        return
    elif args.command == "config":
        show_config()
        return

    if not validate_args(args):
        parser.print_help()
        return

    if args.debug:
        logging.basicConfig(
            filename=config_path / "debug.log",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            filename=config_path / "debug.log",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

    logging.debug("debug mode enabled")

    input_data = read_input(args)

    if args.pipeline:
        pipeline = load_pipeline(args.pipeline)
    else:
        pipeline = init_pipeline(args)

    process_data(input_data, pipeline)

    create_pipeline(pipeline.instructions, pipeline.codes)


if __name__ == "__main__":
    main()
