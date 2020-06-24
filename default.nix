with import <nixpkgs> {};

let
  pythonEnv = python38.withPackages (ps: [
  ]);
in pkgs.mkShell {
  buildInputs = [
    pre-commit
    pythonEnv
  ];

  shellHook = ''
    export PATH="$PATH:$HOME/.yarn/bin"
  '';
}
