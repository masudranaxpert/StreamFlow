"""Test script for bysevepoin.com video access challenge with ECDSA signature."""

import httpcloak
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key_pair():
    """Generate ECDSA P-256 key pair like browser does."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key


def public_key_to_jwk(public_key):
    """Convert public key to JWK format."""
    public_numbers = public_key.public_numbers()
    
    def base64url_encode(value, length):
        b = value.to_bytes(length, 'big')
        return base64.urlsafe_b64encode(b).rstrip(b'=').decode('ascii')
    
    x_bytes = base64url_encode(public_numbers.x, 32)
    y_bytes = base64url_encode(public_numbers.y, 32)
    
    return {
        "alg": "ES256",
        "crv": "P-256",
        "ext": True,
        "key_ops": ["verify"],
        "kty": "EC",
        "x": x_bytes,
        "y": y_bytes
    }


def sign_nonce(private_key, nonce):
    """Sign the nonce using ECDSA."""
    signature = private_key.sign(nonce.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
    r_val, s_val = decode_dss_signature(signature)
    r_bytes = r_val.to_bytes(32, 'big')
    s_bytes = s_val.to_bytes(32, 'big')
    raw_signature = r_bytes + s_bytes
    return base64.urlsafe_b64encode(raw_signature).rstrip(b'=').decode('ascii')


def decrypt_payload(payload_b64, key, iv_b64):
    """Decrypt AES-256-GCM encrypted payload."""
    payload = base64.b64decode(payload_b64)
    iv = base64.b64decode(iv_b64)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(iv, payload, None)


def test_challenge_flow():
    """Test challenge -> attest -> playback flow with real ECDSA signature."""
    
    video_id = "1wf9tyk7vv4n"
    
    # Step 1: Get challenge
    challenge_url = f"https://bysevepoin.com/api/videos/access/challenge"
    challenge_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://bysevepoin.com/d/{video_id}",
        "Origin": "https://bysevepoin.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
    }

    print("Step 1: Calling challenge endpoint...")
    challenge_resp = httpcloak.post(challenge_url, headers=challenge_headers)
    print(f"Challenge Status: {challenge_resp.status_code}")
    challenge_data = challenge_resp.json()

    challenge_id = challenge_data["challenge_id"]
    nonce = challenge_data["nonce"]

    # Generate key pair and sign
    print("\nStep 2: Generating ECDSA key pair and signing nonce...")
    private_key, public_key = generate_key_pair()
    signature = sign_nonce(private_key, nonce)
    public_key_jwk = public_key_to_jwk(public_key)
    
    print(f"Signature: {signature}")

    # Step 3: Attest - minimal payload
    attest_url = "https://bysevepoin.com/api/videos/access/attest"
    attest_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Content-Type": "application/json",
    }

    attest_payload = {
        "challenge_id": challenge_id,
        "nonce": nonce,
        "signature": signature,
        "public_key": public_key_jwk,
    }

    print("\nStep 3: Calling attest endpoint...")
    attest_resp = httpcloak.post(attest_url, headers=attest_headers, json=attest_payload)
    print(f"Attest Status: {attest_resp.status_code}")
    attest_data = attest_resp.json()
    
    token = attest_data["token"]
    viewer_id = attest_data["viewer_id"]
    device_id = attest_data["device_id"]
    confidence = attest_data["confidence"]
    
    print(f"Token: {token}")
    print(f"Viewer ID: {viewer_id}")
    print(f"Device ID: {device_id}")
    print(f"Confidence: {confidence}")

    # Step 4: Get playback
    playback_url = f"https://bysevepoin.com/api/videos/{video_id}/playback"
    playback_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://bysevepoin.com/d/{video_id}",
        "Content-Type": "application/json",
        "Origin": "https://bysevepoin.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "Cookie": f"byse_viewer_id={viewer_id}; byse_device_id={device_id}",
    }

    playback_payload = {
        "fingerprint": {
            "token": token,
            "viewer_id": viewer_id,
            "device_id": device_id,
            "confidence": confidence,
        }
    }

    print("\nStep 4: Calling playback endpoint...")
    playback_resp = httpcloak.post(playback_url, headers=playback_headers, json=playback_payload)
    print(f"Playback Status: {playback_resp.status_code}")
    playback_data = playback_resp.json()

    if "playback" in playback_data:
        pb = playback_data["playback"]
        print("\n=== Playback Response Decoded ===")
        print(f"Algorithm: {pb.get('algorithm')}")
        print(f"Expires at: {pb.get('expires_at')}")
        print(f"Cache status: {playback_data.get('cache_status')}")
        
        # Decrypt payload
        key_parts = pb.get("key_parts", [])
        decrypt_keys = pb.get("decrypt_keys", {})
        payload = pb.get("payload")
        iv = pb.get("iv")
        payload2 = pb.get("payload2")
        iv2 = pb.get("iv2")
        
        print(f"\nKey parts: {key_parts}")
        print(f"Decrypt keys: {decrypt_keys}")
        print(f"IV: {iv}")
        print(f"IV2: {iv2}")
        print(f"Payload length: {len(payload) if payload else 0}")
        print(f"Payload2 length: {len(payload2) if payload2 else 0}")
        
        # Decrypt payload using key_parts
        def b64url_decode(s):
            s += "=" * (-len(s) % 4)
            return base64.urlsafe_b64decode(s)
        
        iv_bytes = b64url_decode(iv)
        kp1 = b64url_decode(key_parts[0])
        kp2 = b64url_decode(key_parts[1])
        key = kp1 + kp2
        payload_data = b64url_decode(payload)
        
        print(f"IV length: {len(iv_bytes)}, Key length: {len(key)}, Payload length: {len(payload_data)}")
        
        aesgcm = AESGCM(key)
        try:
            plaintext = aesgcm.decrypt(iv_bytes, payload_data, None)
            print(f"\n=== Decrypted Payload ===")
            result = plaintext.decode("utf-8")
            print(result)
            
            # Parse and pretty print
            parsed = json.loads(result)
            print(f"\n=== Parsed Response ===")
            print(f"Video URL: {parsed['sources'][0]['url'] if parsed.get('sources') else 'N/A'}")
            print(f"Quality: {parsed['sources'][0]['label'] if parsed.get('sources') else 'N/A'}")
            print(f"Expires: {parsed.get('expires_at')}")
        except Exception as e:
            print(f"Decrypt failed: {e}")
    else:
        print(f"Playback Response: {json.dumps(playback_data, indent=2)}")


if __name__ == "__main__":
    test_challenge_flow()
