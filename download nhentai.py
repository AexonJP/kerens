try:
    import requests
    import re
    import os
    from PIL import Image as ubah
    from tkinter import *
    from bs4 import BeautifulSoup
    from time import sleep
    from playwright.sync_api import sync_playwright
    from cf_clearance import sync_cf_retry, sync_stealth
    from playsound import playsound
    import threading


except:
    tempats=''
    for i in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
        tempats = tempats+i+'/'
    with open(tempats+'requerments.txt', "w") as f:
        f.write("beautifulsoup4\nrequests\nPillow\ntk\ncf-clearance\npytest-playwright"
                )
    tempats=''
    for i in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
        tempats = tempats+i+'\\'
    print(f"copas ini ke terminal ( pip install -r {tempats}requerments.txt ) setelah itu ( playwright install )")
    exit()

def notif():
    suara=''
    for iv in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
        suara = suara+iv+'/'
    try:
        playsound(suara+"sound1.mp3")
    except:
        pass
    
    
def done():
    suara=''
    for iv in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
        suara = suara+iv+'/'
    try:
        playsound(suara+"sound2.mp3")
    except:
        pass

def hapusError(s):

    t = ""
    for i in s:
         
        # Store only valid characters
        if (i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z') or (i ==' '):
            t += i
    return t

def cookies(address, kode, tempat):
    try:
        headers = eval(open(tempat+'headers.txt', 'r').read())
        cookies = eval(open(tempat+'cookie.txt', 'r').read())
        fps = requests.get(f"https://nhentai.net/g/{kode}/", headers=headers, cookies=cookies)
        html = fps.text
        soup = BeautifulSoup(html, 'html.parser')
        oks = str(soup.find(itemprop="image"))
        oks = oks.split("/")
        
        oks = str(soup.find(itemprop="image"))
        oks = oks.split("/")
        server=  (oks[2][1])
        
        obes = str(soup.get_text())
        obes = obes.split('»')
        nama = obes[0]
        
        
        path = (oks[4])
        
        soup = BeautifulSoup(html, 'html.parser')
        obes = str(soup.get_text())
        obes = obes.split(':')
        okll = 6
        while(okll < 20):
            try:
                isi =  int((obes[okll].replace('\t','')).split('\n')[1])
                break
            except:
                okll+=1
        
        return [nama, server, path, isi, headers]
    except:
        isix = "cf_clearance"
        res = requests.get(address)
        if '<title>Please Wait... | Cloudflare</title>' in res.text:
            print("cf challenge fail")
        # get cf_clearance
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False,
                                        # proxy={"server": "http://"+ol}
                                        )
            page = browser.new_page()
            sync_stealth(page, pure=True)
            page.goto(address)

            res = sync_cf_retry(page)
            if res:
                cookies = page.context.cookies()
                for cookie in cookies:
                    if cookie.get('name') == 'cf_clearance':
                        cf_clearance_value = cookie.get('value')
                        isix = 'cf_clearance'
                        
                    elif cookie.get('name') == 'csrftoken':
                        cf_clearance_value = cookie.get('value')
                        isix = 'csrftoken'

                ua = page.evaluate('() => {return navigator.userAgent}')
            else:
                print("cf challenge fail")
            browser.close()
        # use cf_clearance, must be same IP and UA
        headers = {"user-agent": ua}
        with open(tempat+'headers.txt', 'w') as f:
            f.write(str(headers))
        
        cookies = {isix: cf_clearance_value}
        with open(tempat+'cookie.txt', 'w') as f:
            f.write(str(cookies))
        res = requests.post(address,
                        #    proxies=proxies,
                        headers=headers, cookies=cookies)
        if '<title>Please Wait... | Cloudflare</title>' not in res.text:
            fps = requests.get(f"https://nhentai.net/g/{kode}/", headers=headers, cookies=cookies)
        html = fps.text
        soup = BeautifulSoup(html, 'html.parser')
        oks = str(soup.find(itemprop="image"))
        oks = oks.split("/")
        
        oks = str(soup.find(itemprop="image"))
        oks = oks.split("/")
        server=  (oks[2][1])
        
        obes = str(soup.get_text())
        obes = obes.split('»')
        nama = obes[0]
        
        
        path = (oks[4])
        
        soup = BeautifulSoup(html, 'html.parser')
        obes = str(soup.get_text())
        obes = obes.split(':')
        okll = 6
        while(okll < 20):
            try:
                isi =  int((obes[okll].replace('\t','')).split('\n')[1])
                break
            except:
                okll+=1
        
        return [nama, server, path, isi, headers]
        
    


