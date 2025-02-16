import json

json_cookies_file = "C://Users//denizdu//OneDrive//Masaüstü//BaDumTss//cookies.json"
netscape_cookies_file = "C://Users//denizdu//OneDrive//Masaüstü//BaDumTss//cookies.txt"

# JSON dosyasını oku
with open(json_cookies_file, "r", encoding="utf-8") as f:
    cookies = json.load(f)

# Netscape formatına çevir
with open(netscape_cookies_file, "w", encoding="utf-8") as f:
    f.write("# Netscape HTTP Cookie File\n")
    for cookie in cookies:
        domain = cookie["domain"]
        flag = "TRUE" if cookie["domain"].startswith(".") else "FALSE"
        path = cookie["path"]
        secure = "TRUE" if cookie["secure"] else "FALSE"
        expiration = str(int(cookie["expirationDate"])) if "expirationDate" in cookie else "0"
        name = cookie["name"]
        value = cookie["value"]
        f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n")

print(f"✅ Çerezler Netscape formatına çevrildi: {netscape_cookies_file}")
