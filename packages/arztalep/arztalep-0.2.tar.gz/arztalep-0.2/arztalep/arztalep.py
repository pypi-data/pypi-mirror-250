#epias sitesinden 24 saatlik arz talep cekme
#gerekli kutuphaneler
import requests
import json
import datetime
import pandas as pd
import numpy as np

def arztalep():
    url_arztalep = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/supply-demand"


    #arztalep icin default tarih
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=0)
    # Saat dilimi ofsetini oluştur
    offset = datetime.timezone(datetime.timedelta(hours=3))


    # Boş bir DataFrame oluştur
    all_arztalep = pd.DataFrame()

    # Saat saat artan bir döngü
    #her saat arztalebi cekmek icin
    for hour in range(24):
        # Tarihi ve saati güncelle
        current_datetime = datetime.datetime.combine(tomorrow, datetime.time(hour, 0)).replace(tzinfo=offset)
        
        # formatted_datetime'u oluştur
        formatted_datetime = current_datetime.isoformat()
    
        # JSON oluştur
        payload = json.dumps({
            "date": formatted_datetime
        })

        # İsteği gönder
        response = requests.post(url_arztalep, data=payload, headers={'Content-Type': 'application/json'})

        # Yanıtı DataFrame'e çevir
        data = json.loads(response.text)

        # "items" dizisine ulaşın
        items_list = data.get('items', [])

        # Liste elemanlarını DataFrame'e çevirin
        df = pd.DataFrame(items_list)
        
        df= df.drop(columns=['date'])
        df = df[['price', 'demand', 'supply']]
        df= df.reset_index(drop=True )
        
        all_arztalep = pd.concat([all_arztalep, df], axis=1)
    #arz degerlerini negatif turden pozitife cevirme
    all_arztalep["supply"]= all_arztalep["supply"]* -1
    #nan gelen yerleri bosluga cevirme
    all_arztalep = all_arztalep.fillna("")

    #sutun isimlerini degistirme
    all_arztalep = all_arztalep.rename(columns={
        'price': 'Fiyat',
        'supply': 'Arz',
        'demand': 'Talep',
    })
    # DataFrame'i kaydet
    path = "Arz_Talep.xlsx"

    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')

    sayfa_adi = str(tomorrow) + " arz talebi"
    all_arztalep.to_excel(writer,sheet_name = sayfa_adi)
    return writer.save()