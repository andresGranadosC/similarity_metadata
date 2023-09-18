{
  description = "Compute similarity between keywords and disciplines";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    # nix-filter.url = "github:numtide/nix-filter";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {inherit system;};
        python = pkgs.python310;
        nix-filter = self.inputs.nix-filter.lib;

        # build the spaCy language processing pipeline as a python package
        de_core_news_lg = with pkgs.python3Packages;
          buildPythonPackage rec {
            pname = "de_core_news_lg";
            version = "3.5.0";
            src = pkgs.fetchzip {
              url = "https://github.com/explosion/spacy-models/releases/download/${pname}-${version}/${pname}-${version}.tar.gz";
              hash = "sha256-oOrxOoe+SyleTsDO9WYB25Vvs4LX6B4aJPlGbMRsAk4=";
            };
            doCheck = false;
            propagatedBuildInputs = [
              spacy
              spacy-transformers
            ];
          };

        ### declare the python packages used for building, docs & development
        python-packages-build = python-packages:
          with python-packages; [
            de_core_news_lg
            numpy
            spacy
            uvicorn
            fastapi
            pydantic
          ];

          python-packages-devel = python-packages:
          with python-packages; [
            spacy
          ]
          ++ (python-packages-build python-packages);

        ### declare how the python package shall be built
        similarity = with python.pkgs; buildPythonPackage rec {
          pname = "similarity";
          version = "0.1.2";
          # only include the package-related files
          src = nix-filter {
            root = self;
            include = [
              "${pname}"
              ./setup.py
              ./requirements.txt
            ];
            exclude = [ (nix-filter.matchExt "pyc") ];
          };
          propagatedBuildInputs = (python-packages-build python.pkgs);
        };

      in {
        # default = import ./shell.nix { inherit pkgs; };
        packages.default = similarity;
        devShells.default = pkgs.mkShell {
          buildInputs = [
            (python.withPackages python-packages-devel)
            # python language server
            pkgs.nodePackages.pyright
          ];
        };

      }
    );}
