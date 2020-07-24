import math
gaussRssi = [[-54 ,-54 ,-54 ,-55 ,-54 ,-56 ,-54 ,-54 ,-54 ,-55 ,-55 ,-54 ,-54 ,-54 ,-54 ,-56 ,-54 ,-54 ,-55 ,-55 ,-55 ,-55 ,-55 ,-55 ,-55 ,-54 ,-56 ,-55 ,-54 ,-57 ],
[-66 ,-67 ,-66 ,-66 ,-67 ,-65 ,-65 ,-66 ,-66 ,-66 ,],
[-62 ,-62 ,-62 ,-61 ,-61 ,-61 ,-61 ,-62 ,-62 ,-61 ,],
[-62 ,-63 ,-62 ,-63 ,-62 ,-62 ,-63 ,-62 ,-63 ,-61 ,],
[-66 ,-66 ,-66 ,-67 ,-65 ,-66 ,-66 ,-67 ,-66 ,-65],
[-66 ,-66 ,-65 ,-66 ,-66 ,-66 ,-66 ,-67 ,-66 ,-67],
[-65 ,-66 ,-66 ,-66 ,-66 ,-67 ,-65 ,-65 ,-66 ,-66],
[-66 ,-66 ,-66 ,-67 ,-66 ,-68 ,-67 ,-66 ,-67 ,-65],
[-65 ,-65 ,-64 ,-67 ,-65 ,-66 ,-66 ,-65 ,-66 ,-65],
[-71 ,-72 ,-72 ,-72 ,-71 ,-72 ,-72 ,-73 ,-72 ,-71],
[-76 ,-74 ,-73 ,-74 ,-75 ,-76 ,-75 ,-75 ,-75 ,-75],
[-78 ,-77 ,-76 ,-76 ,-77 ,-76 ,-77 ,-76 ,-75 ,-77],
[-81 ,-80 ,-81 ,-80 ,-81 ,-81 ,-81 ,-81 ,-79 ,-80],
[-78 ,-79 ,-80 ,-79 ,-80 ,-80 ,-80 ,-80 ,-82 ,-80],
[-78 ,-79 ,-79 ,-80 ,-80 ,-79 ,-81 ,-79 ,-78 ,-80],
[-78 ,-78 ,-76 ,-78 ,-78 ,-77 ,-77 ,-78 ,-77 ,-78],
[-76 ,-77 ,-76 ,-76 ,-77 ,-76 ,-77 ,-77 ,-75 ,-77],
[-77 ,-77 ,-77 ,-78 ,-77 ,-78 ,-76 ,-76 ,-78 ,-78],
[-79 ,-78 ,-78 ,-78 ,-78 ,-79 ,-79 ,-79 ,-86 ,-79],
[-76 ,-75 ,-75 ,-76 ,-75 ,-75 ,-74 ,-75 ,-75 ,-75],
[-80 ,-80 ,-81 ,-80 ,-80 ,-82 ,-82 ,-82 ,-80 ,-81],
[-78 ,-79 ,-78 ,-78 ,-79 ,-78 ,-79 ,-79 ,-78 ,-79],
[-86 ,-84 ,-88 ,-88 ,-87 ,-87 ,-86 ,-84 ,-86 ,-81],
[-82 ,-83 ,-83 ,-85 ,-84 ,-84 ,-82 ,-84 ,-83 ,-82],
[-80 ,-81 ,-80 ,-80 ,-80 ,-80 ,-80 ,-86 ,-85 ,-88],
[-85 ,-85 ,-87 ,-87 ,-87 ,-85 ,-86 ,-86 ,-85 ,-87],
[-80 ,-80 ,-81 ,-80 ,-81 ,-81 ,-80 ,-80 ,-80 ,-79],
[-82 ,-81 ,-81 ,-82 ,-81 ,-81 ,-82 ,-82 ,-81 ,-82],
[-80 ,-79 ,-82 ,-81 ,-81 ,-82 ,-82 ,-82 ,-83 ,-83],
[-84 ,-84 ,-85 ,-84 ,-86 ,-83 ,-85 ,-85 ,-84 ,-82],
[-84 ,-87 ,-83 ,-84 ,-85 ,-86 ,-84 ,-86 ,-83 ,-83],
[-83 ,-85 ,-84 ,-82 ,-85 ,-79 ,-85 ,-83 ,-85 ,-86]]
sumRSS = []
yRSS = []
oRSS = []
RSS = []
RSSfinal = []

for x in range(len(gaussRssi)):
    if len(sumRSS) < len(gaussRssi):
        sumRSS.append(0)
        yRSS.append(0)
    for y in range(len(gaussRssi[x])):
        if sumRSS[x] == 0:
            sumRSS[x] = gaussRssi[x][y]
        else:
            sumRSS[x] = sumRSS[x] + gaussRssi[x][y]
    yRSS[x] = sumRSS[x]/len(gaussRssi[x])

for x in range(len(gaussRssi)):
    if len(oRSS) < len(gaussRssi):
        oRSS.append(0)
    for y in range(len(gaussRssi[x])):
        if oRSS[x] == 0:
            oRSS[x] = (gaussRssi[x][y]-yRSS[x])*(gaussRssi[x][y]-yRSS[x])
        else:
            oRSS[x] = oRSS[x]+(gaussRssi[x][y]-yRSS[x]) * \
                (gaussRssi[x][y]-yRSS[x])
    if len(gaussRssi[x]) != 1:
        oRSS[x] = math.sqrt(oRSS[x]/(len(gaussRssi[x])-1))

for x in range(len(gaussRssi)):
    if len(RSS) < len(gaussRssi):
        RSS.append([0])
    for y in range(len(gaussRssi[x])):
        if gaussRssi[x][y] > yRSS[x]-oRSS[x] and gaussRssi[x][y] < yRSS[x]+oRSS[x]:
            if RSS[x][0] == 0:
                RSS[x][0] = gaussRssi[x][y]
            else:
                c = False
                for k in range(len(RSS[x])):
                    if RSS[x][k] == gaussRssi[x][y]:
                        c = True
                        break
                if c == False:
                    RSS[x].append(gaussRssi[x][y])
for x in range(len(RSS)):
    if len(RSSfinal) < len(RSS):
        RSSfinal.append(0)
    for y in range(len(RSS[x])):
        if RSSfinal[x] == 0:
            RSSfinal[x] = RSS[x][y]
        else:
            RSSfinal[x] = RSSfinal[x] + RSS[x][y]
    RSSfinal[x] = RSSfinal[x]/len(RSS[x])

for x in range(len(gaussRssi)):
    if oRSS[x] == 0 or len(gaussRssi[x]) == 1:
        RSSfinal[x] = gaussRssi[x][0]

# print('sum: ' + str(sumRSS))
# print('yRSS: ' + str(yRSS))
# print('oRSS: ' + str(oRSS))
# print('RSS: ' + str(RSS))
for x in range(len(RSSfinal)):
    print(RSSfinal[x])
print('RSSfinal: '+str(RSSfinal))