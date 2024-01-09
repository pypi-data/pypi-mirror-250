#!/usr/bin/env python3
import argparse
import atexit
import dataclasses
import json
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any, List, Dict, Tuple

import tarfile
import json5
import csv
import requests
import urllib3.util
from strenum import StrEnum

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from EVMVerifier.certoraContextValidator import KEY_ENV_VAR
from Shared.certoraUtils import safe_copy_folder, change_working_directory, CERTORA_INTERNAL_ROOT, \
    get_package_resource, CERTORA_BINS
from certoraRun import run_certora, CertoraRunResult

DEFAULT_NUM_MUTANTS = 5


def exit_unless(cond: bool, msg: str) -> None:
    if not cond:
        print(msg)
        sys.exit(1)


def get_conf_from_certora_metadata(certora_sources: Path) -> Path:
    metadata_file = certora_sources / ".certora_metadata.json"
    if metadata_file.exists():
        with metadata_file.open() as orig_run_conf:
            metadata = json.load(orig_run_conf)
            if Constants.CONF in metadata:
                return metadata[Constants.CONF]
            else:
                print(f"{metadata_file} does not have the prover conf entry. Exiting.")
                sys.exit(1)
    else:
        print(f"Could not find .certora_metadata.json in {certora_sources}. Try certoraMutate with --prover_conf.")
        sys.exit(1)


def print_notification_msg() -> None:
    print("You will receive an email notification when this mutation test is completed. It may take several hours.")


def print_final_report_url_msg(url: str, mutation_id: str, anonymous_key: str) -> None:
    final_url = f"{url}?id={mutation_id}&{Constants.ANONYMOUS_KEY}={anonymous_key}"
    print(f"Mutation testing report is available at {final_url}")


def get_diff(original: Path, mutant: Path) -> str:
    test_result = subprocess.run(["diff", "--help"], capture_output=True, text=True)
    if test_result.returncode:
        print("Unable to get diff for manual mutations. Install 'diff' and try again to see more detailed information")
        return ""
    result = subprocess.run(["diff", str(original), str(mutant)], capture_output=True, text=True)
    if result.stdout is None:
        print("diff stdout was none for some reason")
    return result.stdout


