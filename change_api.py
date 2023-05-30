from settings import token, captcha_service
import os
import shutil


def update_api_key():
    apies = ['rehalka', 'rucaptcha']
    js_file_path = os.path.join(fr'{apies[captcha_service-1]}\common', 'config.js')
    with open(js_file_path, 'r') as file:
        content = file.read()
    updated_content = content.replace('apiKey: null', f'apiKey: "{token}"')
    with open(js_file_path, 'w') as file:
        file.write(updated_content)
    shutil.make_archive(f'{apies[captcha_service-1]}_api.crx', 'zip', apies[captcha_service-1])
    new_crx_file_path = f'{apies[captcha_service-1]}_api.crx'.replace('.zip', '.crx')
    if os.path.exists(new_crx_file_path):
        os.remove(new_crx_file_path)
    os.rename(f'{apies[captcha_service-1]}_api.crx' + '.zip', new_crx_file_path)
    updated_content = content.replace(f'apiKey: "{token}"', 'apiKey: null')
    with open(js_file_path, 'w') as file:
        file.write(updated_content)


update_api_key()
