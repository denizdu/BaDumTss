import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def convert_cookies(json_cookies_file, netscape_cookies_file):
    """Convert an explicit JSON cookie export to Netscape format."""
    with Path(json_cookies_file).open(encoding="utf-8") as file:
        cookies = json.load(file)

    with Path(netscape_cookies_file).open("w", encoding="utf-8") as file:
        file.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie["domain"]
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = cookie["path"]
            secure = "TRUE" if cookie["secure"] else "FALSE"
            expiration = str(int(cookie.get("expirationDate", 0)))
            name = cookie["name"]
            value = cookie["value"]
            file.write(
                f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n"
            )
    return Path(netscape_cookies_file)


def main():
    output_file = convert_cookies(
        PROJECT_ROOT / "cookies.json", PROJECT_ROOT / "cookies.txt"
    )
    print(f"Cookies converted to Netscape format: {output_file}")


if __name__ == "__main__":
    main()
