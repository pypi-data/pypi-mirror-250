from xdcc_dl.pack_search import SearchEngines
from xdcc_dl.xdcc import XDCCClient
from pyfzf.pyfzf import FzfPrompt
from tempfile import TemporaryDirectory
from multiprocessing import Process
from colorama import Fore, Style
import colorama
import shutil
import time
import os


class SilencedXDCCClient(XDCCClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def progress_printer(self):
        pass


fzf = FzfPrompt()


def download_video(search_results, tmp_dir):
    filtered_results = [result for result in search_results if "1080p" in result.filename]

    filenames = [f"{str(i + 1)} {result.filename.rsplit('.', 1)[0]}" for i, result in enumerate(filtered_results)]

    selected_index = int(fzf.prompt(filenames, "--reverse --cycle")[0].split(" ", 1)[0]) - 1
    selected_result = filtered_results[selected_index]

    selected_result.set_directory(tmp_dir)

    def download_process():
        client = SilencedXDCCClient(selected_result, channel_join_delay=3)
        client.download()

    download = Process(target=download_process)

    download.start()

    return selected_result, download


def main():
    colorama.init(autoreset=True)

    # check dependencies
    print(Fore.BLUE + Style.BRIGHT + "Checking dependencies...")
    if shutil.which("mpv") is None:
        print(Fore.RED + Style.BRIGHT + "mpv is not in PATH")
        exit(1)
    if shutil.which("fzf") is None:
        print(Fore.RED + Style.BRIGHT + "fzf is not in PATH")
        exit(1)

    with TemporaryDirectory(None, "xdcc-cli-") as tmp_dir:

        def play_video(selected_result):
            while selected_result.filename not in os.listdir(tmp_dir):
                time.sleep(0.25)

            executable_path = shutil.which("mpv")
            os.system(f"{executable_path} --no-terminal '{os.path.join(tmp_dir, selected_result.filename)}' &")

        search_term = input(Fore.CYAN + Style.BRIGHT + "Enter search term: " + Style.RESET_ALL)
        search_results = SearchEngines.NIBL.value.search(search_term)
        selected_result, download = download_video(search_results, tmp_dir)
        choice = ["Placeholder"]

        while True:
            if choice[0] == "Search again":
                search_term = input(Fore.CYAN + Style.BRIGHT + "Enter search term: " + Style.RESET_ALL)
                search_results = SearchEngines.NIBL.value.search(search_term)

            if choice[0] == "Choose again" or choice[0] == "Search again":
                selected_result, download = download_video(search_results, tmp_dir)

            play = Process(target=play_video, args=(selected_result,))
            play.start()
            print(Fore.BLUE + Style.BRIGHT + "Download starting...")
            play.join()

            choice = fzf.prompt(["Play again", "Choose again", "Search again", "Exit"], "--reverse --cycle")

            if choice[0] != "Play again":
                download.terminate()
                download.join()

            if choice[0] == "Exit":
                break


if __name__ == "__main__":
    main()
