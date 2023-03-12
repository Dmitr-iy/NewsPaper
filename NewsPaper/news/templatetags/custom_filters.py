from django import template

register = template.Library()

bad_words = ['idiot', 'stupid', 'Fool', 'Cattle']

@register.filter(name='censor')
def censor(value):

    sent = value.split()
    for i in bad_words:
        for words in sent:
            if i in words:
                pos = sent.index(words)
                sent.remove(words)
                sent.insert(pos, '*' * len(i))
    return " ".join(sent)