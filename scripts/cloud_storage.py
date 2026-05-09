import os
from datetime import timedelta
from pathlib import Path
from urllib.request import urlopen

import pandas as pd
from dotenv import load_dotenv
from google.cloud import storage

BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_FILE = BASE_DIR / "config" / "gcp_service_account.json"
CSV_FILE = BASE_DIR / "csvs" / "heart.csv"
DOWNLOAD_DIR = BASE_DIR / "tmp"
PARQUET_FILE = DOWNLOAD_DIR / f"{CSV_FILE.stem}.parquet"
PARQUET_OBJECT_NAME = f"parquet/{PARQUET_FILE.name}"
SIGNED_URL_EXPIRATION = timedelta(minutes=2)

def main():
    load_dotenv(BASE_DIR / ".env")

    bucket_name = os.getenv("BUCKET_NAME")
    if not bucket_name:
        raise RuntimeError("BUCKET_NAME is missing from .env")

    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    bucket = client.bucket(bucket_name)

    DOWNLOAD_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(CSV_FILE)
    df.to_parquet(PARQUET_FILE, index=False)

    blob = bucket.blob(PARQUET_OBJECT_NAME)
    blob.upload_from_filename(
        PARQUET_FILE,
        content_type="application/octet-stream",
    )

    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=SIGNED_URL_EXPIRATION,
        method="GET",
    )

    download_path = DOWNLOAD_DIR / f"downloaded_{PARQUET_FILE.name}"
    with urlopen(signed_url) as response:
        download_path.write_bytes(response.read())

    print("Authenticated project:", client.project)
    print(f"Converted CSV to Parquet: {PARQUET_FILE}")
    print(f"Uploaded {PARQUET_OBJECT_NAME} to bucket: {bucket_name}")
    print(f"Signed URL expires in: {SIGNED_URL_EXPIRATION}")
    print(f"Downloaded via signed URL to: {download_path}")
    print("Signed URL:", signed_url)


if __name__ == "__main__":
    main()
