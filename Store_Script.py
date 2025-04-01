import os
import cloudinary
import cloudinary.api
import cloudinary.utils
import requests
import time
import subprocess
import traceback

# ✅ Configure Cloudinary
cloudinary.config(
    cloud_name="dwquzmwam",
    api_key="817587174551443",
    api_secret="7WMCvvjzdjUHY-nSONCd2K4clXw"
)

ALLOWED_FORMATS = {"pdf", "jpg", "jpeg", "png"}
API_URL = "http://localhost:8000/api/update_order_status/"  # Update your backend URL

# ✅ Track the last processed file
global last_processed_file
last_processed_file = None

def fetch_orders_from_cloudinary():
    try:
        print("🔎 Fetching the most recent order from Cloudinary...")
        resources = cloudinary.api.resources(
            type="upload",
            max_results=10,  # Fetch the most recent 10 files
            sort_by={"created_at": "desc"}  # Sort by creation date in descending order
        )

        if resources.get("resources"):
            recent_file = resources["resources"][0]
            global last_processed_file

            # Check if it's a new file
            if recent_file['public_id'] == last_processed_file:
                print("⚠️ No new files found. Waiting for new uploads.")
                return

            last_processed_file = recent_file['public_id']

            file_format = recent_file['format'].lower()
            if file_format not in ALLOWED_FORMATS:
                print(f"⚠️ Unsupported file format: {file_format}, skipping.")
                return

            file_url, _ = cloudinary.utils.cloudinary_url(
                recent_file['public_id'],
                format=file_format,
                secure=True
            )
            print(f"📄 Recent File: {recent_file['public_id']}.{file_format} | URL: {file_url}")
            download_and_print(file_url, recent_file['public_id'], file_format)
        else:
            print("⚠️ No files found in Cloudinary.")
    except Exception as e:
        print("❌ Error while fetching from Cloudinary:")
        traceback.print_exc()

def download_and_print(file_url, filename, file_format):
    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            safe_filename = f"{filename.replace('/', '_')}.{file_format}"
            file_path = os.path.join('downloads', safe_filename)
            os.makedirs('downloads', exist_ok=True)

            # ✅ Download with progress
            total_size = int(response.headers.get('content-length', 0))
            with open(file_path, 'wb') as file:
                downloaded_size = 0
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    print(f"\r🔽 Downloading: {downloaded_size / total_size * 100:.2f}%", end='')

            print(f"\n✅ File downloaded: {file_path}")

            # ✅ Print File
            print_file(file_path, filename)

            # ✅ Delete the file after printing (optional)
            os.remove(file_path)
            print("🗑️ File deleted after printing.")
        else:
            print(f"❌ Failed to download {filename} | Status Code: {response.status_code}")
    except Exception as e:
        print("❌ Error during download or print:")
        traceback.print_exc()

def print_file(file_path, filename):
    try:
        print("🖨️ Sending to printer...")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # ✅ Check Microsoft Word Path
        word_path = r"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        if not os.path.isfile(word_path):
            raise FileNotFoundError("Microsoft Word executable not found. Check installation path.")

        # ✅ Print using Microsoft Word
        subprocess.run([word_path, "/mFilePrintDefault", file_path], check=True)
        print(f"✅ Printing initiated for: {file_path}")

        # ✅ Update order status to completed
        update_order_status(filename)

    except FileNotFoundError as e:
        print("❌ File Error:", e)
    except subprocess.CalledProcessError as e:
        print("❌ Error during printing:", e)
        traceback.print_exc()

def update_order_status(filename):
    try:
        print(f"🔔 Updating order status to 'completed' for {filename}")
        response = requests.post(API_URL, json={"file_id": filename, "status": "completed"})
        if response.status_code == 200:
            print("✅ Order status updated successfully.")
        else:
            print(f"❌ Failed to update order status. Status Code: {response.status_code}")
    except Exception as e:
        print("❌ Error updating order status:")
        traceback.print_exc()

def main():
    print("🚀 Store Service Started")
    while True:
        fetch_orders_from_cloudinary()
        print("⏳ Waiting for new orders...")
        time.sleep(30)

if __name__ == "__main__":
    main()
