from ._version import __version__

import sys
import warnings
from pathlib import Path

from traitlets import Bool, Unicode

from datalayer.application import DatalayerApp, NoStart, base_aliases, base_flags

HERE = Path(__file__).parent


jupyter_embed_aliases = dict(base_aliases)
jupyter_embed_aliases["cloud"] = "JupyterEmbedApp.cloud"

jupyter_embed_flags = dict(base_flags)
jupyter_embed_flags["dev-build"] = (
    {"JupyterEmbedApp": {"dev_build": True}},
    "Build in development mode.",
)
jupyter_embed_flags["no-minimize"] = (
    {"JupyterEmbedApp": {"minimize": False}},
    "Do not minimize a production build.",
)


class ConfigExportApp(DatalayerApp):
    """An application to export the configuration."""

    version = __version__
    description = """
   An application to export the configuration
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for workspace export.")
            self.exit(1)
        self.log.info("JupyterEmbedConfigApp %s", self.version)


class JupyterEmbedConfigApp(DatalayerApp):
    """A config app."""

    version = __version__
    description = """
    Manage the configuration
    """

    subcommands = {}
    subcommands["export"] = (
        ConfigExportApp,
        ConfigExportApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error("One of `export` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class JupyterEmbedShellApp(DatalayerApp):
    """A shell app."""

    version = __version__
    description = """
    Run predefined scripts.
    """

    def start(self):
        super().start()
        args = sys.argv
        self.log.info(args)
            


class JupyterEmbedApp(DatalayerApp):
    name = "jupyter_embed"
    description = """
    Import or export a JupyterLab workspace or list all the JupyterLab workspaces

    You can use the "config" sub-commands.
    """
    version = __version__

    aliases = jupyter_embed_aliases
    flags = jupyter_embed_flags

    cloud = Unicode("ovh", config=True, help="")

    minimize = Bool(True, config=True, help="")

    subcommands = {
        "config": (JupyterEmbedConfigApp, JupyterEmbedConfigApp.description.splitlines()[0]),
        "sh": (JupyterEmbedShellApp, JupyterEmbedShellApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments"""
        super().initialize()

    def start(self):
        super(JupyterEmbedApp, self).start()
        self.log.info("JupyterEmbed - Version %s - Cloud %s ", self.version, self.cloud)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterEmbedApp.launch_instance

if __name__ == "__main__":
    main()
