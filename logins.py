def create_prelogins(initial, numerics, name, length):
    c = 0
    while c < length-1:
        initial.append(name[0]+name[c+1])
        for x in range(4):
            numerics.append(name[0]+name[c+1]+str(x+2))
        c += 1

def register_login(name, initial, numerics, existing, user, logins):
    for pre_initial in initial:
        if not pre_initial in existing:
            logins += [[name, pre_initial, user]]
            return
    for pre_numeric in numerics:
        if not pre_numeric in existing:
            logins += [[name, pre_initial, user]]
            return

def generate_logins():

    import pandas as pd
    from unicodedata import normalize
    import dataframes

    logins = []
    cont = 0

    for customer in dataframes.total_services['Cliente'].values:

        if dataframes.total_services.query(f'Cliente == "{customer}"')['Assunto'].values == 'Instalação':

            cont += 1

            format_name = normalize('NFKD', customer).encode('ASCII','ignore').decode('ASCII')
            arr_name = (format_name.lower()).split(' ')

            existing_logins = dataframes.logins['Login'].values

            app_user = ' '.join(dataframes.incomplete_registrations.query(f'Cliente == "{customer}"')['App User'].values)

            initial_prelogins = []
            numeric_prelogins = []

            short_names = ['de', 'do', 'dos', 'da', 'das', 'e']

            customer_name = []

            for x in range(len(arr_name)):
                if not arr_name[x] in short_names:
                    customer_name.append(arr_name[x])
            
            length_name = len(customer_name)
            
            create_prelogins(initial_prelogins, numeric_prelogins, customer_name, length_name)

            register_login(customer, initial_prelogins, numeric_prelogins, existing_logins, app_user, logins)

    df = pd.DataFrame(logins, columns=['Customer', 'Login', 'User'])
    df.to_excel('sheets/new_logins_list.xlsx', index = False, header=True)
    
    return f'{cont} logins gerados'

# print(generate_logins())