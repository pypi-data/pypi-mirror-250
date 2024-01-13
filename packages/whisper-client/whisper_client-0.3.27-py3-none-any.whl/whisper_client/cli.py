import json
import sys
from pathlib import Path
import argparse
from enum import Enum
from typing import Optional
import tkinter as tk

from whisper_client.main import WhisperClient, Mode, Scheme

parser = argparse.ArgumentParser()

parser.add_argument("-k", "--api-key", type=str, help="API key for the whisper API")

parser.add_argument("-s", "--api-scheme", type=str, default="https", help="API scheme for the whisper API")
parser.add_argument("-u", "--api-url", type=str, default=None, help="API url for the whisper API")
parser.add_argument("-p", "--api-port", type=int, default=443, help="API port for the whisper API")

parser.add_argument("-i", "--input", type=str, default=None, help="Input file to send to the API")
parser.add_argument("-o", "--output", type=str, default=None, help="Output file to save the result")

parser.add_argument("-f", "--folder", type=bool, default=False, help="Folder mode")
parser.add_argument("--video", type=bool, default=False, help="Video mode")

parser.add_argument("--stdout", action="store_true", help="Print the result to stdout")
parser.add_argument("--stderr", action="store_true", help="Print the result to stderr")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

parser.add_argument("-m", "--mode", type=str, default="full",
                    help="Mode for the API, can be 'full', 'text', 'segments' and/or 'words' (comma separated)")

parser.add_argument("-c", "--config", type=str, default=None,
                    help="Config file for the whisper API, by default it is .whisperrc in the current directory "
                         "or in the home directory")
parser.add_argument("--overwrite-config", action="store_true",
                    help="Overwrite config file with the current arguments (if the --config argument isn't provided,"
                         " this will overwrite the default config file which is .whisperrc in the current directory"
                         " or in the home directory")

parser.add_argument("--no-verify", action="store_true", help="Do not verify the SSL certificate")
parser.add_argument("--no-skip", action="store_true", help="Do not skip already downloaded files")
parser.add_argument("--interval", type=int, default=100, help="Interval between two status checks")
parser.add_argument("--version", action="store_true", help="Print the version of the client")

parser.add_argument("--gui", action="store_true", help="Launch the GUI")


class Type(Enum):
    VIDEO = "video"
    AUDIO = "audio"


class FileMode(Enum):
    FILE = "file"
    FOLDER = "folder"


class WhisperGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Whisper Client")

        self.api_key = tk.StringVar()
        self.api_scheme = tk.StringVar()
        self.api_url = tk.StringVar()
        self.api_port = tk.IntVar()

        self.input = tk.StringVar()
        self.output = tk.StringVar()

        self.folder = tk.BooleanVar()
        self.video = tk.BooleanVar()

        self.stdout = tk.BooleanVar()
        self.stderr = tk.BooleanVar()
        self.verbose = tk.BooleanVar()

        self.mode = tk.StringVar()

        self.config = tk.StringVar()
        self.overwrite_config = tk.BooleanVar()

        self.no_verify = tk.BooleanVar()
        self.no_skip = tk.BooleanVar()
        self.interval = tk.IntVar()

        self.api_scheme.set("https")
        self.api_port.set(443)
        self.mode.set("full")
        self.interval.set(100)

        self.api_scheme.trace("w", self.update_api_url)

        self.gui()

        self.mainloop()

    def gui(self):
        tk.Label(self, text="API Key").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.api_key).grid(row=0, column=1)

        tk.Label(self, text="API Scheme").grid(row=1, column=0)
        tk.OptionMenu(self, self.api_scheme, "https", "http").grid(row=1, column=1)

        tk.Label(self, text="API URL").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.api_url).grid(row=2, column=1)

        tk.Label(self, text="API Port").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.api_port).grid(row=3, column=1)

        tk.Label(self, text="Input").grid(row=4, column=0)
        tk.Entry(self, textvariable=self.input).grid(row=4, column=1)

        tk.Label(self, text="Output").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.output).grid(row=5, column=1)

        tk.Label(self, text="Folder").grid(row=6, column=0)
        tk.Checkbutton(self, variable=self.folder).grid(row=6, column=1)

        tk.Label(self, text="Video").grid(row=7, column=0)
        tk.Checkbutton(self, variable=self.video).grid(row=7, column=1)

        tk.Label(self, text="Stdout").grid(row=8, column=0)
        tk.Checkbutton(self, variable=self.stdout).grid(row=8, column=1)

        tk.Label(self, text="Stderr").grid(row=9, column=0)
        tk.Checkbutton(self, variable=self.stderr).grid(row=9, column=1)

        tk.Label(self, text="Verbose").grid(row=10, column=0)
        tk.Checkbutton(self, variable=self.verbose).grid(row=10, column=1)

        tk.Label(self, text="Mode").grid(row=11, column=0)
        tk.Entry(self, textvariable=self.mode).grid(row=11, column=1)

        tk.Label(self, text="Config").grid(row=12, column=0)
        tk.Entry(self, textvariable=self.config).grid(row=12, column=1)

        tk.Label(self, text="Overwrite Config").grid(row=13, column=0)
        tk.Checkbutton(self, variable=self.overwrite_config).grid(row=13, column=1)

        tk.Label(self, text="No Verify").grid(row=14, column=0)
        tk.Checkbutton(self, variable=self.no_verify).grid(row=14, column=1)

        tk.Label(self, text="No Skip").grid(row=15, column=0)
        tk.Checkbutton(self, variable=self.no_skip).grid(row=15, column=1)

        tk.Label(self, text="Interval").grid(row=16, column=0)
        tk.Entry(self, textvariable=self.interval).grid(row=16, column=1)

        tk.Button(self, text="Launch", command=self.launch).grid(row=17, column=0)

        tk.Button(self, text="Quit", command=self.quit).grid(row=17, column=1)

        tk.Button(self, text="Help", command=self.help).grid(row=17, column=2)


    def update_api_url(self, *args):
        if self.api_scheme.get() == "https":
            self.api_port.set(443)
        else:
            self.api_port.set(80)

    def launch(self):
        args = argparse.Namespace(
            api_key=self.api_key.get(),
            api_scheme=self.api_scheme.get(),
            api_url=self.api_url.get(),
            api_port=self.api_port.get(),
            input=self.input.get(),
            output=self.output.get(),
            folder=self.folder.get(),
            video=self.video.get(),
            stdout=self.stdout.get(),
            stderr=self.stderr.get(),
            verbose=self.verbose.get(),
            mode=self.mode.get(),
            config=self.config.get(),
            overwrite_config=self.overwrite_config.get(),
            no_verify=self.no_verify.get(),
            no_skip=self.no_skip.get(),
            interval=self.interval.get(),
            version=False,
            gui=False,
        )

        cli(args)

    def help(self):
        tk.messagebox.showinfo(
            "Help",
            """API Key : API key for the whisper API
API Scheme : API scheme for the whisper API
API URL : API url for the whisper API
API Port : API port for the whisper API
Input : Input file to send to the API
Output : Output file to save the result
Folder : Folder mode
Video : Video mode
Stdout : Print the result to stdout
Stderr : Print the result to stderr
Verbose : Verbose mode
Mode : Mode for the API, can be 'full', 'text', 'segments' and/or 'words' (comma separated)
Config : Config file for the whisper API, by default it is .whisperrc in the current directory or in the home directory
Overwrite Config : Overwrite config file with the current arguments (if the --config argument isn't provided, this will overwrite the default config file which is .whisperrc in the current directory or in the home directory
No Verify : Do not verify the SSL certificate
No Skip : Do not skip already downloaded files
Interval : Interval between two status checks
Version : Print the version of the client
GUI : Launch the GUI
"""
        )














