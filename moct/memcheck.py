import subprocess


class MemCheck:
    def run(self):
        return self.check_frequency()

    def check_frequency(self):
        return self.get_frequency() != 2666

    def get_frequency(self):
        cmd = ["wmic", "memorychip", "get", "speed"]
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode("utf-8", errors="ignore").strip().split("\n")

        return int(lines[-1])
