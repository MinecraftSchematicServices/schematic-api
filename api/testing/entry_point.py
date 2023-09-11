


@register_arg({
    "a": {"bonjour":1}
})
def a(**kwargs):
    print(kwargs)



def main():

    a(bonjour=1)




if __name__ == '__main__':
    main()