import os
import cloudinary
import cloudinary.api
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

ALLOWED_FORMATS = {"pdf", "jpg", "jpeg", "png", "doc", "docx"}
API_URL = "http://localhost:8000/api/update_order_status/"
LAST_FILE_TRACKER = "last_file.txt"  # File to track last processed file

# ✅ Persistent last processed file
def get_last_processed_file():
    if os.path.exists(LAST_FILE_TRACKER):
        with open(LAST_FILE_TRACKER, "r") as f:
            return f.read().strip()
    return None

def save_last_processed_file(file_id):
    with open(LAST_FILE_TRACKER, "w") as f:
        f.write(file_id)

def fetch_orders_from_cloudinary():
    try:
        print("🔎 Fetching recent orders from Cloudinary...")
        resources = cloudinary.api.resources(type="upload", max_results=10, sort_by={"created_at": "desc"})

        if not resources.get("resources"):
            print("⚠️ No files found in Cloudinary.")
            return

        print("📂 Retrieved Files:")
        for file in resources["resources"]:
            print(f" - {file['public_id']} ({file['format']})")

        # ✅ Filter files with "uploads/" prefix
        recent_file = next((f for f in resources["resources"] if f["public_id"].startswith("uploads/")), None)

        if not recent_file:
            print("⚠️ No files found in 'uploads/' folder.")
            return

        last_processed_file = get_last_processed_file()
        if recent_file['public_id'] == last_processed_file:
            print("⚠️ No new files found. Waiting for new uploads.")
            return

        save_last_processed_file(recent_file['public_id'])

        file_format = recent_file['format'].lower()
        if file_format not in ALLOWED_FORMATS:
            print(f"⚠️ Unsupported file format: {file_format}, skipping.")
            return

        file_url = recent_file['secure_url']
        print(f"📄 Recent File: {recent_file['public_id']} | URL: {file_url}")
        download_and_print(file_url, recent_file['public_id'], file_format)
    except Exception:
        print("❌ Error while fetching from Cloudinary:")
        traceback.print_exc()

def download_and_print(file_url, filename, file_format):
    try:
        print(f"📥 Downloading {filename}...")
        file_path = os.path.join("downloads", f"{filename}.{file_format}")
        os.makedirs("downloads", exist_ok=True)

        for attempt in range(3):
            try:
                response = requests.get(file_url, stream=True, timeout=10)
                if response.status_code == 200:
                    with open(file_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"✅ File downloaded: {file_path}")
                    break
                print(f"⚠️ Attempt {attempt + 1}: Failed to download. Retrying...")
            except requests.exceptions.RequestException:
                print("❌ Network Error. Retrying...")
        else:
            print("❌ Max retries reached. Skipping file.")
            return

        # ✅ Print File
        print_file(file_path, filename)

        # ✅ Delete after printing
        os.remove(file_path)
        print("🗑️ File deleted after printing.")

    except Exception:
        print("❌ Error during download or print:")
        traceback.print_exc()

def print_file(file_path, filename):
    try:
        print("🖨️ Sending to printer...")

        file_extension = filename.split('.')[-1].lower()

        if file_extension == "pdf":
            print("📄 Printing PDF using SumatraPDF...")
            sumatra_path = r"C:\Program Files\SumatraPDF\SumatraPDF.exe"
            if not os.path.exists(sumatra_path):
                raise FileNotFoundError("SumatraPDF not found. Install it for faster PDF printing.")
            subprocess.run([sumatra_path, "-print-to-default", file_path], check=True)

        elif file_extension in ["jpg", "jpeg", "png"]:
            print("🖼️ Printing Image using MSPaint...")
            subprocess.run(["mspaint", "/p", file_path], check=True)

        elif file_extension in ["doc", "docx"]:
            print("📑 Printing Word Document...")
            word_path = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
            if not os.path.exists(word_path):
                raise FileNotFoundError("Microsoft Word not found. Check installation path.")
            subprocess.run([word_path, "/mFilePrintDefault", file_path], check=True)

        else:
            print(f"❌ Unsupported file format: {file_extension}")
            return

        print(f"✅ Printing initiated for: {file_path}")
        update_order_status(filename)

    except FileNotFoundError as e:
        print("❌ File Error:", e)
    except subprocess.CalledProcessError:
        print("❌ Error during printing:")
        traceback.print_exc()

def update_order_status(filename):
    try:
        print(f"🔔 Updating order status to 'completed' for {filename}")
        response = requests.post(API_URL, json={"file_id": filename, "status": "completed"})
        
        print(f"📝 Response: {response.text}")  # Log the response
        
        if response.status_code == 200:
            print("✅ Order status updated successfully.")
        else:
            print(f"❌ Failed to update order status. Status Code: {response.status_code}")
    except Exception:
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
