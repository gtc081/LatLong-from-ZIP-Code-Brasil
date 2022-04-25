import csv
from geopy.geocoders import Nominatim
import requests
import json

f = open("ceps.csv",'r')
csvreader = csv.reader(f)
rows = []
for row in csvreader:
        rows.append(row)
rows

valid = []
cep_invalid = []
url = "https://buscacepinter.correios.com.br/app/endereco/carrega-cep-endereco.php"

form_data = {
    'pagina': "/app/endereco/index.php",
    'cepaux': None,
    'mensagem_alerta': None,
    'endereco': None,
    'tipoCEP': 'LOG'
}

# print(rows)
# exit()
a = 0

for i in rows[1:]:
    try:
        form_data["endereco"] = str(i[0])
        response = requests.post(url, data=form_data)
        resposta_dados = json.loads(response.content)

        endereco={}
        foi = 0
        for j in resposta_dados['dados']:
            if j['cep'][:5] == str(i[0]):
                n = j['logradouroDNEC'].find(' - ')
                if (n != -1):
                    end = j['logradouroDNEC'][:n]
                else:
                    end = j['logradouroDNEC']
                endereco['logradouro'] = end
                endereco['cidade'] = j['localidade']
                endereco['bairro'] = j['bairro']

                # print(endereco)
                geolocator = Nominatim(user_agent="test_app")
                location = geolocator.geocode(endereco['logradouro'] + ", " + endereco['cidade'] + " - " + endereco['bairro'])
                # print([location.latitude,location.longitude])
                # exit()

                if location:
                    # print([location.latitude,location.longitude])
                    valid.append([str(i[0]),endereco['logradouro'],location.latitude,location.longitude])
                    foi = 1
                    break
        
        if foi == 0:
            if endereco == {}:
                cep_invalid.append([str(i[0]),None])
            else:
                cep_invalid.append([str(i[0]),endereco['logradouro']])
    except:
        # print("invalid")
        if endereco == {}:
            cep_invalid.append([str(i[0]),None])
        else:
            cep_invalid.append([str(i[0]),endereco['logradouro']])

print(len(rows[1:]))
with open("out_validos.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(valid)
with open("out_invalidos.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(cep_invalid)

print("ceps validos" + str(len(valid)))
print("ceps invalidos" + str(len(cep_invalid)))

