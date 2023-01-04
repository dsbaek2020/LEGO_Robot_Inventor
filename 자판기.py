#만든이: 젤리코딩학원 (백대성)
#만든날짜: 2023. 1. 3(화)

from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# 여기에서 객체를 만듭니다.
hub = MSHub()
paper_scanner = ColorSensor('D')

# 여기에서 프로그램을 작성합니다.
hub.speaker.beep()



motor_F3 = Motor('E')
motor_F2 = Motor('C')
motor_F1 = Motor('A')

# 모터를 0도 위치로 작동합니다.
motor_F3.run_to_position(0, 'shortest path', 20)
motor_F2.run_to_position(0, 'shortest path', 20)
motor_F1.run_to_position(0, 'shortest path', 20)



#변수 정의를 합니다.
select_item_number = 1

input_money = 0

coin_value = {
'red' : 50,      #5만원권
'cyan' : 10,     #만원권
'yellow' : 5,    #5천원권
'white': 1       #천원권
}

item_led_positon = {
1: (0, 0),
2: (0, 4),
3: (2, 0),
4: (2, 4),
5: (4, 0),
6: (4, 4),
}

select_positon = {
1: (0, 1),
2: (0, 3),
3: (2, 1),
4: (2, 3),
5: (4, 1),
6: (4, 3),
}


#모터와 관련된 자료를 딕셔너리로 정의합니다. -------------------------
item_motor_position = {
1: {'motor': 'E', 'angle': 330},
2: {'motor': 'E', 'angle': 30},
3: {'motor': 'C', 'angle': 330},
4: {'motor': 'C', 'angle': 30},
5: {'motor': 'A', 'angle': 330},
6: {'motor': 'A', 'angle': 30},
}

motors = {
    'A' : motor_F1,
    'C' : motor_F2,
    'E' : motor_F3
}


def pop_item(n):

    #아이템 번호 n 에 따른 모터의 이름과 각도를 item_motor_position 딕셔너리에 정의한 정보들로부터 가져옵니다. 
    motor_name = item_motor_position[n]['motor']
    motor_angle = item_motor_position[n]['angle']

    #모터를 해상 상품이 나오도록 해당 각도로 움직입니다. 
    motors[motor_name].run_to_position(motor_angle, 'shortest path', 60)

    #모터를 다시 0도로 정렬합니다. 
    motors[motor_name].run_to_position(0, 'shortest path', 60)








class Item():
    def __init__(self, name, cost, item_number):
        self.name = name #상품이름
        self.cost = cost #가격
        self.position = item_number  #상품이 자판기 어디에 있는지 나타낸 번호
        self.count = 1  #현재 상품의 갯수 
        self.set_item_status() # 상품의 상태를 표시 

    #현재 상품의 재고(수량)을 반환한다. 
    def get_number_Of_item(self):
        return self.count

    #이 상품의 개수를 감소 시킨다. 
    def decrease_item(self):
        self.count-=1

    #이 상품의  이름과  남은 수량을 문자열로 반환한다. 
    def __str__(self):
        return '<'+self.name+ '=' +str(self.count)+'>'

    #이 상품의 현재 상태를 led로 표시 
    def set_item_status(self):
        if self.count > 0 :
            self.draw_led_on()
        else:
            self.draw_led_off()

    #이 함수를 호출하면 상품의 있을때 led를 해당 위치에 표시해준다. 
    def draw_led_on(self):
        hub.light_matrix.set_pixel(item_led_positon[self.position][1],
                                item_led_positon[self.position][0], 100)
    #이 함수를 호출하면 상품이 없음을 나타내기 위해서 led를 끈다.
    def draw_led_off(self):
        hub.light_matrix.set_pixel(item_led_positon[self.position][1],
                                item_led_positon[self.position][0], 0)
    
    #이 함수는 이 상품이 선택됨을 알려주기 위해서 호출한다. 
    def select_led(self):
        hub.light_matrix.set_pixel(select_positon[self.position][1],
                                select_positon[self.position][0], 80)

    #이 함수는 이 상품이 선택해제 되었음을 나타내기 위해서 호출한다. 
    def diselect_led(self):
        hub.light_matrix.set_pixel(select_positon[self.position][1],
                                select_positon[self.position][0], 0)




# 상품의 이름, 가격, 위치를 속성으로한 아이템 클래스의 인스턴스(객체)를 6개 선언한다. 
#             이름                 가격(천원)    상품위치 
item1 = Item('dualRedPin',          2,       1)
item2 = Item('threeGear',           5,       2)
item3 = Item('whiteTwoWheel',       10,      3)
item4 = Item('GrayBulePin',         15,      4)
item5 = Item('GrayBrounPin',        50,      5)
item6 = Item('WhiteAngleAxisHole',  70,      6)

#만들어진 아이템 클래스의 인스턴스를 모은 리스트를 만들어, 대괄호 [] 연산자로 각각 접근 하도록 한다. (if else 문 개수를 줄이기 위해서 )
items = [item1, item2, item3 ,item4, item5, item6]



# 동전을 감지
def check_Coin():
    color = paper_scanner.get_color()
    if not_equal_to(color, None) and color != 'black':
        hub.speaker.play_sound('Bing')
        hub.status_light.on(color)
        #hub.light_matrix.write(color)
        print(color)
        return color
    else:
        return 'not detected'
 


#프로그램을 시작합니다. 
items[select_item_number-1].select_led()

while True:

    #1. 동전이 들어 왔는지 또는 아닌지 확인한다.
    coin_Color = check_Coin()

    #2. 동전이 감지되면 누적된 금액을 계산(덧셈)하고 표시 
    if coin_Color != 'not detected':
       input_money =  input_money + coin_value[coin_Color]
       
       #넣은 금액을 콘솔에 표시합니다. 
       print('Your input money = ', input_money)

       #넣은 금액을 led 메트릭스에 표시합니다.
       hub.light_matrix.write(input_money)
       wait_for_seconds(1)
       hub.light_matrix.off()

       #상품의 상태를 다시 표시한다. 
       for item in items:
            item.set_item_status()

       #선택 위치를 다시 표시한다. 
       items[select_item_number-1].select_led()



    #3. 만약 오른쪽 버튼이 눌러지면 상품 선택을 합니다. 
    if hub.right_button.is_pressed():
        # 뭔가를 합니다.
        hub.speaker.beep()

        #이전에 선택한 상품을 가리킨 led를 끈다. 
        items[select_item_number-1].diselect_led()

        # 현재 선택이 6번이라면 1로 초기화 한다. 아니면 상품번호는 증가시킨다.  
        if select_item_number == 6:
            select_item_number = 1
        else:
            select_item_number+=1
            
        #현재 선택된 상품을 표시한다. 
        items[select_item_number-1].select_led()

    



    #4. 만약 왼쪽 버튼이 눌러지고, 넣은 금액이 선택된 상품의 값보다 같으면,
    if hub.left_button.is_pressed():
        # 소리를 냅니다. 
        hub.speaker.beep()

        #상품을 나오게 하고, (금액이 작거나 크면 놓은 금액을 모두 환불하고 금액을 초기화 한다.)
        #상품이 나오면, 해당 상품 위치를 가리키는 LED를 끈다. 그리고 금액을 초기화한다.  

        # 자판기에서 상품을 내보냅니다.
        pop_item(select_item_number)

        # 이 아이템의 수량을 하나 감소 시킵니다.
        items[select_item_number-1].decrease_item()

        #상품의 상태를 다시 표시한다.
        for item in items:
            item.set_item_status()






