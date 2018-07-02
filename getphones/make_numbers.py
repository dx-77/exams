#!/usr/bin/env python3
import random

NUM = 50000
if __name__ == '__main__':
    phones = []
    for i in range(89011231111, 89011231111 + NUM):
        phones.append(str(i))
    print ('Phones created')
    print('Creating *.htm')
    n = random.randrange(NUM //2, NUM)
    ind = list(set([random.randrange(NUM) for i in range(n)]))

    with open('phones.htm', 'w') as f:
        f.write(
            '<html lang="ru"><head><meta http-equiv="Content-Type"'
            ' content="text/html; charset=UTF-8"></head>\n<body>\n'
            '<p>NUMBER OF PHONES == __%d__\n\n</p><div class="tel"><table>\n<tr>\n' % len(ind)
        )
        
        count = 1 
       
        for i in ind:
                     
            if not count % 10:
                f.write('<tr>')

            f.write('<td>%s</td>' % phones[i])

            if not count % 10:
                f.write('</tr>')
            count +=1
                                 
        f.write('\n</tr>\n</table>\n</div></body>\n</html>')