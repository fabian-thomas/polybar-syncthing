{ buildPythonPackage
, fetchFromGitHub
, setuptools
, requests
, dateutil
, applyPatches
}:

buildPythonPackage rec {
  pname = "syncthing";
  version = "2.4.3";
  format = "pyproject";

  src = (applyPatches {
    src = (fetchFromGitHub {
        owner = "blakev";
        repo = "python-syncthing";
        rev = "0d1e968a9d3a15f152a67b053b98a50c7361cd20";
        hash = "sha256-QEwkwnUq8RH5ntQSnlEjzjijRGktZaiK/BSEQc0kM+s=";
    });
    patches = [ ./python-syncthing.patch ];
  });

  nativeBuildInputs = [
    setuptools
  ];

  propagatedBuildInputs = [
    requests
    dateutil
  ];
}
