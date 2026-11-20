{
    description = "Tiny, performant, native Discord client written in Rust (egui/wgpu)";

    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
        flake-parts = {
            url = "github:hercules-ci/flake-parts";
            inputs.nixpkgs-lib.follows = "nixpkgs";
        };
    };

    outputs = inputs @ {
        self,
        nixpkgs,
        flake-parts,
        ...
    }:
        flake-parts.lib.mkFlake {inherit inputs;} {
            systems = [
                "x86_64-linux"
                "aarch64-darwin"
            ];

            perSystem = {
                config,
                pkgs,
                system,
                ...
            }: {
                packages.rustcord = pkgs.callPackage ./packaging/nix/package.nix {};
                packages.serein = config.packages.rustcord;
                packages.default = config.packages.rustcord;

                devShells.default = pkgs.mkShell {
                    name = "rustcord-dev";

                    inputsFrom = [config.packages.rustcord];
                };
            };
        };
}
