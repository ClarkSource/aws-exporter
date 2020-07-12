with import <nixpkgs> {};

let
  mach-nix = import (
    builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "2.1.0";
    }
  );
in
mach-nix.mkPythonShell {
  requirements = ''
    wheel
    setuptools
    prometheus_client
    boto3
    tox
    pre-commit
    nodeenv
  '';
}
