{ stdenv, python3 }:

stdenv.mkDerivation {
  pname = "polybar-syncthing";
  version = "1.0";

  src = ./.;

  buildInputs = [
    (python3.withPackages (p: with p; [ (callPackage ./python-syncthing.nix {}) ]))
  ];

  phases = [ "installPhase" "fixupPhase" ];

  installPhase = ''
    mkdir -p $out/bin
    cp $src/polybar-syncthing.py $out/bin/polybar-syncthing
  '';
}
