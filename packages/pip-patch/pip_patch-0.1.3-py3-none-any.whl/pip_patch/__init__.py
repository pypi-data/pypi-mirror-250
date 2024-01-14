import subprocess
import os
import sys


class PipPatch:
    root_dir = os.getcwd()
    working_dir = "site-packages"

    def __init__(self, package_name):
        if os.path.exists("package_info.txt"):
            os.remove("package_info.txt")
        if os.path.exists(self.working_dir):
            os.system(f"rm -rf {self.working_dir}")
        os.mkdir(self.working_dir)
        os.system(f"pip show {package_name} > package_info.txt")
        with open("package_info.txt", "r") as f:
            for line in f:
                if line.startswith("Name: "):
                    self.package_name = line.split(" ")[1].strip()
                if line.startswith("Location: "):
                    self.package_path = line.split(" ")[1].strip()
                if line.startswith("Version: "):
                    self.package_version = line.split(" ")[1].strip()
                if line.startswith("Home-page: "):
                    self.repo = line.split(" ")[1].strip()

    def download_original_package(self):
        subprocess.run(
            [
                "pip",
                "download",
                f"{self.package_name}=={self.package_version}",
                "--no-deps",
                "--no-binary",
                ":all:",
                "--dest",
                self.working_dir
            ],
            capture_output=True
        )
        uncompressed = False
        files = os.listdir(self.working_dir)
        if files:
            for file in os.listdir(self.working_dir):
                if file.endswith(".tar.gz"):
                    os.system(f"tar -xzf {self.working_dir}/{file} -C {self.working_dir} --strip-components=1")
                    uncompressed = True
                if file.endswith(".zip"):
                    os.system(f"unzip {self.working_dir}/{file} -d {self.working_dir}")
                    os.system(f"mv {self.working_dir}/{file.replace('.zip', '')}/* {self.working_dir}")
                    os.system(f"rm -rf {self.working_dir}/{file.replace('.zip', '')}")
                    uncompressed = True
        else:
            os.system(f"git clone {self.repo} {self.working_dir}")
            uncompressed = True
        if uncompressed:
            contents = subprocess.run(
                [
                    "find",
                    self.working_dir,
                    "-type",
                    "d",
                    "-maxdepth",
                    "1",
                    "-not",
                    "-name",
                    "*.egg-info",
                ],
                capture_output=True,
                text=True
            ).stdout.strip().split("\n")
            contents.remove(self.working_dir)
            contents = contents[0]
            contents = contents.replace(self.working_dir, "").strip("/")
            return contents

    def create_patch(self):
        if not self.package_path:
            return
        module_name = self.download_original_package()
        if not module_name:
            return
        patch_file = f"{self.package_name}-{self.package_version}.patch"
        os.system(f"cp -r {os.path.join(self.package_path, module_name)} {self.root_dir}")
        os.system(f'diff -u {os.path.join(self.working_dir, module_name)} {module_name} > "{patch_file}"')
        os.system(f"rm -rf {module_name}")
        os.system(f"rm -rf {self.working_dir}")
        os.system(f"rm package_info.txt")

    def apply_patch(self, patch_file):
        if not self.package_path:
            return
        installation_path = self.package_path.replace(self.working_dir, '')
        os.system(f"patch -d {installation_path} < {patch_file}")


def print_usage():
    print("Usage:\n"
          "  - pip-patch create <package_name> to create a patch file\n"
          "  - pip-patch apply <package_name> <patch_file> to apply a patch file")


def main():
    try:
        args = sys.argv[1:]
        print(args)
        if args[0] == "create":
            if len(args) < 2:
                raise IndexError
            pp = PipPatch(args[1])
            pp.create_patch()
        elif args[0] == "apply":
            pp = PipPatch(args[1])
            pp.apply_patch(args[2])
        else:
            print_usage()
    except IndexError:
        print_usage()


if __name__ == "__main__":
    main()
