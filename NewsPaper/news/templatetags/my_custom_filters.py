from django import template

register = template.Library()


@register.filter()
def censor(message: str):
    global string2
    black_list = ['черт', 'сука', 'гнида', 'чмо']
    ln = len(black_list)
    filtred_message = ''
    string = ''
    pattern = '*'
    for i in message:
        string += i
        string2 = string.lower()
        flag = 0
        for j in black_list:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_message += pattern * len(string)
                flag -= 1
                string = ''
        if flag == ln:
            filtred_message += string
            string = ''

    if string2 != '' and string2 not in black_list:
        filtred_message += string
    elif string2 != '':
        filtred_message += pattern * len(string)

    return filtred_message
