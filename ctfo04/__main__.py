import os
import requests
import argparse
import zipfile
import pathlib


dest = pathlib.Path('ctfo04-challanges')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ctfid', type=str)
    args = parser.parse_args()

    response = requests.get(f'https://ctf.mintux.de/api/getFlag.php?id={args.ctfid}').json()

    if not response['success']:
        print('Error:', response['msg'])
        return
    
    flag = response["args"]["flag"]
    print('Flag:', flag)
    
    
    response = requests.get(f'https://ctf.mintux.de/api/getChallenge.php?id={args.ctfid}').raw
    
    with open(f'{args.ctfid}.zip', 'wb') as f:
        f.write(response.read())
        
    with zipfile.ZipFile(f'{args.ctfid}.zip', 'r') as zip_ref:
        zip_ref.extractall(dest)
        
    print('Challenge extracted to:', dest)
    
    dockerfile = (dest / 'Dockerfile').read_text()
    (dest / 'Dockerfile').write_text(dockerfile.replace('{PLACEHOLDER}', flag))
    
    os.system(f'docker build -t {args.ctfid} {dest}')
    os.system(f'docker run --rm {args.ctfid}')

    # dest.mkdir(parents=True, exist_ok=True)
    # zip_path = dest / f'{args.ctfid}.zip'
    # zip_path.write_bytes(requests.get(zip_url).content)

    # with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    #     zip_ref.extractall(dest)

    # print('Challenge extracted to:', dest)

    
if __name__ == '__main__':
    main()
