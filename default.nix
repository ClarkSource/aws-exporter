with import <nixpkgs> {};

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
