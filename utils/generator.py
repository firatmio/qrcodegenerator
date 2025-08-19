import qrcode, secrets, string, os

def generator(data, front_color, back_color, border):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=front_color, back_color=back_color)
    img_file_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)) + ".png"
    downloads_path = os.path.expanduser("~/Downloads")
    img_file_path = os.path.join(downloads_path, img_file_name)
    img.save(img_file_path)
    return img, img_file_path