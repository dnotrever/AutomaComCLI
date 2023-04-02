import os, pytz, message_colors
from datetime import date, datetime, timedelta
from os import system
system('mode con: cols=125 lines=25')

historic = []

def commandLine():

    tz = pytz.timezone('America/Sao_Paulo')
    sp_time = datetime.now(tz)
    now = sp_time.strftime("%d/%m/%Y %H:%M:%S")
    
    others, success, error, info, reset = message_colors.MessageColors.values()
    
    def messageError(code, param=None):
        messages = {
            1: f'Parâmetro faltando {info}[{param}]{reset}',
            2: 'Commando não reconhecido!',
            3: 'Excesso de parâmetros!'
        }
        message = messages.get(code, 'Código de erro inválido.')
        print(f'\n {others}>> {error}Erro: {message}{reset}')
        return commandLine()

    command = input(f'\n {others}$~{reset} ')
    
    arr_command = command.split()
    
    if len(arr_command) > 0:
        
        if arr_command[0] == '?':
            print(f'\n {others}>>{info} Possíveis parâmetros: emerg | services | hist | clear | exit{reset}')
            
        elif arr_command[0] == 'logins':
            
            if len(arr_command) > 1:
                        
                if arr_command[1] == '?':
                    print(f'\n {others}>>{info} Possíveis parâmetros: param{reset}')
                    commandLine()    

                elif arr_command[1] != '?':
                    
                    op_cod = arr_command[1]
                            
                    if len(arr_command) < 3:

                        try:
                            import logins
                            msg = logins.generate_logins()
                            print(f'\n {others}>> {success}{msg}{reset}')
                            historic.append(''.join(f'{now} - {msg}'))
                            
                            import register_logins as Logins
                            msg = Logins.register_logins(op_cod)
                            print(f'\n {others}>> {success}{msg}{reset}')
                        
                        except Exception as err:
                            print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                            commandLine()
                        
                    else: messageError(3)
                            
                else: messageError(2)
                        
            else: messageError(1)
                
        elif arr_command[0] == 'complet':
            
            if len(arr_command) > 1:
                        
                if arr_command[1] == '?':
                    print(f'\n {others}>>{info} Possíveis parâmetros: param{reset}')
                    commandLine()    

                elif arr_command[1] == '-l':
                    
                    try:
                        import completions
                        msg = completions.register_ending_services()
                        print(f'\n {others}>> {success}{msg}{reset}')
                        historic.append(''.join(f'{now} - {msg}'))
                    
                    except Exception as err:
                        print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                        commandLine()

                elif arr_command[1] != '?' or arr_command[1] != '-l':
                    
                    op_cod = arr_command[1]
                            
                    if len(arr_command) < 3:

                        try:
                            import os_completion as Complet
                            msg = Complet.os_completion(op_cod)
                            print(f'\n {others}>> {success}{msg}{reset}')
                            historic.append(''.join(f'{now} - {msg}'))
                        
                        except Exception as err:
                            print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                            commandLine()
                        
                    else: messageError(3)
                            
                else: messageError(2)
                        
            else: messageError(1)
                
        elif arr_command[0] == 'scheds':
            
            if len(arr_command) > 1:
                        
                if arr_command[1] == '?':
                    print(f'\n {others}>>{info} Possíveis parâmetros: param{reset}')
                    commandLine()    

                elif arr_command[1] == '-l':
                    
                    try:
                        import schedulings
                        msg = schedulings.register_customers_schedulings()
                        print(f'\n {others}>> {success}{msg}{reset}')
                        historic.append(''.join(f'{now} - {msg}'))
                    
                    except Exception as err:
                        print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                        commandLine()

                elif arr_command[1] != '?' or arr_command[1] != '-l':
                    
                    op_cod = arr_command[1]
                            
                    if len(arr_command) < 3:

                        try:
                            import os_scheduling as Scheds
                            msg = Scheds.os_scheduling(op_cod)
                            print(f'\n {others}>> {success}{msg}{reset}')
                            historic.append(''.join(f'{now} - {msg}'))
                        
                        except Exception as err:
                            print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                            commandLine()
                        
                    else: messageError(3)
                            
                else: messageError(2)
                        
            else: messageError(1)
                
        elif arr_command[0] == 'attend':

            param_1 = 'código do atendente para transferir'
            
            if len(arr_command) > 1:
                        
                if arr_command[1] == '?':
                    print(f'\n {others}>>{info} Possíveis parâmetros: {param_1}{reset}')
                    commandLine()    

                elif arr_command[1] in ['RAPH', 'MARC', 'ALEX', 'MAUR', '?']:
                    
                    attendant = arr_command[1]
                            
                    if len(arr_command) < 3:

                        try:
                            import transfer_attendance as Attend
                            msg = Attend.transfer_attendances('0', attendant)
                        
                        except Exception as err:
                            print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                            commandLine()
                        
                    else: messageError(3)
                            
                else: messageError(2)
                        
            else: messageError(1, param_1)
        
        elif arr_command[0] == 'emerg':

            param_1 = 't (visita técnica) | r (retirada de equipamentos)'
            param_2 = 'id do cliente'
            param_3 = 'código do operador'
            
            if len(arr_command) > 1:
                    
                if arr_command[1] == '?':
                    print(f'\n {others}>>{info} Possíveis parâmetros: {param_1}{reset}')
                    commandLine()

                elif arr_command[1] in ['t', 'r', '?']:
                    
                    option = arr_command[1]
                                    
                    if len(arr_command) > 2:
                                
                        if arr_command[2] == '?':
                            print(f'\n {others}>>{info} Possíveis parâmetros: {param_2}{reset}')
                            commandLine()
                                    
                        elif arr_command[2] != '?':
                            
                            customer_id = arr_command[2]
                                    
                            if len(arr_command) > 3:
                                
                                if arr_command[3] == '?':
                                    print(f'\n {others}>>{info} Possíveis parâmetros: {param_3}{reset}')
                                    commandLine()
                                
                                elif arr_command[3] in ['0', '1', '2', '3', '4', '?']:
                                    
                                    op_code = arr_command[3]
                                    
                                    if len(arr_command) < 5:
                                        
                                        try:
                                            import customer_infos as Infos
                                            Infos.customer_infos(op_code, customer_id)
                                            
                                            import emergency
                                            msg = emergency.customer_infos(option)
                                            print(f'\n {others}>> {success}{msg}{reset}')

                                            historic.append(''.join(f'{now} - {msg}'))
                                        
                                        except Exception as err:
                                            print(f'\n {others}>>{error} Ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                                            commandLine()
                                        
                                    else: messageError(3)
                                
                                else: messageError(2)
                                
                            else: messageError(1, param_3)
                                    
                        else: messageError(2)
                                
                    else: messageError(1, param_2)
                                    
                else: messageError(2)

            else: messageError(1, param_1)
        
        elif arr_command[0] == 'services':

            param_1 = 'código do operador'
            
            if len(arr_command) > 1:
                                
                if arr_command[1] == '?':
                    print(f'\n {others}>>{info} Possíveis parâmetros: {param_1}{reset}')
                    commandLine()

                elif arr_command[1] != '?':
                    
                    op_code = arr_command[1]

                    if len(arr_command) < 3:
                            
                        try:
                            tomorrow = (date.today() + timedelta(days=1)).strftime('%d/%m/%Y')

                            import services_infos as Services
                            msg_1 = Services.services_infos(op_code, tomorrow)
                            
                            import services
                            msg_2 = services.services_infos()

                            print(f'\n {others}>> {success}{msg_2} {msg_1}{reset}')

                            historic.append(''.join(f'{now} - {msg_2} {msg_1}'))
                        
                        except Exception as err:
                            print(f'\n {others}>>{error} ocorreu um erro...{reset}\t{info}\n    {err}{reset}')
                            commandLine()
                                
                    else: messageError(2)
                                      
                else: messageError(2)

            else: messageError(1, param_1)

        elif arr_command[0] == 'hist':
            
            if historic:
                print('')
                for log in historic:
                    print(f'     {info}{log}{reset}')
            else:
                print(f'\n {others}>> {info}Não há histórico para exibir.{reset}')
            
        elif arr_command[0] == 'clear':
            os.system('cls')
            commandLine()
            
        elif arr_command[0] == 'exit': return
        
        else: messageError(2)
        
    commandLine()

commandLine()