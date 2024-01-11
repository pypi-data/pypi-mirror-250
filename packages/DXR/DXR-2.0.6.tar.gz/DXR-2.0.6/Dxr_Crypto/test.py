from dxr_crypto import Dxr_Crypto

dxr_tsdk = Dxr_Crypto()

while True:
    input_str = input("请输入要加密的字符串：")
    e_data, e_len = dxr_tsdk.encrypt(input_str)
    d_str, d_len = dxr_tsdk.decrypt(e_data, e_len)
    print(f'加密前的字符串：{input_str}, 加密后的字符串：{e_data}, 解密后的字符串：{d_str}')
    print(f"加密前和解密后的字符串是否相等：{input_str == d_str}")
    if input_str == "exit":
        break