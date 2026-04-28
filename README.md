Original [README.md](./README.md)

## AI Disclaimer:
I've used ChatGPT to generate basic structure for HTML files. They were edited further after that, but first iteration was generated
by ChatGPT. I've also auto-generated [models.py](./py/compmatrix/models.py) since it's a boilerplate.

## Nix setup:
I'm using flakes based NixOS installation, so as to not pollute my system I've added basic wrapper around your `default.nix` file.
It doesn't do anything, except wrapping the file. I'm not actually sure, where `nix-shell` shells live, but I assumed that they live
in different place than flakes, and the usual cleaning commands that I use to clean my system from time to time won't work.