def download_image(nama_folder, url, file_name, headers):

    try:
        # Send GET request
        response = requests.get(url, headers=headers)

        # Save the image
        if response.status_code == 200:
            with open(nama_folder+file_name, "wb") as f:
                f.write(response.content)
            return 1
        else:
            url = url[0:len(url)-3] + "jpg"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                with open(nama_folder+file_name, "wb") as f:
                    f.write(response.content)
                
                img = ubah.open(nama_folder+file_name)
                img.save(nama_folder+file_name)
                return 2
            else:
                print("gangguan dengan kode "+response.status_code)
                return 0
    except:
        print("sudah selesai atau ada kesalahan pada path atau vpn anda")
        return 0

def jadi_gambar(tempat, berapa):
    gambars =[]
    for i in range(berapa):
        img = ubah.open(f"{tempat}{i+2}.png")
        gambars.append(img.convert("RGB"))
    return gambars

def mulai(nama_gambar, folders, url_database, berapa, nama_manga, headers):
    

    if folders != "" :
        nama_folder = folders+"/"+nama_gambar+"/"
        try:
            
            os.mkdir(nama_folder)
        except:
            t = threading.Thread(target=notif)
            t.start()
            okse = input("folder dengan nama tersebut sudah ada ingin berhenti (y) :")
            if okse.upper == 'Y':
                exit()
    else : 
        nama_folder = ""
    try:
        print(f"anda akan mendownload sebanyak {berapa} halaman")
        i=0
        # Download image
        for i in range(berapa):
            i+=1
            file_name = f"{nama_gambar}{i}.png"
            persen = ((i-1)/berapa)*100
            print(f"\rgambar berhasil di download {i-1}/{berapa} ({persen:.2f}%)...",end="")
            url = f"{url_database}{i}.png"
            coba = (download_image(nama_folder, url, file_name, headers))
            if coba == 0 :
                break
            # print(f"selesai mendownload gambar ke {i}")
            # print(f"gambar sedang di download {i}/{berapa} ({(i/berapa)*100}%)...")
            sleep(0.2)
                
        
        if i == berapa:
            persen = ((i)/berapa)*100
            print(f"\rgambar berhasil di download {i}/{berapa} ({persen:.2f}%) Done!")
            print("sedang mencoba memngconvert jadi pdf")
            barang = ubah.open(nama_folder+nama_gambar+"1.png")
            barang = barang.convert('RGB')
            barang.save(nama_folder+hapusError(nama_manga)+ '.pdf',save_all=True, append_images=jadi_gambar(nama_folder+nama_gambar, berapa-1))
            
            t = threading.Thread(target=notif)
            t.start()

            print("sudah selesai membuat pdf")
            if (input("apakah anda ingin menghapus semua gambar (y) : ")).upper() == "Y":
                for jalan in range(i):
                    os.remove(f"{nama_folder}{nama_gambar}{jalan+1}.png")
                print("semua gambar telah di hapus")
                
                t = threading.Thread(target=done)
                t.start()
        else:
            print("download belum selesai")
    except:
        print("masukin angka bgst")
        
    






os.system("cls")
# image file name
kode_nuklir = input("masukkan kode nuklir : ")
# image file folder

folders=''
for i in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
    folders = folders+i+'/'

nama_manga, servers, paths, semua, headers  = cookies('https://nhentai.net', kode_nuklir, folders)
# URL of an image
path =f"/galleries/{paths}/"
url_database = f"https://i{servers}.nhentai.net"+path
nama_manga = nama_manga.replace('\n', '')
nama_manga = nama_manga[0:len(nama_manga)-1]
print(f'\n\nmanga yang akan di download berjudul \n"{nama_manga}"\n')
mulai(kode_nuklir, folders, url_database, int(semua), nama_manga, headers)