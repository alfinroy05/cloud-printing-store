import os
import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from printer import print_file
import config
import time

def fetch_orders():
    try:
        headers = {'Authorization': f'Bearer {config.ADMIN_TOKEN}'}
        response = requests.get(config.FETCH_ORDERS_URL, headers=headers)

        if response.status_code == 200:
            print("✅ Orders fetched successfully.")
            return response.json()
        else:
            print(f"❌ Failed to fetch orders: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error while fetching orders: {e}")
        return []

def get_decryption_key(order_id):
    try:
        headers = {'Authorization': f'Bearer {config.ADMIN_TOKEN}'}
        response = requests.post(config.FETCH_DECRYPTION_KEY_URL, json={'order_id': order_id}, headers=headers)

        if response.status_code == 200:
            print("✅ Decryption key fetched successfully.")
            return response.json().get('aes_key'), response.json().get('iv')
        else:
            print(f"❌ Failed to fetch decryption key: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Error while fetching decryption key: {e}")
        return None, None

def decrypt_file(file_path, key, iv):
    try:
        key = base64.b64decode(key)
        iv = base64.b64decode(iv)

        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        # Perform AES decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)

        decrypted_file_path = file_path.replace("encrypted_", "decrypted_")
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"✅ File decrypted successfully: {decrypted_file_path}")
        return decrypted_file_path
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        return None

def update_order_status(order_id):
    try:
        headers = {'Authorization': f'Bearer {config.ADMIN_TOKEN}'}
        response = requests.post(config.UPDATE_STATUS_URL, json={'order_id': order_id, 'status': 'completed'}, headers=headers)

        if response.status_code == 200:
            print(f"✅ Order {order_id} status updated to completed.")
        else:
            print(f"❌ Failed to update order status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error while updating order status: {e}")

def main():
    print("🚀 Store Service Started")
    os.makedirs('downloads', exist_ok=True)

    while True:
        orders = fetch_orders()

        for order in orders:
            if order.get('status') == 'pending':
                print(f"🔎 Processing Order: {order.get('file_name', 'Unknown File')}")

                # Download File
                file_url = order.get('file_url')
                file_path = os.path.join('downloads', order.get('file_name', 'unknown_file'))

                try:
                    response = requests.get(file_url)
                    response.raise_for_status()
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"📥 File downloaded: {file_path}")
                except Exception as e:
                    print(f"❌ Error downloading file: {e}")
                    continue

                # Decrypt File
                aes_key, iv = get_decryption_key(order.get('id'))
                if aes_key and iv:
                    decrypted_file_path = decrypt_file(file_path, aes_key, iv)
                    if decrypted_file_path:
                        print_file(decrypted_file_path)
                        update_order_status(order.get('id'))

        print("⏳ Waiting for new orders...")
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()
