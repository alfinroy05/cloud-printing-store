import os
import cloudinary
import cloudinary.api
import requests
import time
import win32api

# ✅ Configure Cloudinary
cloudinary.config(
    cloud_name="dwquzmwam",
    api_key="817587174551443",
    api_secret="7WMCvvjzdjUHY-nSONCd2K4clXw"
)

def fetch_orders_from_cloudinary():
    try:
        print("🔎 Fetching orders from Cloudinary...")

        # ✅ List resources from Cloudinary (e.g., from 'uploads' folder)
        resources = cloudinary.api.resources(
            type="upload",
            prefix="uploads/",
            max_results=10
        )

        if resources.get("resources"):
            print("✅ Files Retrieved Successfully!")
            for resource in resources["resources"]:
                print(f"📄 File: {resource['public_id']} | URL: {resource['secure_url']}")
                download_and_print(resource['secure_url'], resource['public_id'])
        else:
            print("⚠️ No files found in Cloudinary.")
    except Exception as e:
        print("❌ Error while fetching from Cloudinary:", str(e))

def download_and_print(file_url, filename):
    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(file_url)
        if response.status_code == 200:
            file_path = f"downloads/{filename.replace('/', '_')}.pdf"
            os.makedirs('downloads', exist_ok=True)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"✅ File downloaded: {file_path}")

            # ✅ Print File
            print_file(file_path)

            # ✅ Delete the file after printing (optional)
            os.remove(file_path)
            print("🗑️ File deleted after printing.")
        else:
            print(f"❌ Failed to download {filename} | Status Code: {response.status_code}")
    except Exception as e:
        print("❌ Error during download or print:", str(e))

def print_file(file_path):
    try:
        print("🖨️ Sending to printer...")

        # Ensure file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Print using default PDF viewer
        win32api.ShellExecute(0, "print", file_path, None, ".", 0)
        print(f"✅ Printing: {file_path}")
    except FileNotFoundError as e:
        print("❌ File Error:", e)
    except Exception as e:
        print("❌ Error during printing:", str(e))

def main():
    print("🚀 Store Service Started")
    while True:
        fetch_orders_from_cloudinary()
        print("⏳ Waiting for new orders...")
        time.sleep(30)  # ✅ Check every 30 seconds

if __name__ == "__main__":
    main()
