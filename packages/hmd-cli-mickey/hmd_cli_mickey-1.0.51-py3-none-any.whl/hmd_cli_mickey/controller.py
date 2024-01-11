import json
import os
from importlib.metadata import version
from pathlib import Path

from cement import Controller, ex
from hmd_cli_tools import get_version, load_hmd_env

VERSION_BANNER = """
hmd generate version: {}
"""

VERSION = version("hmd_cli_mickey")


class LocalController(Controller):
    class Meta:
        label = "mickey"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Runs the hmd-tf-mickey transform on a project"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the generate command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(VERSION),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="build <...>",
        arguments=[
            (
                [],
                {
                    "help": "key in manifest.json generate section to use, optional",
                    "action": "store",
                    "dest": "runs",
                    "nargs": "*",
                    "default": [],
                },
            ),
            (
                ["-t", "--template"],
                {
                    "help": "Glob expression for templates to render",
                    "action": "store",
                    "dest": "templates",
                    "required": False,
                    "nargs": "*",
                    "default": [],
                },
            ),
            (
                ["-c", "--context"],
                {
                    "help": "Glob expression for context files",
                    "action": "store",
                    "dest": "contexts",
                    "required": False,
                    "nargs": "*",
                    "default": [],
                },
            ),
            (
                ["-rp", "--repo-path", "-p"],
                {
                    "help": "Path to repository to run command",
                    "action": "store",
                    "dest": "repo_path",
                    "required": False,
                    "default": os.getcwd(),
                },
            ),
            (
                ["-v", "--var"],
                {
                    "help": "set variable in data context, NAME:VALUE",
                    "action": "store",
                    "dest": "vars",
                    "required": False,
                    "nargs": "*",
                    "default": [],
                },
            ),
            (
                ["-V", "--var-file"],
                {
                    "help": "JSON file of variable values",
                    "action": "store",
                    "dest": "var_file",
                    "required": False,
                    "nargs": "*",
                    "default": [],
                },
            ),
            (
                ["-d", "--deps"],
                {
                    "help": "download remote templates",
                    "action": "store_true",
                    "dest": "deps",
                    "required": False,
                    "default": False,
                },
            ),
            (
                ["-ln", "--links"],
                {
                    "help": "volumes to mount for remote artifacts, uses Docker volumes syntax",
                    "action": "store",
                    "dest": "links",
                    "required": False,
                    "nargs": "*",
                    "default": [],
                },
            ),
        ],
    )
    def build(self):
        HMD_HOME = os.environ.get("HMD_HOME", None)
        if HMD_HOME:
            load_hmd_env(override=False)
        else:
            print(
                "WARNING: HMD_HOME environment variable not set. Using only session variables"
            )

        args = {}
        # build the args values...
        if "runs" not in self.app.pargs:
            self.app.pargs.runs = []
        runs = self.app.pargs.runs if self.app.pargs.runs is not None else []

        if "templates" not in self.app.pargs:
            self.app.pargs.templates = []
        templates = (
            self.app.pargs.templates if self.app.pargs.templates is not None else []
        )

        if "contexts" not in self.app.pargs:
            self.app.pargs.contexts = []
        contexts = (
            self.app.pargs.contexts if self.app.pargs.contexts is not None else []
        )

        if "vars" not in self.app.pargs:
            self.app.pargs.vars = []
        arg_vars = self.app.pargs.vars if self.app.pargs.vars is not None else []

        if "templates" not in self.app.pargs:
            self.app.pargs.templates = []

        if "var_file" not in self.app.pargs:
            self.app.pargs.var_file = []
        var_file = self.app.pargs.var_file

        if "repo_path" not in self.app.pargs:
            self.app.pargs.repo_path = os.getcwd()
        repo_path = self.app.pargs.repo_path

        if "deps" not in self.app.pargs:
            self.app.pargs.deps = True
        deps = self.app.pargs.deps

        if "links" not in self.app.pargs:
            self.app.pargs.links = []
        links = self.app.pargs.links
        image_name = f"{os.environ.get('HMD_CONTAINER_REGISTRY', 'ghcr.io/neuronsphere')}/hmd-tf-mickey"
        vars_dict = {
            v[0]: v[1] for v in list(map(lambda var: var.split(":"), arg_vars))
        }

        for v_file in var_file:
            with open(v_file, "r") as vb:
                vars_dict = {**json.load(vb), **vars_dict}

        args.update(
            {
                "image_name": image_name,
                "runs": runs,
                "templates": templates,
                "contexts": contexts,
                "variables": vars_dict,
                "repo_path": repo_path,
                "deps": deps,
                "links": links,
                "repo_version": self.app.pargs.repo_version,
            }
        )

        from .hmd_cli_mickey import build as do_build

        result = do_build(**args)

    @ex(label="init", help="Initialize new Mickey project")
    def init(self):
        from .hmd_cli_mickey import init as do_init

        do_init()

    @ex(help="Force pull new hmd-tf-mickey image")
    def update_image(self):
        from .hmd_cli_mickey import update_image as do_update_image

        image_name = f"{os.environ.get('HMD_CONTAINER_REGISTRY', 'ghcr.io/neuronsphere')}/hmd-tf-mickey"
        img_tag = os.environ.get("HMD_TF_MICKEY_VERSION", "stable")

        do_update_image(image_name=f"{image_name}:{img_tag}")

    @ex(
        help="remove all generated files",
        arguments=[
            (
                [],
                {
                    "help": "key in manifest.json generate section to use, optional",
                    "action": "store",
                    "dest": "runs",
                    "nargs": "*",
                    "default": [],
                },
            ),
            (
                ["-ln", "--links"],
                {
                    "help": "volumes to mount for remote artifacts, uses Docker volumes syntax",
                    "action": "store",
                    "dest": "links",
                    "required": False,
                    "nargs": "*",
                    "default": [],
                },
            ),
        ],
    )
    def clean(self):
        HMD_HOME = os.environ.get("HMD_HOME", None)
        if HMD_HOME:
            load_hmd_env(override=False)
        else:
            print(
                "WARNING: HMD_HOME environment variable not set. Using only session variables"
            )
        args = {}
        # build the args values...
        if "runs" not in self.app.pargs:
            self.app.pargs.runs = []
        runs = self.app.pargs.runs if self.app.pargs.runs is not None else []
        if "links" not in self.app.pargs:
            self.app.pargs.links = []
        links = self.app.pargs.links
        image_name = f"{os.environ.get('HMD_CONTAINER_REGISTRY', 'ghcr.io/neuronsphere')}/hmd-tf-mickey"

        if "repo_path" not in self.app.pargs:
            self.app.pargs.repo_path = os.getcwd()
        repo_path = self.app.pargs.repo_path

        args.update(
            {
                "image_name": image_name,
                "runs": runs,
                "templates": [],
                "contexts": [],
                "variables": {},
                "repo_path": repo_path,
                "deps": False,
                "links": links,
                "repo_version": self.app.pargs.repo_version,
                "cmd": "clean",
            }
        )

        from .hmd_cli_mickey import build as do_build

        result = do_build(**args)
