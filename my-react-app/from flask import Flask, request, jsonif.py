from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/setup_mfa', methods=['POST'])
def setup_mfa():
    username = request.json['username']
    
    # Run Google Authenticator setup for the user
    process = subprocess.Popen(['google-authenticator', '-t', '-d', '-f', '-r', '3', '-R', '30', '-w', '3'],
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output, error = process.communicate(input=b'y\ny\ny\ny\n')
    
    if process.returncode == 0:
        # Extract the QR code URL from the output
        qr_code_url = [line for line in output.decode().split('\n') if 'https://' in line][0]
        return jsonify({'success': True, 'qr_code_url': qr_code_url})
    else:
        return jsonify({'success': False, 'error': error.decode()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)