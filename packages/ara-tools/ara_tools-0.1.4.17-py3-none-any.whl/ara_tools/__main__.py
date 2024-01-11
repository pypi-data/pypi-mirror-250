import os
import sys
import argparse
from ara_tools.artefact_creator import ArtefactCreator
from ara_tools.artefact_renamer import ArtefactRenamer
from ara_tools.filename_validator import is_valid_filename
from ara_tools.classifier_validator import is_valid_classifier
from ara_tools.template_manager import SpecificationBreakdownAspects
from ara_tools.artefact_deleter import ArtefactDeleter
from ara_tools.artefact_lister import ArtefactLister
from .prompt_handler import read_prompt, send_prompt, append_headings, write_prompt_result


def create_action(args):
    if args.parameter and args.classifier and args.aspect:
        sba = SpecificationBreakdownAspects()
        try:
            sba.create(args.parameter, args.classifier, args.aspect)
        except ValueError as ve:
            print(f"Error: {ve}")
            sys.exit(1)
        return
    if not is_valid_filename(args.parameter):
        print("Invalid filename provided. Please provide a valid filename.")
        sys.exit(1)
        return

    if not is_valid_classifier(args.classifier):
        print("Invalid classifier provided. Please provide a valid classifier.")
        sys.exit(1)
        return

    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    artefact_creator = ArtefactCreator()
    artefact_creator.run(args.parameter, args.classifier, template_path)

def delete_action(args):
    artefact_deleter = ArtefactDeleter()
    artefact_deleter.delete(args.parameter, args.classifier)


def rename_action(args):
    if not is_valid_filename(args.parameter):
        print("Invalid filename provided. Please provide a valid filename.")
        sys.exit(1)
        return

    if not is_valid_classifier(args.classifier):
        print("Invalid classifier provided. Please provide a valid classifier.")
        sys.exit(1)
        return

    if not is_valid_filename(args.aspect):
        print("Invalid new filename provided. Please provide a valid filename.")
        sys.exit(1)
        return

    artefact_renamer = ArtefactRenamer()
    artefact_renamer.rename(args.parameter, args.aspect, args.classifier)

def list_action(args):
    artefact_lister = ArtefactLister()
    if args.tags:
        artefact_lister.list_files(tags=args.tags)
    else:
        artefact_lister.list_files()
    

def prompt_action(args):
    if not args.classifier or not args.parameter:
        return
    classifier = args.classifier
    param = args.parameter

    prompt = read_prompt(classifier, param)
    if(prompt):
        append_headings(classifier, param, "prompt")
        write_prompt_result(classifier, param, prompt)
        response = send_prompt(prompt)
        append_headings(classifier, param, "result")
        write_prompt_result(classifier, param, response)


def cli():
    parser = argparse.ArgumentParser(description="Ara tools for creating files and directories.")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform (e.g. 'create', 'delete', 'list', 'rename')")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a file with a classifier and aspect")
    create_parser.add_argument("parameter", help="Filename for create action")
    create_parser.add_argument("classifier", help="Classifier for the file to be created")
    create_parser.add_argument("aspect", help="Specification breakdown aspect", nargs='?', default=None)  # aspect is now optional

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a file with a classifier")
    delete_parser.add_argument("parameter", help="Filename for delete action")
    delete_parser.add_argument("classifier", help="Classifier for the file to be deleted")

    # Rename command
    rename_parser = subparsers.add_parser("rename", help="Rename a file with a classifier and new filename")
    rename_parser.add_argument("parameter", help="Current filename for rename action")
    rename_parser.add_argument("classifier", help="Classifier for the file to be renamed")
    rename_parser.add_argument("aspect", help="New filename for the file")

    # List command
    list_parser = subparsers.add_parser("list", help="List files with optional tags")
    list_parser.add_argument("tags", nargs="*", help="Tags for listing files")

    # Prompt command
    prompt_parser = subparsers.add_parser("prompt", help="Send a prompt to ChatGPT and save the result")
    prompt_parser.add_argument("parameter", help="Filename for create action")
    prompt_parser.add_argument("classifier", help="Classifier for the file to be created")

    args = parser.parse_args()

    if args.action == "create":
        create_action(args)
    elif args.action == "delete":
        delete_action(args)
    elif args.action == "rename":
        rename_action(args)
    elif args.action == "list":
        list_action(args)
    elif args.action == "prompt":
        prompt_action(args)
    else:
        print("Invalid action provided. Type ara -h for help")
        sys.exit(1)
        return

if __name__ == "__main__":
    cli()
