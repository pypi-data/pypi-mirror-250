import os
import subprocess
import threading
import time
import traceback
from threading import RLock
from typing import Optional

import click
import psutil

from nrp_devtools.commands.ui.link_assets import link_assets
from nrp_devtools.config import OARepoConfig


class Runner:
    python_server_process: Optional[subprocess.Popen] = None
    webpack_server_process: Optional[subprocess.Popen] = None
    file_watcher_thread: Optional[threading.Thread] = None
    file_watcher_stopping = None

    def __init__(self, config: OARepoConfig):
        self.config = config

    def start_python_server(self, development_mode=False):
        click.secho("Starting python server", fg="yellow")
        environment = {}
        if development_mode:
            environment["FLASK_DEBUG"] = "1"
            environment["INVENIO_TEMPLATES_AUTO_RELOAD"] = "1"
        self.python_server_process = subprocess.Popen(
            [
                self.config.invenio_command,
                "run",
                "--cert",
                self.config.repository_dir / "docker" / "development.crt",
                "--key",
                self.config.repository_dir / "docker" / "development.key",
            ],
            env={**os.environ, **environment},
        )
        for i in range(5):
            time.sleep(2)
            if self.python_server_process.poll() is not None:
                click.secho(
                    "Python server failed to start. Fix the problem and type 'server' to reload",
                    fg="red",
                )
                self.python_server_process.wait()
                self.python_server_process = None
                time.sleep(10)
                break
        click.secho("Python server started", fg="green")

    def start_webpack_server(self):
        click.secho("Starting webpack server", fg="yellow")
        manifest_path = (
            self.config.invenio_instance_path / "static" / "dist" / "manifest.json"
        )
        if manifest_path.exists():
            manifest_path.unlink()

        self.webpack_server_process = subprocess.Popen(
            [
                "npm",
                "run",
                "start",
            ],
            cwd=self.config.invenio_instance_path / "assets",
        )
        # wait at most a minute for webpack to start
        for i in range(60):
            time.sleep(2)
            if self.webpack_server_process.poll() is not None:
                click.secho(
                    "Webpack server failed to start. Fix the problem and type 'ui' to reload",
                    fg="red",
                )
                self.webpack_server_process.wait()
                self.webpack_server_process = None
                time.sleep(10)
                break

            if manifest_path.exists():
                manifest_data = manifest_path.read_text()
                if '"status": "done"' in manifest_data:
                    click.secho("Webpack server is running", fg="green")
                    break
        click.secho("Webpack server started", fg="green")

    def start_file_watcher(self):
        click.secho("Starting file watcher", fg="yellow")

        def watch_files():
            while True:
                if self.file_watcher_stopping.acquire(timeout=1):
                    break

        self.file_watcher_stopping = RLock()
        self.file_watcher_stopping.acquire()

        self.file_watcher_thread = threading.Thread(target=watch_files, daemon=True)
        self.file_watcher_thread.start()
        click.secho("File watcher started", fg="green")

    def stop(self):
        self.stop_python_server()
        self.stop_webpack_server()
        self.stop_file_watcher()

    def restart_python_server(self, development_mode=False):
        try:
            self.stop_python_server()
            self.start_python_server(development_mode=development_mode)
        except:
            traceback.print_exc()

    def restart_webpack_server(self):
        try:
            self.stop_webpack_server()
            self.stop_file_watcher()
            # just for being sure, link assets
            # (they might have changed and were not registered before)
            link_assets(self.config)
            self.start_file_watcher()
            self.start_webpack_server()
        except:
            traceback.print_exc()

    def stop_python_server(self):
        click.secho("Stopping python server", fg="yellow")
        if self.python_server_process:
            self.python_server_process.terminate()
            try:
                self.python_server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                click.secho(
                    "Python server did not stop in time, killing it", fg="yellow"
                )
                self._kill_process_tree(self.python_server_process)
            self.python_server_process = None

    def stop_webpack_server(self):
        click.secho("Stopping webpack server", fg="yellow")
        if self.webpack_server_process:
            self.webpack_server_process.terminate()
            try:
                self.webpack_server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                click.secho(
                    "Webpack server did not stop in time, killing it", fg="yellow"
                )
                self._kill_process_tree(self.webpack_server_process)
            self.webpack_server_process = None

    def stop_file_watcher(self):
        click.secho("Stopping file watcher", fg="yellow")
        if self.file_watcher_thread:
            self.file_watcher_stopping.release()
            self.file_watcher_thread.join()
            self.file_watcher_thread = None
            self.file_watcher_stopping = None

    def _kill_process_tree(self, process_tree: subprocess.Popen):
        parent_pid = process_tree.pid
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
