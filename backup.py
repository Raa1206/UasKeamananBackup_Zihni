import logging
import pyzipper
from pathlib import Path
from datetime import datetime
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from dotenv import load_dotenv
import os

logging.basicConfig(
    filename="backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load konfigurasi .env

load_dotenv()

key_id = os.getenv("B2_KEY_ID")
app_key = os.getenv("B2_APPLICATION_KEY")
bucket_name = os.getenv("B2_BUCKET_NAME")
aes_password = os.getenv("AES_PASSWORD")

if not key_id or not app_key or not bucket_name or not aes_password:
    raise ValueError("Konfigurasi .env belum lengkap")

password = aes_password.encode()

# Pembuatan ZIP terenkripsi

source = Path("data_backup")

files = [f for f in source.rglob("*") if f.is_file()]

print("File yang akan di-backup:", [f.name for f in files])

zip_name = f"backup_{datetime.now():%Y%m%d_%H%M%S}.zip"

with pyzipper.AESZipFile(
    zip_name,
    "w",
    compression=pyzipper.ZIP_DEFLATED,
    encryption=pyzipper.WZ_AES,
) as zf:

    zf.setpassword(password)

    for file in files:
        zf.write(file, arcname=file.name)

print(f"Backup terenkripsi berhasil dibuat: {zip_name}")
logging.info(f"Backup terenkripsi dibuat: {zip_name}")

# Upload ke Backblaze B2

info = InMemoryAccountInfo()
b2_api = B2Api(info)

b2_api.authorize_account(
    "production",
    key_id,
    app_key
)

bucket = b2_api.get_bucket_by_name(bucket_name)

bucket.upload_local_file(
    local_file=zip_name,
    file_name=zip_name,
)

print("File berhasil diunggah ke Backblaze B2.")
logging.info(f"Upload berhasil ke Backblaze B2: {zip_name}")