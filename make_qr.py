import urllib.request

wedding_url = "https://ryu1127.github.io/260822_wedding/"
qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={wedding_url}"

try:
    print("Generating QR code...")
    urllib.request.urlretrieve(qr_api_url, "qr.png")
    print("Success! 'qr.png' has been created.")
except Exception as e:
    print(f"Error: {e}")
