def costumers_id_list():
    import dataframes, format_address, CONF
    id_list = open('../ID_List.txt', 'w')
    for _, row in dataframes.total_services.iterrows():
        columns = [
            str(row['ID']),
            row['Assunto'],
            row['Cliente'],
            row['Condomínio'],
        ]
        id, subject, name, condominium = columns
        if subject == 'Instalação' and (condominium in CONF.PROV_SYS_H or CONF.PROV_SYS_D):
            id_list.write(f'\n{id} - {condominium} - {name}\n')
    id_list.close()
    return 'Lista de clientes para instalação gerada com sucesso!'

def generate_customer_infos(customer_id):
    from unicodedata import normalize
    import re, dataframes
    for _, row in dataframes.registrations.iterrows():
        columns = [
            str(row['ID']),
            row['Cliente'],
            row['Condomínio'],
            str(row['Bl']),
            str(row['Apto']),
        ]
        id, name, condominium, block, apt = columns
        if id == customer_id:
            format_name = (normalize('NFKD', name).encode('ASCII','ignore').decode('ASCII')).lower()
            arr_name = (format_name.lower()).split(' ')
            short_names = ['de', 'do', 'dos', 'da', 'das', 'e']
            customer_name = []
            for x in range(len(arr_name)):
                if not arr_name[x] in short_names:
                    customer_name.append(arr_name[x])
            block = ''.join(re.findall('[0-9]+', block))
            if len(block) == 1: block = '0' + block
            apt = ''.join(re.findall('[0-9]+', apt))
            infos = f'{customer_name[0]}-{customer_name[1]}-bl{block}-apto{apt}'
            return [name, infos, condominium, block]

def provis_customer_datacom(op, id):

    import telnetlib, time, infra_configs
    import CONF as CONF
    import contract_activation as CONTRACT
    from datetime import date, datetime

    # # - - - - - - - - - - - - - - - - - - - - 
    
    name, infos, condominium, block = generate_customer_infos(id)
    ip_olt = infra_configs.discover_olt(condominium)
    print('\nolt: ' + ip_olt)
    print('cliente: ' + infos)

    # # - - - - - - - - - - - - - - - - - - - - 

    try:
        telnet = telnetlib.Telnet(ip_olt)
    except:
        print('Erro ao se conectar!')
    user = b'erosa\n'
    password = CONF.APP_PASS.encode('ascii') + b'\n'
    telnet.read_until(b': ')
    telnet.write(user)
    telnet.read_until(b': ')
    telnet.write(password)
    telnet.read_until(b'# ')
    telnet.write(b'config\n')

    # # - - - - - - - - - - - - - - - - - - - - 

    print(telnet.read_very_eager())

    telnet.read_until(b'# ')
    telnet.write(b'do show interface gpon discovered-onus\n')
    telnet.read_until(b'\n')
    time.sleep(2)
    onu_infos = telnet.read_very_eager().decode('utf-8').splitlines()
    if '% No entries found.' in onu_infos:
        print('Sem ONU!')
        return
    else:
        onu_mac = onu_infos[3].split()[1]
        print('mac: ' + onu_mac)
        onu_gpon = onu_infos[3].split(' ')[7]
        print('gpon: ' + onu_gpon)
    vlan = infra_configs.discover_vlan(condominium, onu_gpon, block)
    print('vlan: ' + vlan)

    # # - - - - - - - - - - - - - - - - - - - - 

    telnet.write(f'do show running-config interface gpon {onu_gpon} | nomore'.encode('ascii') + b'\n')
    telnet.read_until(b'\n')
    time.sleep(7)
    onus = telnet.read_very_eager().splitlines()
    onus_arr = []
    for onu in onus:
        onu_str = onu.decode('utf-8')
        if 'onu' in onu_str:
            onus_arr.append(onu_str)
    last_onu = str(onus_arr[len(onus_arr)-1])
    curr_onu = int(last_onu.split(' ')[2]) + 1
    print('onu:', curr_onu)

    # # - - - - - - - - - - - - - - - - - - - - 

    telnet.write(f'interface gpon {onu_gpon} onu {curr_onu}'.encode('ascii') + b'\n')
    telnet.read_until(b'\n')
    telnet.write(f'serial-number {onu_mac}'.encode('ascii') + b'\n')
    telnet.read_until(b'# ')
    telnet.write(f'name {infos}'.encode('ascii') + b'\n')
    telnet.read_until(b'# ')
    telnet.write(f'line-profile DEFAULT-LINE\nethernet 1\nnegotiation\nno shutdown\nnative vlan vlan-id {vlan}\nnative vlan cos 0'.encode('ascii') + b'\n')
    telnet.read_until(b'# ')
    telnet.write(b'commit\n')
    time.sleep(3)
    telnet.read_until(b'# ')
    telnet.write(b'top\n')

    # # - - - - - - - - - - - - - - - - - - - - 

    telnet.read_until(b'# ')
    telnet.write(b'do show running-config | include service-port | nomore\n')
    telnet.read_until(b'# ')
    time.sleep(45)
    services = telnet.read_very_eager().splitlines()
    services_arr = []
    for service in services:
        service_str = service.decode('utf-8')
        services_arr.append(service_str)
    last_service = str(services_arr[len(services_arr)-2])
    curr_service = int(last_service.split(' ')[1]) + 1
    print('service port:', curr_service, '\n')

    # # - - - - - - - - - - - - - - - - - - - - 

    telnet.write(f'service-port {curr_service} gpon {onu_gpon} onu {curr_onu} gem 1 match vlan vlan-id {vlan} action vlan replace vlan-id {vlan}'.encode('ascii') + b'\n')
    telnet.read_until(b'# ')
    telnet.write(b'commit\n')
    time.sleep(3)

    # # - - - - - - - - - - - - - - - - - - - - 
    
    today = date.today()
    now_date = str(datetime.now()).split(' ')[1]
    now_time = now_date.split('.')[0]
    provis_logs = open(f'../Provising_Logs_{today}.txt', 'w')
    provis_logs.write(f'\n[{now_time}]\n{name} ({condominium})\n{infos}\nMAC: {onu_mac}\nGPON: {onu_gpon}\nONU: {curr_onu}\nVLAN: {vlan}\nService Port: {curr_service}\n')
    provis_logs.close()

    CONTRACT.contract_activation(op, id, name)

    return f'{name} - provisionamento concluído.'

def provis_customer_huawei(): pass


# print(costumers_id_list())

print(provis_customer_datacom('0', '9310'))

# import telnetlib
# telnet = telnetlib.Telnet('')
# telnet.interact()