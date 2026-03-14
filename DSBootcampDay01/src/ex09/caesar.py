import sys

def caesar_cipher(text, shift, mode="encode"):
    if any(ord(ch) > 127 for ch in text if ch.isalpha()):
        raise Exception("The script does not support your language yet.")
    
    shift = int(shift) if mode == "encode" else -int(shift)
    result = []

    for ch in text:
        if 'A' <= ch <= 'Z':
            new_ch = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        elif 'a' <= ch <= 'z':
            new_ch = chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        else:
            new_ch = ch
        
        result.append(new_ch)

    return "".join(result)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 caesar.py <encode|decode> '<text>' <shift>")
        sys.exit(1)

    mode, text, shift = sys.argv[1], sys.argv[2], sys.argv[3]

    if mode not in ["encode", "decode"]:
        print("Error: <mode> should be 'encode' or 'decode'")
        sys.exit(1)

    try:
        result = caesar_cipher(text, shift, mode)
        print(result)
    except Exception as e:
        print(str(e))
