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

#kode pembuatan ZIP

password = b"REMOVED_PASSWORD"
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

#kode upload ke Backblaze B2

info = InMemoryAccountInfo()
b2_api = B2Api(info)
load_dotenv()
key_id = os.getenv("B2_KEY_ID")
app_key = os.getenv("B2_APPLICATION_KEY")
if not key_id or not app_key:
    raise ValueError("B2_KEY_ID atau B2_APPLICATION_KEY tidak ditemukan. Periksa file .env Anda.")
b2_api.authorize_account(
    "production",
    key_id,
    app_key
)

bucket = b2_api.get_bucket_by_name("zihni.tamara.barus-backup.uas")
bucket.upload_local_file(
    local_file=zip_name,
    file_name=zip_name,
)

print("File berhasil diunggah ke Backblaze B2.")
logging.info(f"Upload berhasil ke Backblaze B2: {zip_name}")