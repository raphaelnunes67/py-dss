if __name__ == '__main__':
    values = ''
    for i in range(60 * 4):
        with open('../dss/networks_article/dados_ve.txt', 'a') as file:
            file.write('1\n')

    for i in range(60 * 15):
        with open('../dss/networks_article/dados_ve.txt', 'a') as file:
            file.write('0\n')

    for i in range(60 * 5):
        with open('../dss/networks_article/dados_ve.txt', 'a') as file:
            file.write('1\n')
