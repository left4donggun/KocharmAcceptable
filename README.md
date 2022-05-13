# 컴활공석알림이

pip install KocharmAcceptable

# 사용방법

import KocharmAcceptable<br>
kc = KocharmAcceptable<br>
result = kc.get("컴퓨터활용능력 - 실기","1급","특별광역시","대구상공회의소 제2시험장(지하1층)")

for x in result:
    print(x,result[x])
