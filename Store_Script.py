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
            return response.json()
        else:
            print("❌ Failed to fetch orders:", response.json().get('error', 'Unknown error'))
            return []
    except Exception as e:
        print("❌ Error:", str(e))
        return []

def get_decryption_key(order_id):
    try:
        headers = {'Authorization': f'Bearer {config.ADMIN_TOKEN}'}
        response = requests.post(config.FETCH_DECRYPTION_KEY_URL, json={'order_id': order_id}, headers=headers)

        if response.status_code == 200:
            return response.json()['aes_key'], response.json()['iv']
        else:
            print("❌ Failed to fetch decryption key:", response.json().get('error', 'Unknown error'))
            return None, None
    except Exception as e:
        print("❌ Error:", str(e))
        return None, None

def decrypt_file(file_path, key, iv):
    try:
        key = base64.b64decode(key)
        iv = base64.b64decode(iv)

        # Read encrypted file
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        # Perform AES decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)

        # Save decrypted file
        decrypted_file_path = file_path.replace("encrypted_", "decrypted_")
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"✅ File decrypted: {decrypted_file_path}")
        return decrypted_file_path
    except Exception as e:
        print(f"❌ Error while decrypting: {e}")
        return None

def update_order_status(order_id):
    try:
        headers = {'Authorization': f'Bearer {config.ADMIN_TOKEN}'}
        response = requests.post(config.UPDATE_STATUS_URL, json={'order_id': order_id, 'status': 'completed'}, headers=headers)

        if response.status_code == 200:
            print("✅ Order status updated to completed.")
        else:
            print("❌ Failed to update order status:", response.json().get('error', 'Unknown error'))
    except Exception as e:
        print("❌ Error:", str(e))

def main():
    print("🚀 Store Service Started")
    while True:
        orders = fetch_orders()

        for order in orders:
            if order['status'] == 'pending':
                print(f"🔎 Processing Order: {order['file_name']}")

                # Download File
                file_url = order['file_url']
                file_path = f"downloads/{order['file_name']}"

                response = requests.get(file_url)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"📥 File downloaded: {file_path}")

                # Decrypt File
                aes_key, iv = get_decryption_key(order['id'])
                if aes_key and iv:
                    decrypted_file_path = decrypt_file(file_path, aes_key, iv)
                    if decrypted_file_path:
                        print_file(decrypted_file_path)
                        update_order_status(order['id'])

        print("⏳ Waiting for new orders...")
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()
