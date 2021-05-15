import requests,json

from requests.api import patch



def parser(name,pr):
    site = f'https://api.rivegauche.ru/rg/v1/newRG/products/search?fields=FULL&currentPage=0&pageSize=24&text={name}&tag=1272867863968984'
    r = requests.get(site)
    js = json.loads(r.text)
    lenght_pages=js['pagination']['totalPages']
    page_size = js['pagination']['pageSize']
    ls = list()
    for i in range(lenght_pages):
        site = f'https://api.rivegauche.ru/rg/v1/newRG/products/search?fields=FULL&currentPage=0&pageSize=24&text={name}&tag=1272867863968984'
        resp = requests.get(site)
        data_json = json.loads(resp.text)
        cont = data_json['results']
        for s in range(page_size-1):
            price = cont[s]['price']['value']
            if price <= pr:
                name_prod = cont[s]['name']
                url_ad ='https://rivegauche.ru' + cont[s]['url']
                try:
                    description = cont[s]['description']
                except KeyError:
                    description = ''
                stock = cont[s]['stock']['stockLevelStatus']
                price_valut = cont[s]['price']['currencyIso']
                image = cont[s]['listingImage']['url']
                image ='https://api.rivegauche.ru'+ image
                ds = name_prod + '\n' +url_ad + '\n'+ str(price)+' '+price_valut+'\n'+stock+'\n'+description
                ds = {'image':image,'body':ds}
                ls.append(ds)
            else:
                continue
    return ls