def cli(parser: argparse.ArgumentParser | argparse.Namespace = parser) -> None:
    if isinstance(parser, argparse.Namespace):
        args = parser
    elif isinstance(parser, argparse.ArgumentParser):
        args = parser.parse_args()
    else:
        raise TypeError(f"ERROR : invalid type for parser : {type(parser)}")

    if args.version:
        from . import __version__
        print(f"whisper-client {__version__}")
        sys.exit(0)

    if args.gui:
        sys.exit(WhisperGUI())

    hash_audio = None

    config = None

    if args.config is not None:
        config = Path(args.config)
        assert config.exists(), f"ERROR : {config} does not exist"

    else:
        config = Path.cwd() / ".whisperrc"
        if not config.exists():
            config = Path.home() / ".whisperrc"
            if not config.exists():
                config = None

    if config is not None:
        with config.open(mode="r", encoding="utf-8") as f:
            config_data = json.load(f)

        for k, v in config_data.items():
            if v is not None and (
                    not hasattr(args, k)  # the attribute does not exist
                    or not getattr(args, k)  # the attribute is None or False or 0 or ""
                    or getattr(args, k) == parser.get_default(k)  # the attribute is the default value
            ):
                setattr(args, k, v)

    if args.verbose:
        print(args)

    if args.api_key is None:
        print("ERROR : no API key provided")
        sys.exit(1)

    if any([args.api_scheme is None, args.api_url is None]):
        print("ERROR : no API url provided")
        sys.exit(1)

    try:
        args.api_scheme = Scheme(args.api_scheme)
    except ValueError:
        print("ERROR : invalid API scheme provided")
        sys.exit(1)

    if args.mode is not None:
        try:
            if "," in args.mode:
                args.mode = [Mode(m) for m in args.mode.split(",")]
            else:
                args.mode = Mode(args.mode)
        except ValueError:
            print("ERROR : invalid API mode provided")
            sys.exit(1)

    if args.input is None:
        print("ERROR : no input provided")
        sys.exit(1)

    args.input = args.input.strip()

    if all((not args.output, not args.stdout, not args.stderr)) and not args.folder:
        print("ERROR : no output provided")
        sys.exit(1)

    dict_kwargs = {
        "api_key": args.api_key,
        "api_scheme": args.api_scheme,
        "api_url": args.api_url,
        "api_port": args.api_port,
        "verbose": args.verbose,
        "stdout": args.stdout,
        "stderr": args.stderr,
        "no_verify": args.no_verify,
        "no_skip": args.no_skip,
        "mode": args.mode,
    }

    if args.overwrite_config:
        config_data.update(dict_kwargs)
        with config.open(mode="w", encoding="utf-8") as f:
            json.dump(config_data, f)

        del config_data

    audio_folder, video_folder, text_folder = None, None, None

    if args.folder:
        if args.video:
            video_folder = Path(args.input)
        else:
            audio_folder = Path(args.input)

        text_folder = Path(args.output)

    wc = WhisperClient(
        api_key=args.api_key,
        api_scheme=args.api_scheme,
        api_host=args.api_url,
        api_port=args.api_port,
        audio_folder=audio_folder,
        video_folder=video_folder,
        text_folder=text_folder,
    )

    res = manage_input(
        wc,
        args.input,
        args.folder,
        args.video,
        args.mode,
        args.no_skip,
        args.no_verify,
        args.interval,
    )

    # hash_audio = wc.get_hash_audio()  ## Getting it from the global variable instead (not the prettiest thing though)

    if args.output is not None:
        manage_output(res, args.output, args.mode, args.folder, hash_audio)

    if args.stdout:
        print(res)

    if args.stderr:
        print(res, file=sys.stderr)


def manage_input(
        wc: WhisperClient,
        input: str,
        folder: bool,
        video: bool,
        modes: Mode | list[Mode] | str | list[str],
        no_skip: bool,
        no_verify: bool,
        interval: int
) -> Optional[list]:
    if folder:
        if video:
            wc.manage_video_folder(
                folder=folder,
                mode=modes,
                no_skip=no_skip,
                no_verify=no_verify,
                interval=interval
            )
        else:
            wc.manage_audio_folder(
                folder=folder,
                mode=modes,
                no_skip=no_skip,
                no_verify=no_verify,
                interval=interval
            )
    else:
        audiofile = Path(input)
        assert audiofile.exists(), f"ERROR : {audiofile} does not exist"
        hash_audio = wc.get_hash_audio(audiofile)

        if not no_skip and wc.is_hash_done(hash_audio):
            print(f"Result for {audiofile} already exists, skipping")
        else:
            hash_audio = wc.send_audio(audiofile)["hash"]
            wc.wait_for_result()

        if isinstance(modes, list):
            return [
                wc.get_result_with_mode(mode=mode, hash_audio=hash_audio)
                for mode in modes
            ]
        else:
            return wc.get_result_with_mode(mode=modes, hash_audio=hash_audio)


def manage_output(
        res: list | dict | str,
        output: str | Path,
        modes: Mode | list[Mode] | str | list[str],
        folder: bool,
        hash_audio: str = None
) -> None:
    if folder:
        return

    if isinstance(output, str):
        output = Path(output)

    if isinstance(res, list):
        assert len(res) == len(modes), f"ERROR : {len(res)} results for {len(modes)} modes"
        assert output.is_dir(), f"ERROR : {output} is not a directory (folder mode)"
        for r, m in zip(res, modes):
            manage_output(r, output, m, folder)

    output = output if not output.is_dir() else output / f"{hash_audio}_{modes}.json"

    if isinstance(res, dict):
        with output.open(mode="w", encoding="utf-8") as f:
            json.dump(res, f)

    elif isinstance(res, str):
        with output.open(mode="w", encoding="utf-8") as f:
            f.write(res)

    else:
        raise TypeError(f"ERROR : invalid type for res : {type(res)}")


if __name__ == "__main__":
    cli(parser)
