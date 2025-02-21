import binascii
from flask import Flask, render_template, request
from aes import pad_to_128_bit, aes_encrypt_message, aes_decrypt_message

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    word_info = []
    round_info = []
    error = ""
    operation = ""
    result = None
    
    if request.method == 'POST':
        operation = request.form.get('operation', 'encrypt')
        # Process key input
        key_mode = request.form.get('key_mode', 'text')
        key_input = request.form.get('key', '')
        if key_mode == 'hex':
            try:
                key_bytes = bytes.fromhex(key_input)
            except ValueError:
                error = "Invalid hex input for key."
                return render_template('index.html', error=error)
            if len(key_bytes) != 16:
                error = "Key in hex must represent exactly 16 bytes (32 hex digits)."
                return render_template('index.html', error=error)
        else:
            key_bytes = key_input.encode()
            if len(key_bytes) != 16:
                error = "Key must be exactly 16 characters long."
                return render_template('index.html', error=error)

        if operation == 'encrypt':
            plaintext_mode = request.form.get('plaintext_mode', 'text')
            plaintext_input = request.form.get('plaintext', '')
            if plaintext_mode == 'hex':
                try:
                    plaintext_bytes = bytes.fromhex(plaintext_input)
                except ValueError:
                    error = "Invalid hex input for plaintext."
                    return render_template('index.html', error=error)
                # Ensure block length is a multiple of 16 bytes
                while len(plaintext_bytes) % 16 != 0:
                    plaintext_bytes += b' '
            else:
                plaintext_bytes = pad_to_128_bit(plaintext_input)
            ciphertext = aes_encrypt_message(plaintext_bytes, key_bytes, word_info, round_info)
            structured_round_info = []
            for block in round_info:
                lines = block.split("\n")
                header = lines[0] if lines else ""
                lines = lines[1:]
                structured_round_info.append({"header": header, "lines": lines})
            result = {
                "ciphertext": binascii.hexlify(ciphertext).decode(),
                "word_info": word_info,
                "round_info": structured_round_info
            }
        elif operation == 'decrypt':
            ciphertext_mode = request.form.get('ciphertext_mode', 'hex')
            ciphertext_input = request.form.get('ciphertext', '')
            if ciphertext_mode == 'hex':
                try:
                    ciphertext_bytes = bytes.fromhex(ciphertext_input)
                except ValueError:
                    error = "Invalid hex input for ciphertext."
                    return render_template('index.html', error=error)
            else:
                error = "For decryption, ciphertext must be provided in hex format."
                return render_template('index.html', error=error)
            
            decrypted = aes_decrypt_message(ciphertext_bytes, key_bytes, word_info, round_info)
            decrypted_mode = request.form.get('decrypted_mode', 'text')
            if decrypted_mode == 'text':
                try:
                    decrypted_output = decrypted.decode('utf-8').rstrip()
                except UnicodeDecodeError:
                    # If decoding fails, use error replacement so that invalid bytes are replaced.
                    decrypted_output = decrypted.decode('utf-8', errors='replace').rstrip()
            elif decrypted_mode == 'hex':
                decrypted_output = binascii.hexlify(decrypted).decode()
            else:
                decrypted_output = decrypted.decode('utf-8', errors='replace').rstrip()

            structured_round_info = []
            for block in round_info:
                lines = block.split("\n")
                header = lines[0] if lines else ""
                lines = lines[1:]
                structured_round_info.append({"header": header, "lines": lines})
            result = {
                "decrypted_text": decrypted_output,
                "word_info": word_info,
                "round_info": structured_round_info
            }
        else:
            error = "Invalid operation selected."

    return render_template('index.html', result=result, error=error, operation=operation)

if __name__ == '__main__':
    app.run(debug=True)
