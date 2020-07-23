with import <nixpkgs> {};

# let
#   mach-nix = import (
#     builtins.fetchGit {
#       url = "https://github.com/DavHau/mach-nix/";
#       ref = "2.1.0";
#     }
#   );
# in
# mach-nix.mkPythonShell {
#   requirements = ''
#     wheel
#     setuptools
#     prometheus_client
#     boto3
#     tox
#     pre-commit
#     nodeenv
#   '';
# }

let
  aws_exporter = with python3.pkgs; buildPythonApplication rec {
    pname = "aws_exporter";
    version = "dev";

    src = ./.;

    # No tests included
    doCheck = false;

    nativeBuildInputs = [
      git
    ];

    propagatedBuildInputs = [
      boto3
      prometheus_client
    ];

    meta = with lib; {
      homepage = "https://github.com/clarksource/aws-exporter";
      license = licenses.isc;
    };
  };
in with python3.pkgs; pkgs.mkShell {
  buildInputs = [
    aws_exporter
    setuptools
    pre-commit
    tox
  ];
}
