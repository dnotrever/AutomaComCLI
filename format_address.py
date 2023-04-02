def format_address(block, apt, condominium, complement):
    if block != '0':
        if len(block) == 1:
            return f'{condominium} - Bloco 0{block} - Apto {apt}'
        else:
            return f'{condominium} - Bloco {block} - Apto {apt}'
    elif complement != '0':
        return f'{condominium} - {complement.title()}'
    else:
        return condominium