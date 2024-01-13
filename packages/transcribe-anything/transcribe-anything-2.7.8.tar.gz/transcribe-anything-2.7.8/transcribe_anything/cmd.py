"""
    Entry point for running the transcribe-anything prgram.
"""

# flake8: noqa E501

import argparse
import sys
import os
import traceback

from transcribe_anything.api import transcribe
from transcribe_anything.whisper import get_computing_device
from transcribe_anything.parse_whisper_options import parse_whisper_options

os.environ["PYTHONIOENCODING"] = "utf-8"

WHISPER_MODEL_OPTIONS = [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large-legacy",
    "large",
    "large-v2",
    "large-v3"
]

def main() -> int:
    """Main entry point for the command line tool."""
    whisper_options = parse_whisper_options()
    device = get_computing_device()
    help_str = (
        f'transcribe_anything is using a "{device}" device.'
        " Any unrecognized args are assumed to be for whisper"
        " ai and will be passed as is to whisper ai."
    )
    parser = argparse.ArgumentParser(description=help_str)
    parser.add_argument(
        "url_or_file",
        help="Provide file path or url (includes youtube/facebook/twitter/etc)",
    )
    parser.add_argument(
        "--output_dir",
        help="Provide output directory name,d efaults to the filename of the file.",
        default=None,
    )
    parser.add_argument(
        "--model",
        help="name of the Whisper model to us",
        default="small",
        choices=WHISPER_MODEL_OPTIONS,
    )
    parser.add_argument(
        "--task",
        help="whether to perform transcription or translation",
        default="transcribe",
        choices=whisper_options["task"],
    )
    parser.add_argument(
        "--language",
        help="language to the target audio is in, default None will auto-detect",
        default=None,
        choices=[None] + whisper_options["language"],
    )
    parser.add_argument(
        "--device",
        help="device to use for processing, None will auto select CUDA if available or else CPU",
        default=None,
        choices=[None, "cpu", "cuda", "insane"],
    )
    parser.add_argument(
        "--embed",
        help="whether to embed the translation file into the output file",
        action="store_true",
    )
    # add extra options that are passed into the transcribe function
    args, unknown = parser.parse_known_args()
    if args.model == "large-legacy":
        args.model = "large"
    elif args.model == "large":
        args.model = "large-v3"

    if unknown:
        print(f"Unknown args: {unknown}")
    print(f"Running transcribe_audio on {args.url_or_file}")
    try:
        transcribe(
            url_or_file=args.url_or_file,
            output_dir=args.output_dir,
            model=args.model if args.model != "None" else None,
            task=args.task,
            language=args.language if args.language != "None" else None,
            device=args.device,
            embed=args.embed,
            other_args=unknown,
        )
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        return 1
    except Exception as e:  # pylint: disable=broad-except
        stack = traceback.format_exc()
        sys.stderr.write(f"Error: {e}\n{stack}\nwhile processing {args.url_or_file}\n")
        return 1
    return 0


if __name__ == "__main__":
    # push sys argv prior to call
    sys.argv.append("test.wav")
    sys.argv.append("--model")
    sys.argv.append("large")
    sys.argv.append('--initial_prompt "What is your name?"')
    sys.exit(main())