def get_gambit_exec() -> str:
    exec = get_package_resource(CERTORA_BINS / "gambit")
    # try executing it
    try:
        rc = subprocess.run([exec, "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if rc.returncode == 0:
            return str(exec)
        else:
            print(f"Failed to execute {exec}")
            stderr_lines = rc.stderr.splitlines()
            for line in stderr_lines:
                print(line)
            # try just "gambit" - note this may hide some issues with the underlying process
            return "gambit"
    except Exception:
        # could not run the specialized name, just run gambit
        return "gambit"


def get_dir_from_certora_internal(_dir: str) -> Path:
    return CERTORA_INTERNAL_ROOT / _dir


def load_mutation_conf(mutation_conf: str) -> Any:
    if mutation_conf is not None:
        with Path(mutation_conf).open() as g_conf:
            return json5.load(g_conf)
    else:
        print(f"{mutation_conf} is None.")
        sys.exit(1)


def get_mutant_link(mutant: Dict[Any, Any]) -> Optional[str]:
    rule_report_link = mutant.get(Constants.RULE_REPORT_LINK)
    if rule_report_link is None:
        return mutant.get(Constants.LINK)
    return rule_report_link


def get_gambit_out_dir(conf: Any) -> Path:
    if Constants.GAMBIT in conf:
        conf = conf[Constants.GAMBIT]
    if isinstance(conf, list):
        if all(Constants.GAMBIT_OUTDIR not in obj for obj in conf):
            return Path(Constants.GAMBIT_OUT)
            # maybe return args.gambit_out when we have that.
        else:
            all_somes = [obj[Constants.GAMBIT_OUTDIR] for obj in conf if Constants.GAMBIT_OUTDIR in obj]
            if len(all_somes) != len(conf):
                print("Some of the conf objects have an outdir while others do not."
                      "Please fix your config.")
                sys.exit(1)
            if len(set(all_somes)) != 1:
                print("The outdir for all gambit mutants should be the same. Please fix your config.")
                sys.exit(1)
            else:
                return Path(all_somes[0])
    else:
        return Path(conf.get(Constants.GAMBIT_OUTDIR, Constants.GAMBIT_OUT))
    # return CERTORA_INTERNAL / args.gambit_out - waiting for a gambit bug to be introduced :)
    # (Gambit in json mode ignores -o. Luckily, it did not ignore skip_validate.
    # Chandra says it's a feature, but I (SG) asked to "introduce this bug" allowing to -o in json mode.)
    # Note: (CN) this is actually done now by Ben. Should be in the upcoming release.
    # THIS SHOULD BE: once Ben's PR is merged.
    # path = Path(Constants.GAMBIT_OUT) if Constants.GAMBIT_OUTDIR not in conf else Path(conf[Constants.GAMBIT_OUTDIR])
    # return CERTORA_INTERNAL_ROOT / path


def valid_link(link: str) -> bool:
    """
    Returns true if the provided link string is either a valid URL or a valid directory path
    """
    return validate_url(urllib3.util.parse_url(link)) or validate_dir(link)


def validate_dir(url: str) -> bool:
    try:
        return Path(url).is_dir()
    except Exception:
        return False


def valid_prover_run_link(url: str) -> bool:
    parsed_url = urllib3.util.parse_url(url)
    if not validate_url(parsed_url):
        return False
    domain = parsed_url.hostname
    if (
        domain != Constants.STAGING_DOTCOM and
        domain != Constants.PROVER_DOTCOM and
        domain != Constants.DEV_DOTCOM
    ):
        print("Invalid domain of the original job URL was provided")
        return False
    url_path = parsed_url.path
    pattern = re.compile(r"^\/output\/\d+\/[0-9a-fA-F]*(\/)?$")
    if url_path and re.match(pattern, url_path) is None:
        print("Invalid URL path of the original job URL was provided")
        return False
    return True


def valid_message(msg: str) -> None:
    if msg:
        pattern = re.compile(r"^[0-9a-zA-Z_=, ':\.\-\/]+$")
        if not re.match(pattern, msg):
            print("The message includes a forbidden character")
            sys.exit(1)


def validate_url(parsed_url: urllib3.util.Url) -> bool:
    """
    Thanks stackoverflow. This returns true if the given URL string is a valid URL, and false otherwise.
    """
    try:
        return all([parsed_url.scheme, parsed_url.netloc])
    except Exception:
        return False


def store_in_a_file(results: List[Any], ui_out: Path) -> None:
    try:
        with ui_out.open('w+') as ui_out_json:
            json.dump(results, ui_out_json)
    except Exception:
        print(f"Failed to output to {ui_out}")


def read_file(ui_out: Path) -> Any:
    if ui_out.exists():
        try:
            with ui_out.open('r') as ui_out_json:
                return json.load(ui_out_json)
        except Exception:
            print(f"Failed to read {ui_out}")
    else:
        print(f"Couldn't locate the output file ({ui_out})")


class WebUtils:
    def __init__(self, args: argparse.Namespace):
        self.server = self.config_server(args)
        self.max_timeout_attempts_count = args.max_timeout_attempts_count
        self.request_timeout = args.request_timeout
        if self.server == Constants.STAGING:
            domain = Constants.STAGING_DOTCOM
            mutation_test_domain = Constants.MUTATION_TEST_REPORT_STAGING
        elif self.server == Constants.PRODUCTION:
            domain = Constants.PROVER_DOTCOM
            mutation_test_domain = Constants.MUTATION_TEST_REPORT_PRODUCTION
        elif self.server == Constants.DEV:
            domain = Constants.DEV_DOTCOM
            mutation_test_domain = Constants.MUTATION_TEST_REPORT_DEV
        else:
            print(f"Invalid server name {self.server}")
            sys.exit(1)
        self.mutation_test_id_url = f"https://{domain}/mutationTesting/initiate/"
        self.mutation_test_submit_final_result_url = f"https://{domain}/mutationTesting/getUploadInfo/"
        self.mutation_test_final_result_url = f"https://{mutation_test_domain}"
        if args.debug:
            print(f"Using server {self.server} with mutation_test_id_url {self.mutation_test_id_url}")

    @staticmethod
    def config_server(args: argparse.Namespace) -> str:
        """
        If given a server, it is taken.
        Otherwise, computes from either the conf file or the orig run link.
        """
        # default production
        default = Constants.PRODUCTION
        if args.server:
            return args.server
        elif args.prover_conf is not None:
            # read the conf and try to get server configuration
            with open(args.prover_conf, 'r') as conf_file:
                conf_obj = json5.load(conf_file)
            if Constants.SERVER in conf_obj:
                return conf_obj[Constants.SERVER]
            else:
                return default
        elif args.orig_run is not None:
            if Constants.STAGING_DOTCOM in args.orig_run:
                return Constants.STAGING
            elif Constants.PROVER_DOTCOM in args.orig_run:
                return default
            elif Constants.DEV_DOTCOM in args.orig_run:
                return Constants.DEV
            else:
                print(f"{args.orig_run} link is neither for staging not production.")
                sys.exit(1)
        else:
            return default

    def put_response_with_timeout(self, url: str, data: Any, headers: Dict[str, str]) -> Optional[requests.Response]:
        """
        Executes a put request and returns the response, uses a timeout mechanism

        Args
        ----
            url (str): the URL to send a PUT request to
            data (Any): the data to send
            headers (dict[str, str]): an optional set of headers

        Returns
        -------
            Optional[requests.Response]: if any of the attempt succeeded, returns the response
        """
        for i in range(self.max_timeout_attempts_count):
            try:
                return requests.put(url, data=data, timeout=self.request_timeout,
                                    headers=headers)
            except Exception:
                print(f"attempt {i} failed to put url {url}.")
        return None

    def put_json_request_with_timeout(self, url: str, body: Dict[str, Any],
                                      headers: Dict[str, str]) -> Optional[requests.Response]:
        """
        Executes a put request and returns the response, uses a timeout mechanism

        Args
        ----
            url (str): the URL to send a PUT request to
            body (dict[str, Any]): request body
            headers (dict[str, str]): an optional set of headers

        Returns
        -------
            Optional[requests.Response]: if any of the attempt succeeded, returns the response
        """
        for i in range(self.max_timeout_attempts_count):
            try:
                return requests.put(url, json=body, timeout=self.request_timeout,
                                    headers=headers)
            except Exception:
                print(f"attempt {i} failed to put url {url}.")
        return None

    def get_response_with_timeout(self, url: str,
                                  cookies: Dict[str, str] = {}, stream: bool = False) -> Optional[requests.Response]:
        """
        Executes a get request and returns the response, uses a timeout mechanism

        Args
        ----
            url (str): the URL to send a GET request to
            cookies (dict[str, str]): an optional set of cookies/request data
            stream (bool): use a lazy way to download large files

        Returns
        -------
            Optional[requests.Response]: if any of the attempt succeeded, returns the response
        """
        for i in range(self.max_timeout_attempts_count):
            try:
                resp = requests.get(url, timeout=self.request_timeout, cookies=cookies, stream=stream)
                return resp
            except Exception:
                print(f"attempt {i} failed to get url {url}.")
        return None


# SUBMIT PHASE FUNCTIONALITY

@dataclass
class GambitMutant:
    filename: str
    original_filename: str
    directory: str
    id: str
    diff: str
    description: str


@dataclass
class MutantRun:
    gambit_mutant: GambitMutant
    link: Optional[str]
    success: bool
    run_directory: Optional[str]
    rule_report_link: Optional[str]


def check_key_exists() -> None:
    if KEY_ENV_VAR not in os.environ:
        print("Cannot run mutation testing without a Certora Key.")
        sys.exit(1)


class ReportFetcher:
    def get_output_json(self, link: str) -> Optional[Dict[str, Any]]:
        pass

    def get_treeview_json(self, link: str) -> Optional[Dict[str, Any]]:
        pass


class TreeViewStatus(StrEnum):
    RUNNING = "RUNNING"
    VERIFIED = "VERIFIED"
    SKIPPED = "SKIPPED"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"
    SANITY_FAILED = "SANITY_FAILED"
    VIOLATED = "VIOLATED"


class MutationTestRuleStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    TIMEOUT = "TIMEOUT"
    SANITY_FAIL = "SANITY_FAIL"
    UNKNOWN = "UNKNOWN"


class FlowType(StrEnum):
    SYNC = "sync"
    ASYNC = "async"


class FinalJobStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    ERROR = "ERROR"
    LAMBDA_ERROR = "LAMBDA_ERROR"

    @classmethod
    def get_statuses(cls) -> List[str]:
        return [s.value for s in cls]


def convert_to_mutation_testing_status(treeview_status: str) -> str:
    if (treeview_status == TreeViewStatus.VERIFIED) or (treeview_status == TreeViewStatus.SKIPPED):
        return MutationTestRuleStatus.SUCCESS
    elif treeview_status == TreeViewStatus.VIOLATED:
        return MutationTestRuleStatus.FAIL
    elif treeview_status == TreeViewStatus.TIMEOUT:
        return MutationTestRuleStatus.TIMEOUT
    elif treeview_status == TreeViewStatus.SANITY_FAILED:
        return MutationTestRuleStatus.SANITY_FAIL
    else:
        return MutationTestRuleStatus.UNKNOWN


@dataclass
class RuleResult:
    name: str
    status: str

    def __init__(self, _name: str, _status: str):
        self.name = _name
        self.status = _status


@dataclass
class UIData:
    description: str
    diff: str
    link: str
    name: str
    id: str
    rules: List[Dict[str, Any]]
    # no real need to fill this
    SANITY_FAIL: List[str]
    UNKNOWN: List[str]
    TIMEOUT: List[str]

    def __init__(self, _description: str, _diff: str, _id: str, _name: str, _link: str, _rules: List[RuleResult]):
        # build for a mutant
        self.description = _description
        self.diff = _diff
        self.id = _id
        self.name = _name
        self.link = _link

        self.populate_rules(_rules)

    def populate_rules(self, _rules: List[RuleResult]) -> None:
        x = [dataclasses.asdict(e) for e in  # effing linter
             list(
                 filter(
                     lambda r: r.status == MutationTestRuleStatus.SUCCESS or r.status == MutationTestRuleStatus.FAIL,
                     _rules))]
        self.rules = x
        self.SANITY_FAIL = [r.name for r in _rules if r.status == MutationTestRuleStatus.SANITY_FAIL]
        self.UNKNOWN = [r.name for r in _rules if r.status == MutationTestRuleStatus.UNKNOWN]
        self.TIMEOUT = [r.name for r in _rules if r.status == MutationTestRuleStatus.TIMEOUT]


def parse_args() -> argparse.Namespace:
    """
    Returns a Namespace object with the configuration of the mutation testing tool
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--mutation_conf", type=Path, help="The configuration file for this script",
                        required=True)

    # submission related
    parser.add_argument("--prover_conf", type=Path, help="The Prover configuration file for verifying mutants.")
    parser.add_argument("--orig_run", help="Link to a previous run of the prover on the original program.")
    parser.add_argument("--msg", help="Add a message to identify the certoraMutate run.")
    parser.add_argument("--conf_output_file", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--prover_version",
                        help="Specify the certoraRun version for verification. "
                             "If not specified, the installed certoraRun version is used by default.")
    parser.add_argument("--server", help=argparse.SUPPRESS)
    parser.add_argument("--debug", action='store_true', help="Turn on verbose debug prints.")
    parser.add_argument("--orig_run_dir", type=Path, default=Constants.CERTORA_MUTATE_SOURCES,
                        help="The folder where the files will be downloaded from the original run link")
    parser.add_argument("--gambit_only", action="store_true", help="Stop processing after generating mutations.")

    parser.add_argument("--dump_failed_collects", type=Path, default="collection_failures.txt",
                        help="Path to the log file capturing mutant collection failures.")
    parser.add_argument("--dump_link", type=Path, help="Write the UI report link to a file.")

    # Sets a file that will store the object sent to mutation testing UI (useful for testing)
    parser.add_argument("--ui_out", type=Path, default="results.json", help=argparse.SUPPRESS)
    # Write the ui_out content in csv form
    parser.add_argument("--dump_csv", type=Path, help=argparse.SUPPRESS)

    # Synchronous mode
    # Run the tool synchronously in shell
    parser.add_argument("--sync", action="store_true", help=argparse.SUPPRESS)
    '''
    The file containing the links holding certoraRun report outputs.
    In async mode, run this tool with only this option.
    '''
    parser.add_argument("--collect_file", type=Path, default="collect.json", help=argparse.SUPPRESS)
    '''
    The max number of minutes to poll after submission was completed,
     and before giving up on synchronously getting mutation testing results
    '''
    parser.add_argument("--poll_timeout", default=30, type=int, help=argparse.SUPPRESS)

    # Web related config
    # The maximum number of retries a web request is attempted
    parser.add_argument("--max_timeout_attempts_count", default=3, type=int, help=argparse.SUPPRESS)
    # The timeout in seconds for a web request
    parser.add_argument("--request_timeout", default=10, type=int, help=argparse.SUPPRESS)

    args = parser.parse_args()

    return args


class CertoraMutate:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.orig_run = args.orig_run
        self.prover_conf = args.prover_conf
        self.conf_output_file = args.conf_output_file
        self.mutation_conf = args.mutation_conf
        self.prover_version = args.prover_version
        self.msg = args.msg
        self.server = args.server
        self.debug = args.debug
        self.gambit_only = args.gambit_only
        self.orig_run_dir = args.orig_run_dir
        self.ui_out = args.ui_out
        self.dump_csv = args.dump_csv
        self.dump_failed_collects = args.dump_failed_collects
        self.dump_link = args.dump_link
        self.collect_file = args.collect_file
        self.sync = args.sync
        self.max_timeout_attempts_count = args.max_timeout_attempts_count
        self.request_timeout = args.request_timeout
        self.poll_timeout = args.poll_timeout
        self.output_dir = get_gambit_out_dir(load_mutation_conf(self.mutation_conf))

    def validate_args(self) -> None:
        if self.prover_conf is not None and self.orig_run is not None:
            print("Recommended to run with `--orig_run`. Cannot pass both `--prover_conf` and `--orig_run`.")
            sys.exit(1)
        if self.orig_run is not None:
            exit_unless(valid_prover_run_link(self.orig_run),
                        f"Link for previous run {self.orig_run} is not valid. Please provide a valid link.")
            if self.orig_run_dir != Constants.CERTORA_MUTATE_SOURCES:
                print("Warning: using --orig_run_dir without --orig_run has no effect")
        if self.prover_conf is not None:
            exit_unless(self.prover_conf.exists(),
                        f"Prover configuration file {self.prover_conf} does not exist.")
        if self.msg is not None:
            exit_unless(len(self.msg) <= 255, "--msg argument should not exceed 255 characters.")
            valid_message(self.msg)
        if self.mutation_conf is not None:
            exit_unless(self.mutation_conf.exists(),
                        f"Gambit configuration file {self.mutation_conf} does not exist.")
            exit_unless(self.prover_conf is not None or self.orig_run is not None,
                        "Running with `--mutation_conf` must also provide `--prover_conf` or `--orig_run`.")
        # This is a good start, but we can do more to fail gracefully and correct invalid invocations of the tool

        self.validate_empty_directories()

    def fetch_and_extract_inputs_dir(self, url: Optional[str]) -> Path:
        if url is None:
            print("URL for original run is null. Exiting.")
            sys.exit(1)
        web_utils = WebUtils(self.args)
        zip_output_url = url.replace(Constants.OUTPUT, Constants.ZIPOUTPUT)
        response = web_utils.get_response_with_timeout(zip_output_url, stream=True, cookies=default_cookies)
        if response is None:
            print("Could not fetch zip output from previous run. Try running certoraMutate with --prover_conf.")
            sys.exit(1)
        if response.status_code == 200:
            with open(Constants.ZIP_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            print(f"Failed to fetch inputs dir from {url}. Got status code: {response.status_code}."
                  f"Try running certoraMutate with --prover_conf.")
            sys.exit(1)
        try:
            extract = tarfile.open(Constants.ZIP_PATH, "r")
            extract.extractall(self.orig_run_dir)
            return self.orig_run_dir / Constants.TARNAME / Constants.INPUTS
        except Exception:
            print(f"Failed to extract .certora_source from {url}.")
            sys.exit(1)

    def submit(self) -> None:
        print("Generating mutants and submitting...")

        # ensure .certora_internal exists
        os.makedirs(CERTORA_INTERNAL_ROOT, exist_ok=True)

        # start by cleaning up any previous run remnants
        self.delete_artifacts()
        atexit.register(self.cleanup)

        _SEP = "*" * 20
        msg_separator_for_certora_run_start = f"{_SEP} PROVER START {_SEP}"
        msg_separator_for_certora_run_end = f"{_SEP}  PROVER END  {_SEP}"
        msg_separator_for_using_prev_run = f"{_SEP}  USING PREVIOUS RUN LINK  {_SEP}"

        local = None
        sources_dir = None
        prover_conf: Path = Path()

        # call gambit
        generated_mutants = []
        manual_mutants = []
        if self.mutation_conf is not None:
            mutation_conf = load_mutation_conf(self.mutation_conf)
            if mutation_conf.get(Constants.GAMBIT):
                generated_mutants = self.run_gambit()
            elif self.gambit_only:
                print("gambit section must exist when running with 'gambit_only'")
                sys.exit(1)
            if self.gambit_only:
                sys.exit(0)

            if Constants.MANUAL_MUTANTS in mutation_conf:
                manual_mutants = self.parse_manual_mutations()
                if self.debug:
                    print(f"successfully parsed manual mutants from {self.mutation_conf}")
            if Constants.MSG in mutation_conf and not self.msg:
                self.msg = mutation_conf.get(Constants.MSG)

        if self.prover_conf is not None:
            prover_conf = self.prover_conf
            print("WARNING: Running without a link to a previously successful prover run on the original contract. "
                  "So we will first submit the original Prover configuration. No source mutations...")
            print(msg_separator_for_certora_run_start)
            # run original run. if it fails to compile, nothing to continue with
            success, certora_run_result = self.run_certora_prover(self.prover_conf, msg=Constants.ORIGINAL.value)

            if certora_run_result:
                local = certora_run_result.is_local_link
                if local:
                    rule_report_link = certora_run_result.link
                else:
                    rule_report_link = certora_run_result.rule_report_link
                sources_dir = certora_run_result.src_dir

            if local:
                # we do not cleanup in local mode
                atexit.unregister(self.cleanup)

            if not success or not certora_run_result or not rule_report_link or not sources_dir:
                print("Original run was not successful. Cannot run mutation testing.")
                sys.exit(1)

            if local:
                try:
                    if not Path(rule_report_link).is_dir():
                        print("Invalid certoraRun result")
                        if self.debug:
                            print("Unexpected path for a local job", rule_report_link)
                        sys.exit(1)
                except TypeError:
                    print("Invalid certoraRun result")
                    if self.debug:
                        print("rule_report_link is None")
                    sys.exit(1)
            else:
                if not validate_url(urllib3.util.parse_url(rule_report_link)):
                    print("Invalid certoraRun result")
                    if self.debug:
                        print(rule_report_link)
                    sys.exit(1)
            print(msg_separator_for_certora_run_end)
        elif self.orig_run is not None:
            print(msg_separator_for_using_prev_run)
            rule_report_link = self.orig_run
            local = False
            input_dir = self.fetch_and_extract_inputs_dir(rule_report_link)
            sources_dir = input_dir / ".certora_sources"
            prover_conf_content = get_conf_from_certora_metadata(input_dir)
            prover_conf = Path(Constants.ORIG_RUN_PROVER_CONF)
            with prover_conf.open('w') as p_conf:
                json.dump(prover_conf_content, p_conf)
            shutil.copy(prover_conf, sources_dir)

        # match a generated mutant to a directory where we will apply the diff
        base_dir = self.applied_mutants_dir
        generated_mutants_with_target_dir = []
        for mutant in generated_mutants:
            generated_mutants_with_target_dir.append((mutant, base_dir / f"mutant{mutant.id}"))
        manual_mutants_with_target_dir = []
        for mutant in manual_mutants:
            manual_mutants_with_target_dir.append((mutant, base_dir / f"manual{mutant.id}"))
        all_mutants_with_target_dir = generated_mutants_with_target_dir + manual_mutants_with_target_dir
        if self.debug:
            print("Associated each mutant to a target directory where the mutant will be applied to the source code")

        web_utils = WebUtils(self.args)
        # get the mutation test id
        mutation_test_id, collect_presigned_url = (
            self.get_mutation_test_id_request(web_utils, len(all_mutants_with_target_dir)))
        if self.debug:
            print(f"Mutation test id: {mutation_test_id}")

        print("Submit mutations to Prover...")
        print(msg_separator_for_certora_run_start)
        # find out the number of processes. in local runs, we want just one! otherwise,
        # use all CPUs available (set to None)
        if local:
            num_processes_for_mp = 1
            # otherwise, weird things happen locally. this forces us to refresh and get a new executable
            max_task_per_worker = 1
        else:
            num_processes_for_mp = None
            max_task_per_worker = None
        with multiprocessing.Pool(processes=num_processes_for_mp, maxtasksperchild=max_task_per_worker) as pool:
            mutant_runs = pool.starmap(self.run_mutant,
                                       [(mutant, sources_dir, trg_dir, prover_conf, mutation_test_id)
                                        for mutant, trg_dir in all_mutants_with_target_dir])

        print(msg_separator_for_certora_run_end)

        if self.debug:
            print("Completed submitting all mutant runs")
            print(rule_report_link)
            print([dataclasses.asdict(m) for m in mutant_runs])

        # wrap it all up and make the input for the 2nd step: the collector
        with self.collect_file.open('w+') as collect_file:
            collect_data = {Constants.ORIGINAL: rule_report_link,
                            Constants.MUTANTS: [dataclasses.asdict(m) for m in mutant_runs]}
            json.dump(collect_data, collect_file)

        if not self.sync:
            # the new flow. upload the collect_data to the cloud
            self.upload_file_to_cloud_storage(web_utils, collect_presigned_url, collect_data)
            print_notification_msg()
        else:
            print(f"... completed submit phase! Now we poll on {self.collect_file}...")

    def run_mutant(self, mutant: GambitMutant, src_dir: Path, trg_dir: Path, orig_conf: Path,
                   mutation_test_id: str) -> MutantRun:
        # first copy src_dir
        safe_copy_folder(src_dir, trg_dir, shutil.ignore_patterns())  # no ignored patterns

        # now apply diff.
        # Remember: we are always running certoraMutate from the project root.
        file_path_to_mutate = trg_dir / Path(mutant.original_filename)
        # 2. apply the mutated file in the newly rooted path
        shutil.copy(mutant.filename, file_path_to_mutate)

        with change_working_directory(trg_dir):
            # we have conf file in sources, let's run from it, it will have proper filepaths
            success, certora_run_result = (
                self.run_certora_prover(orig_conf, mutation_test_id, msg=f"mutant ID: {mutant.id}"))
            if not success or not certora_run_result:
                print(f"Failed to run mutant {mutant}")
                return MutantRun(
                    gambit_mutant=mutant,
                    success=success,
                    link=None,
                    run_directory=None,
                    rule_report_link=None
                )

            link = certora_run_result.link
            sources_dir = certora_run_result.src_dir

            return MutantRun(
                gambit_mutant=mutant,
                success=success,
                link=link,
                run_directory=str(sources_dir),
                rule_report_link=certora_run_result.rule_report_link
            )

    def run_gambit(self) -> List[GambitMutant]:
        mutation_conf = load_mutation_conf(self.mutation_conf)

        # By default, we should just send the mutation_conf straight to gambit.
        conf_to_send_to_gambit: Path = self.mutation_conf

        # Only send the "gambit" field because manual mutations are a Certora specific feature
        # and gambit expects only the _value_ of the "gambit" field, nothing else.
        # Make sure that this new gambit conf is in the same directory as the old one.
        new_mutation_conf = self.mutation_conf.parent / Constants.TMP_GAMBIT
        if Constants.GAMBIT in mutation_conf:
            gambit_obj_list = mutation_conf[Constants.GAMBIT]
            if not isinstance(gambit_obj_list, list):
                gambit_obj_list = [gambit_obj_list]
            for gambit_obj in gambit_obj_list:
                if Constants.NUM_MUTANTS.value not in gambit_obj:
                    gambit_obj[Constants.NUM_MUTANTS.value] = DEFAULT_NUM_MUTANTS
            with new_mutation_conf.open('w') as g_conf:
                json.dump(gambit_obj_list, g_conf)
                conf_to_send_to_gambit = new_mutation_conf

        gambit_exec = get_gambit_exec()
        gambit_args = [gambit_exec, "mutate", "--json", str(conf_to_send_to_gambit),
                       "-o", str(self.output_dir), "--skip_validate"]
        print(f"Running gambit: {gambit_args}")
        run_result = \
            subprocess.run(gambit_args, shell=False, universal_newlines=True, stderr=subprocess.PIPE,
                           stdout=subprocess.PIPE)

        if run_result.returncode:
            print("Gambit run failed")
            print(run_result.stdout)
            print(run_result.stderr)
            sys.exit(1)

        if self.debug:
            print("Completed gambit run successfully.")

        # read gambit_results.json
        ret_mutants = []
        with open(self.output_dir / "gambit_results.json", "r") as gambit_output_json:
            gambit_output = json.load(gambit_output_json)
            for gambit_mutant_data in gambit_output:
                ret_mutants.append(
                    GambitMutant(
                        filename=str(self.output_dir / gambit_mutant_data[Constants.NAME]),
                        original_filename=gambit_mutant_data[Constants.ORIGINAL],
                        # should be relative to re-root in target dir
                        directory=str(self.output_dir / Constants.MUTANTS / gambit_mutant_data[Constants.ID]),
                        id=gambit_mutant_data[Constants.ID],
                        diff=gambit_mutant_data[Constants.DIFF],
                        description=gambit_mutant_data[Constants.DESCRIPTION]
                    )
                )

        if os.path.exists(new_mutation_conf):
            os.remove(new_mutation_conf)
        if self.debug:
            print("Got mutant information")
        return ret_mutants

    def auto_config(self) -> None:
        print(f"Automatically generating mutation .conf from prover_conf {self.prover_conf}")
        mutation_conf_elts = []
        with open(self.prover_conf, "r") as prover_conf:
            prover_json = json.load(prover_conf)
            for orig_file in prover_json[Constants.FILES]:
                mutation_conf_elt = {
                    Constants.FILENAME: str(Path(os.path.relpath(os.getcwd(), self.mutation_conf.parent)) / orig_file),
                    Constants.SOLC: prover_json[Constants.SOLC],
                }
                # NOTE: this part requires better parity between gambit and prover conf files
                # if Constants.PACKAGES in prover_json:
                #    mutation_conf_elt[Constants.SOLC_REMAPPINGS] = prover_json[Constants.PACKAGES]
                # if Constants.SOLC_ALLOW_PATH in prover_json:
                #    mutation_conf_elt[Constants.SOLC_ALLOW_PATHS] = [ prover_json[Constants.SOLC_ALLOW_PATH], ]
                mutation_conf_elts.append(mutation_conf_elt)

        with open(self.mutation_conf, "w") as mutation_conf:
            json.dump(mutation_conf_elts, mutation_conf)
            print(f"Success! Gambit config was automatically generated at '{str(self.mutation_conf)}' " +
                  f"from the Certora config at '{str(self.prover_conf)}'.")

    def parse_manual_mutations(self) -> List[GambitMutant]:
        mutation_conf = self.mutation_conf
        print(f"Parsing manual mutations from {mutation_conf} file.")
        ret_mutants = []
        manual_id = 0
        with open(mutation_conf, "r") as conf:
            gambit_cfg = json.load(conf)
            for orig in gambit_cfg[Constants.MANUAL_MUTANTS]:
                orig_file = os.path.normpath(mutation_conf.parent / orig)
                path_to_orig = os.path.abspath(orig_file)
                if not os.path.exists(path_to_orig):
                    print(f"Original file '{path_to_orig}' for manual mutations does not exist Skipping verification.")
                    continue
                manual_mutant_dir = mutation_conf.resolve().parent.joinpath(gambit_cfg[Constants.MANUAL_MUTANTS][orig])
                manual_mutants = [mm for mm in Path(manual_mutant_dir).iterdir()
                                  if mm.is_file() and Path(mm).suffix == ".sol"]
                for manual_mutant in manual_mutants:
                    if not manual_mutant.exists():
                        print(f"Mutant file '{str(manual_mutant)}' from manual mutations does not exist." +
                              "Skipping verification for this file.")
                        continue
                    manual_id += 1
                    ret_mutants.append(
                        GambitMutant(
                            filename=str(manual_mutant),
                            original_filename=str(orig_file),
                            directory=str(Path(manual_mutant).parent),
                            id=f"m{manual_id}",
                            diff=get_diff(orig_file, manual_mutant),
                            description=str(manual_mutant),  # NOTE: parse a description from the mutant source
                        )
                    )
        return ret_mutants

    def run_certora_prover(self, conf_file: Path,
                           mutation_test_id: str = "", msg: str = "") -> Tuple[bool, Optional[CertoraRunResult]]:
        with conf_file.open() as conf_file_handle:
            conf_file_obj = json5.load(conf_file_handle)
            if "run_source" in conf_file_obj:
                print(
                    f"Conf object already has a run source: {conf_file_obj['run_source']}")  # is that of significance?

            certora_args = [str(conf_file), "--run_source", "MUTATION", "--msg", msg]
            if mutation_test_id:
                certora_args.extend(["--mutation_test_id", mutation_test_id])

            if self.server is not None and "server" not in conf_file_obj:
                # note that if "server" option already exists in conf, the runs will run on the already specified
                # server in conf, but mutation testing results will be sent to whatever server the user provided to
                # certoraMutate
                certora_args.append("--server")
                certora_args.append(self.server)
            if self.prover_version is not None:
                # prover_version is definitely a prover property, so if it's given already, it's a mistake
                if "prover_version" in conf_file_obj:
                    print(f"Mutation testing asked to run on Prover version {self.prover_version} "
                          f"but Prover conf already specifies {conf_file_obj['prover_version']}")
                    return False, None
                certora_args.append("--prover_version")
                certora_args.append(self.prover_version)
        print(f"Running the Prover: {certora_args}")
        try:
            certora_run_result = run_certora(certora_args, True)
        except Exception as e:
            print(f"Failed to run with {e}")
            return False, None

        return True, certora_run_result

    def validate_empty_directories(self) -> None:
        """
        This function ensures that all the directories used in mutation testing are empty.
        If they are not empty, we risk deleting the files in the first forced cleanup, which can include data from
        previous runs.
        :return:
        """
        def validate_non_existent_dir(_dir: Path, description: str) -> None:
            if _dir.exists():
                raise FileExistsError(f"{description} already exists ({_dir})")

        self.orig_run_dir = get_dir_from_certora_internal(self.orig_run_dir)
        validate_non_existent_dir(self.orig_run_dir, "original run directory")

        self.applied_mutants_dir = get_dir_from_certora_internal(Constants.APPLIED_MUTANTS_DIR_NAME)
        shutil.rmtree(str(self.applied_mutants_dir), ignore_errors=True)

        output_dir_name = str(self.output_dir)
        if output_dir_name == Constants.GAMBIT_OUT:  # the default value
            shutil.rmtree(Constants.GAMBIT_OUT, ignore_errors=True)
        else:
            validate_non_existent_dir(self.output_dir, "gambit output directory")

    @staticmethod
    def delete_artifacts() -> None:
        """
        This function deletes artifacts generated by this script, either in this run or a previous run
        None of these are things the user cares to see
        All files here are NOT user inputs
        """
        for _path in [Constants.ORIG_RUN_PROVER_CONF, Constants.ZIP_PATH]:
            path = Path(_path)
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
            except FileNotFoundError:
                pass

    def cleanup(self) -> None:
        """
        First cleanup will be forced
        """
        if not self.debug:
            self.delete_artifacts()
            shutil.rmtree(str(self.orig_run_dir), ignore_errors=True)
            shutil.rmtree(str(self.applied_mutants_dir), ignore_errors=True)
            shutil.rmtree(str(self.output_dir), ignore_errors=True)

    # COLLECT PHASE FUNCTIONALITY

    def collect(self) -> bool:
        """
        Returns true if finished collecting.
        Returns false if not, but there's still a chance something will return.
        Will exit with exitcode 1 if something is broken in the collect file.
        """
        orig_collect_success = True
        if not self.collect_file.exists():
            print(f"Cannot collect results, as file to collect from {self.collect_file} does not exist.")
            sys.exit(1)

        with open(self.collect_file, 'r') as collect_handle:
            results_work = json.load(collect_handle)

        if Constants.ORIGINAL not in results_work:
            print(f"Could not find original url in {self.collect_file}.")
            sys.exit(1)

        if Constants.MUTANTS not in results_work:
            print(f"Could not find mutants in {self.collect_file}.")
            sys.exit(1)

        print(f"Collecting results from {self.collect_file}...")

        original_url = results_work[Constants.ORIGINAL]

        if original_url is None or (not valid_link(original_url)):
            print("There is no original URL - nothing to collect.")
            orig_collect_success = False

        web_utils = WebUtils(self.args)
        # default is a web fetcher
        fetcher: ReportFetcher = WebFetcher(web_utils, self.debug)
        ui_elements: List[UIData] = []

        # if we got a proper URL, we'll use a WebFetcher, otherwise we'll use a FileFetcher
        if validate_dir(original_url):
            fetcher = FileFetcher()

        original_results = self.get_results(original_url, fetcher)
        original_results_as_map = dict()

        if original_results is not None:
            original_results_as_map = \
                {res.name: res.status for res in original_results if res.status == MutationTestRuleStatus.SUCCESS}
            # add original
            ui_elements.append(UIData("", "", "Original", "Original", original_url, original_results))
        else:
            orig_collect_success = False
            if not self.sync:
                print("Failed to get results for original. This means the report may not get generated correctly.")

        # check the mutant URLs
        mutants_objs = results_work[Constants.MUTANTS]
        mutant_collect_success = True
        if any(
            [
                (get_mutant_link(mutant) is None or not valid_link(get_mutant_link(mutant)))  # type: ignore
                for mutant in mutants_objs
            ]
        ):
            print(f"There are some bad mutant URLs. Check {self.collect_file} to see if some are null or invalid.")
            mutant_collect_success = False

        # build mutants object with the rule results
        mutants_results = []  # type: List[Any]
        for mutant in mutants_objs:
            mutant_link = get_mutant_link(mutant)
            if mutant_link is not None:
                mutants_results.append((mutant, self.get_results(mutant_link, fetcher)))
        # structure of results.json to send to UI is Original -> UIData, and mutantFileName -> UIData

        with self.dump_failed_collects.open('w') as failed_collection:
            # add mutants
            for mutant, mutant_result_list in mutants_results:
                if not mutant_result_list:
                    mutant_collect_success = False
                    failed_collection.write(f"{mutant}\n\n")
                    continue
                # This is a bad thing I did just to help out with the community contests.
                # This is not the right way to use certoraMutate.
                if self.dump_csv is not None:
                    filtered_mutant_result: List[RuleResult] = list(mutant_result_list)
                else:
                    filtered_mutant_result = list(
                        filter(lambda r: r.name in original_results_as_map, mutant_result_list))
                mutant_link = get_mutant_link(mutant)
                if mutant_link is None:
                    mutant_link = ""
                ui_elements.append(UIData(mutant[Constants.GAMBIT_MUTANT][Constants.DESCRIPTION],
                                          mutant[Constants.GAMBIT_MUTANT][Constants.DIFF],
                                          mutant[Constants.GAMBIT_MUTANT][Constants.ID],
                                          mutant[Constants.GAMBIT_MUTANT][Constants.FILENAME],
                                          mutant_link,
                                          filtered_mutant_result))

        if not mutant_collect_success and not self.sync:
            print(f"Failed to get results for some mutants. See {self.dump_failed_collects} "
                  f"and try to manually run the prover on them to see the outcome.")
        if self.debug:
            print(json.dumps([dataclasses.asdict(e) for e in ui_elements]))
        results = [dataclasses.asdict(e) for e in ui_elements]

        if self.ui_out is not None:
            store_in_a_file(results, self.ui_out)

        # This is for the contests mainly.
        # We want to generate this:
        # rulename, original, mutant1, mutant2, ...
        # NAME,     PASS    , FAIL   , PASS, ...
        if self.dump_csv is not None:
            print("WARNING: The --dump_csv feature is only recommended when using certoraMutate as an automation for "
                  "grading competitions. It ignores all failures on the original program. The corresponding "
                  "mutation report or json dump will not match with the csv dump output either. Please do not use this "
                  "unless you are really just using certoraMutate to grade assignments.")
            try:
                self.json_to_csv(results)
            except Exception:
                print(f"Failed to output csv to {self.dump_csv}.")

        if orig_collect_success and mutant_collect_success:
            print("Done successfully collecting results!")
        return orig_collect_success and mutant_collect_success

    def get_mutation_test_id_request(self, web_utils: WebUtils, mutants_number: int) -> Tuple[str, str]:
        if self.debug:
            print(f"Getting mutation test ID for {mutants_number} mutants")
        url = web_utils.mutation_test_id_url
        body = {"mutants_number": mutants_number}  # type: Dict[str, Any]
        if self.orig_run:
            # we have validated this URL before
            parsed_url = urllib3.util.parse_url(self.orig_run)
            # ignore the query parameters and fragments
            body["original_job_url"] = f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
        if self.msg:
            body["msg"] = self.msg
        if self.debug:
            print("Sending a PUT request with the body:", body)
        resp = web_utils.put_json_request_with_timeout(url, body, headers=auth_headers)
        if resp is None:
            print("Failed to get the mutation test ID")
            sys.exit(1)
        if self.debug:
            print(f"Got mutation test ID response: {resp.status_code}")
        resp_obj = resp.json()
        if Constants.ID not in resp_obj or Constants.COLLECT_SIGNED_URL not in resp_obj:
            print("invalid server response, mutation test failed")
            if self.debug:
                print(resp_obj)

            sys.exit(1)

        return resp_obj[Constants.ID], resp_obj[Constants.COLLECT_SIGNED_URL]

    def get_mutation_test_final_report_url(self, web_utils: WebUtils) -> Tuple[str, str, str]:
        if self.debug:
            print("Getting mutation test final report URL")
        url = web_utils.mutation_test_submit_final_result_url
        resp = web_utils.get_response_with_timeout(url, cookies=default_cookies)
        if resp is None:
            print("Failed to get the mutation test report URL")
            sys.exit(1)
        if self.debug:
            print(f"Got response: {resp.status_code}")
        resp_obj = resp.json()
        if Constants.ID in resp_obj and Constants.PRE_SIGNED_URL in resp_obj and Constants.ANONYMOUS_KEY in resp_obj:
            return resp_obj[Constants.ID], resp_obj[Constants.ANONYMOUS_KEY], resp_obj[Constants.COLLECT_SIGNED_URL]
        else:
            print("Couldn't generate the report URL")
            if self.debug:
                print(resp_obj)
            sys.exit(1)

    def upload_file_to_cloud_storage(self, web_utils: WebUtils, presigned_url: str, data: Any) -> None:
        if self.debug:
            print("Uploading file")
        headers = {"Content-Type": "application/json"}
        put_resp = web_utils.put_response_with_timeout(presigned_url, json.dumps(data), headers)
        if put_resp is None:
            print("Failed to submit to presigned URL")
            sys.exit(1)
        if self.debug:
            print(f"Upload file finished with: {put_resp.status_code}")
        if put_resp.status_code != 200:
            print(f"Failed to submit to presigned URL, status code {put_resp.status_code}")
            sys.exit(1)

    def json_to_csv(self, json_obj: List[Any]) -> None:
        with open(self.dump_csv, 'w', newline='') as ui_out_csv:
            wr = csv.writer(ui_out_csv, delimiter=',')
            row1 = [Constants.RULENAME]
            for elem in json_obj:
                mutant_name = os.path.basename(elem[Constants.NAME])
                if not mutant_name:
                    print("Mutant name cannot be empty at this stage.")
                    sys.exit(1)
                name = elem[Constants.ID] + "_" + mutant_name
                row1.append(name)
            wr.writerow(row1)
            rnames = [rule[Constants.NAME] for rule in json_obj[0][Constants.RULES]]
            for to in json_obj[0][Constants.TIMEOUT]:
                rnames.append(to)
            for uk in json_obj[0][Constants.UNKNOWN]:
                rnames.append(uk)
            for sf in json_obj[0][Constants.SANITY_FAIL]:
                rnames.append(sf)
            for rnm in rnames:
                statuses = []
                for elem in json_obj:
                    status = [r[Constants.STATUS] for r in elem[Constants.RULES]
                              if Constants.NAME in r and Constants.STATUS in r and r[Constants.NAME] == rnm]
                    if status:
                        # the same rule should not appear more than once
                        if len(status) > 1:
                            print(f"Found rule {rnm} twice for a mutant."
                                  f"Malformed json input to this function.")
                            sys.exit(1)
                        statuses.append(status[0])
                    elif elem[Constants.SANITY_FAIL]:
                        for r in elem[Constants.SANITY_FAIL]:
                            if r == rnm:
                                statuses.append(Constants.SANITY_FAIL)
                    else:
                        statuses.append("TIMEOUT/UNKNOWN")
                row = [rnm] + statuses
                wr.writerow(row)

    def get_results(self, link: str, fetcher: ReportFetcher) -> Optional[List[RuleResult]]:
        if link is None:
            return None
        if isinstance(fetcher, FileFetcher):
            output_json = fetcher.get_output_json(link)
            if output_json is None:
                print(f"failed to get results for {link}")
                return None

            if Constants.RULES not in output_json:
                if self.debug:
                    print(f"Bad format for {Constants.OUTPUTJSON}")
                return None
        elif isinstance(fetcher, WebFetcher):
            job_data = fetcher.get_job_data(link)
            if job_data is None:
                print(f"failed to get job data for {link}")
                return None

            job_status = job_data.get(Constants.JOB_STATUS, "")
            if job_status not in FinalJobStatus.get_statuses():
                # The job is not completed yet
                return None
        else:
            print("Unexpected format. Can't proceed with the request. Please contact Certora")
            return None

        # now we no longer use output_json

        progress_json = fetcher.get_treeview_json(link)
        if progress_json is None:
            print("Could not get progress object")
            return None
        top_level_rules = get_top_level_rules(progress_json)
        if top_level_rules is None:
            print("Could not get tree view object")
            return None
        rule_results = []

        for rule in top_level_rules:
            # as long as we have children, we need to keep looking.
            # we prioritize failures, then unknown, then timeout, then sanity_fail, and only all success is a success
            if Constants.CHILDREN not in rule:
                print(f"Bad format for a rule {rule}")
                return None

            if Constants.NAME not in rule:
                print(f"Bad format for a rule {rule}")
                return None

            leaf_statuses: List[str] = []
            rec_collect_statuses_children(rule, leaf_statuses)
            name = rule[Constants.NAME]
            if len(leaf_statuses) == 0:
                print("Got no rule results")
                return None
            elif any([s == MutationTestRuleStatus.FAIL for s in leaf_statuses]):
                rule_results.append(RuleResult(name, MutationTestRuleStatus.FAIL))
            elif any([s == MutationTestRuleStatus.UNKNOWN for s in leaf_statuses]):
                rule_results.append(RuleResult(name, MutationTestRuleStatus.UNKNOWN))
            elif any([s == MutationTestRuleStatus.TIMEOUT for s in leaf_statuses]):
                rule_results.append(RuleResult(name, MutationTestRuleStatus.TIMEOUT))
            elif any([s == MutationTestRuleStatus.SANITY_FAIL for s in leaf_statuses]):
                rule_results.append(RuleResult(name, MutationTestRuleStatus.SANITY_FAIL))
            elif not all([s == MutationTestRuleStatus.SUCCESS for s in leaf_statuses]):
                print("Encountered a new unknown status which isn't FAIL, UNKNOWN, TIMEOUT, SANITY_FAIL, or SUCCESS")
                return None
            else:
                rule_results.append(RuleResult(name, MutationTestRuleStatus.SUCCESS))

        print(f"Successfully retrieved results for {link}")

        return rule_results

    def poll_collect(self) -> None:
        SECONDS_IN_MINUTE = 60
        poll_timeout_seconds = self.poll_timeout * SECONDS_IN_MINUTE
        start = time.time()
        duration = 0  # seconds
        attempt_number = 1
        retry = 15
        ready = False
        while duration < poll_timeout_seconds:
            print(f"-------> Trying to poll results... attempt #{attempt_number}")
            ready = self.collect()
            if not ready:
                print(f"-------> Results are still not ready, trying in {retry} seconds")
                attempt_number += 1
                time.sleep(retry)
            else:
                # upload the results file to the cloud
                final_report = read_file(self.ui_out)
                web_utils = WebUtils(self.args)
                id, anonymous_key, pre_signed_url = self.get_mutation_test_final_report_url(web_utils)
                self.upload_file_to_cloud_storage(web_utils, pre_signed_url, final_report)
                print_final_report_url_msg(web_utils.mutation_test_final_result_url, id, anonymous_key)
                return
            duration = int(time.time() - start)

        if not ready:
            print(f"Could not get results after {attempt_number} attempts. Exiting")
            sys.exit(1)


def rec_collect_statuses_children(rule: Dict[str, Any], statuses: List[str]) -> None:
    statuses.append(convert_to_mutation_testing_status(rule[Constants.STATUS]))
    for child in rule[Constants.CHILDREN]:
        rec_collect_statuses_children(child, statuses)


def get_file_url_from_orig_url(url: str, file: str) -> str:
    parsed_url = urllib3.util.parse_url(url)
    file_url = f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
    # ensure there is a single slash
    if not file_url.endswith("/"):
        file_url += "/"
    file_url += f"{file}?{parsed_url.query}"
    return file_url


def get_top_level_rules(progress_json: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    if Constants.VERIFICATION_PROGRESS not in progress_json:
        print(f"Could not find {Constants.VERIFICATION_PROGRESS} in progress {progress_json}")
        return None
    # verification progress holds a string which is a json encoding of the latest tree view file
    tree_view_json = json.loads(progress_json[Constants.VERIFICATION_PROGRESS])
    if Constants.RULES not in tree_view_json:
        print(f"Could not find rules in tree view file {tree_view_json}")
        return None
    return tree_view_json[Constants.RULES]


class Constants(StrEnum):
    VERIFICATION_PROGRESS = "verificationProgress"
    RULENAME = "RULENAME"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"
    SANITY_FAIL = "SANITY_FAIL"
    RULES = "rules"
    JOB_STATUS = "jobStatus"
    JOB_DATA = "jobData"
    PROGRESS = "progress"
    ZIPOUTPUT = "zipOutput"
    GENERALSTATE = "generalState"
    PARAMS = "params"
    OUTPUT = "output"
    INPUTS = "inputs"
    TARNAME = "TarName"
    NAME = "name"
    ID = "id"
    COLLECT_SIGNED_URL = "preSignedUrl"
    DIFF = "diff"
    DESCRIPTION = "description"
    ORIGINAL = "original"
    MUTANTS = "mutants"
    GAMBIT_MUTANT = "gambit_mutant"
    GAMBIT_OUT = "gambit_out"
    GAMBIT = "gambit"
    GAMBIT_OUTDIR = "outdir"
    FILENAME = "filename"
    FILES = "files"
    LINK = "link"
    RULE_REPORT_LINK = "rule_report_link"
    CERTORA_KEY = "certoraKey"
    ANONYMOUS_KEY = "anonymousKey"
    PRE_SIGNED_URL = "preSignedUrl"
    STATUS = "status"
    CHILDREN = "children"
    NUM_MUTANTS = "num_mutants"
    MANUAL_MUTANTS = "manual_mutants"
    MSG = "msg"
    TMP_GAMBIT = "tmp_gambit.conf"
    SOLC = "solc"
    PACKAGES = "packages"
    SOLC_REMAPPINGS = "solc_remappings"
    SOLC_ALLOW_PATH = "solc_allow_path"  # why
    SOLC_ALLOW_PATHS = "solc_allow_paths"  # just, why
    ZIP_PATH = "zip_output_certora_mutate.tar.gz"
    CERTORA_MUTATE_SOURCES = ".certora_mutate_sources"
    APPLIED_MUTANTS_DIR_NAME = "applied_mutants"
    SERVER = "server"
    STAGING = "staging"
    PRODUCTION = "production"
    DEV = "vaas-dev"
    CONF = "conf"
    ORIG_RUN_PROVER_CONF = "cvt_conf_for_certoraMutate.conf"
    PROVER_DOTCOM = "prover.certora.com"
    STAGING_DOTCOM = "vaas-stg.certora.com"
    DEV_DOTCOM = "vaas-dev.certora.com"
    MUTATION_TEST_REPORT_PRODUCTION = "mutation-testing.certora.com"
    MUTATION_TEST_REPORT_STAGING = "mutation-testing-beta.certora.com"
    MUTATION_TEST_REPORT_DEV = "mutation-testing-dev.certora.com"
    OUTPUTJSON = "output.json"
    REPORTS = "Reports"


certora_key = os.getenv(KEY_ENV_VAR, '')
auth_headers = {"Authorization": f"Bearer {certora_key}", "Content-Type": "application/json"}
default_cookies = {str(Constants.CERTORA_KEY): os.getenv(KEY_ENV_VAR, '')}


class FileFetcher(ReportFetcher):

    # in the file fetcher, all links are to the main emv directory
    def get_output_json(self, link: str) -> Optional[Dict[str, Any]]:
        output_path = Path(link) / Constants.REPORTS / Constants.OUTPUTJSON
        if not output_path.is_file():
            print(f"Got no {Constants.OUTPUTJSON} file")
            return None

        with open(output_path, 'r') as output_handle:
            output_json = json.load(output_handle)

        return output_json

    def get_treeview_json(self, link: str) -> Optional[Dict[str, Any]]:
        # it's a hack, but in web we need to go through the verificationProgress and locally we don't.
        treeview_path = Path(link) / Constants.REPORTS / "treeView"

        # look out for the "latest" tree view file
        candidates = list(treeview_path.glob(r"treeViewStatus_*.json"))
        max = None
        max_no = -1
        for candidate in candidates:
            if candidate.is_file():
                index = int(str(candidate.stem).split("_")[1])
                if index > max_no:
                    max = candidate
                    max_no = index
        # max should contain the latest tree view file
        if max is None:
            print("No matching treeview files found")
            return None

        treeview_file = max
        with open(treeview_file, 'r') as treeview_handle:
            treeview_str = json.load(treeview_handle)

        # wrap the json as a string inside another json mimicking progress URL
        return {Constants.VERIFICATION_PROGRESS: json.dumps(treeview_str)}


class WebFetcher(ReportFetcher):
    def __init__(self, _web_utils: WebUtils, debug: bool = False):
        self.web_utils = _web_utils
        self.verification_report_path_pattern = re.compile(r"^\/output\/\d+\/[0-9a-fA-F]*(\/)?$")
        self.job_status_path_pattern = re.compile(r"^\/jobStatus\/\d+\/[0-9a-fA-F]*(\/)?$")
        self.debug = debug

    @staticmethod
    def get_url_path(url: str) -> Optional[str]:
        parsed_url = urllib3.util.parse_url(url)
        return parsed_url.path

    def get_resource_url(self, url: str, keyword: str) -> str:
        url_path = self.get_url_path(url)
        if not url_path:
            print("Invalid URL was provided")
            if self.debug:
                print(url)
            sys.exit(3)
        # we check both the status page and the verification report for
        # backward compatibility
        if re.match(self.verification_report_path_pattern, url_path):
            resource_url = url.replace(Constants.OUTPUT, keyword)
        elif re.match(self.job_status_path_pattern, url_path):
            resource_url = url.replace(Constants.JOB_STATUS, keyword)
        else:
            print("Unknown URL was provided")
            if self.debug:
                print(url)
            sys.exit(3)
        return resource_url

    def get_output_json(self, url: str) -> Optional[Dict[str, Any]]:
        output_url = self.get_resource_url(url, Constants.OUTPUT)
        return self.parse_response(
            get_file_url_from_orig_url(output_url, Constants.OUTPUTJSON),
            Constants.OUTPUTJSON
        )

    def get_treeview_json(self, url: str) -> Optional[Dict[str, Any]]:
        progress_url = self.get_resource_url(url, Constants.PROGRESS)
        return self.parse_response(progress_url, "treeview.json")

    def get_job_data(self, url: str) -> Optional[Dict[str, Any]]:
        job_data_url = self.get_resource_url(url, Constants.JOB_DATA)
        return self.parse_response(job_data_url, "job data")

    def parse_response(self, url: str, resource: str) -> Optional[Dict[str, Any]]:
        response = self.web_utils.get_response_with_timeout(url)
        if response is None or response.status_code != 200:
            print(f"Got bad response code when fetching {resource} {response.status_code if response else ''}")
            return None
        return response.json()


def gambit_entry_point() -> None:
    args = parse_args()
    certoraMutate = CertoraMutate(args)
    certoraMutate.validate_args()

    if args.conf_output_file:
        certoraMutate.auto_config()
        sys.exit(0)

    # default mode is async. That is, we either _submit_ or _collect_, not both
    if not args.sync:
        # if the user did not supply a conf file or a link to an original run,
        # we will check whether there is a collect file and poll it
        if not args.prover_conf and not args.orig_run:
            ready = certoraMutate.collect()
            if not ready:
                print("Note that the report might broken because some results could not be fetched. "
                      f"Check the {args.collect_file} file to investigate.")
                sys.exit(1)
        else:
            check_key_exists()
            certoraMutate.submit()
    else:
        check_key_exists()
        # sync mode means we submit, then we poll for the specified amount of minutes
        if not args.prover_conf and not args.orig_run:
            # sync mode means we submit + collect. If the user just wants to collect, do not add --sync
            print("Must provide a conf file in sync mode. If you wish to poll on a previous submission,"
                  "omit `--sync`.")
            sys.exit(1)
        certoraMutate.submit()
        certoraMutate.poll_collect()


if __name__ == '__main__':
    gambit_entry_point()
