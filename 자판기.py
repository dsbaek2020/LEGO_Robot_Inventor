#만든이: 젤리코딩학원 (백대성)
#만든날짜: 2023. 1. 3(화)
#수정: 1.5(목)


from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
from random import randint, choice


#아이템(상품)에 대한 클래스를 선언하고 정의합니다. 
class Item():
    def __init__(self, name, cost, item_number):
        self.name = name #상품이름
        self.cost = cost #가격
        self.position = item_number#상품이 자판기 어디에 있는지 나타낸 번호
        self.count = 1#현재 상품의 갯수
        self.set_item_status() # 상품의 상태를 표시

    #현재 상품의 재고(수량)을 반환한다.
    def get_number_Of_item(self):
        return self.count

    #이 상품의 개수를 감소 시킨다.
    def decrease_item(self):
        self.count-=1

    #이 상품의이름과남은 수량을 문자열로 반환한다.
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




# 여기에서 레고 마인드 스톰 하드웨어와 관련된 객체를 만듭니다. ----------------------
#MSHub 클래스의 생성자를 호출하여 객체를 생성합니다.
hub = MSHub()
#ColorSensor 클래스의 생성자를 호출하여 객체를 생성합니다.
paper_scanner = ColorSensor('D')

#Motor 클래스의 생성자를 호출하여 객체를 3개 각각 생성합니다.
motor_F3 = Motor('E')
motor_F2 = Motor('C')
motor_F1 = Motor('A')

# 여기에서 프로그램을 작성합니다.
hub.speaker.beep()


#자판기 프로그램과 관련된 변수 정의를 합니다. -----------------------------------
#아래의 코드에서는 자판기와 관련된 정보를 단일 변수 또는 딕셔너리, 리스트, 튜플로 만듭니다. 

#자판기의 잠금시 사용되는 암호를 저장하는 변수를 초기화합니다.
pass_code = ''
#어떤 색으로 된 동전을 넣었는지를 나타내는 아래의 변수를 초기화합니다.(동전 3개까지만 기록)
pass_code_input = ''
#넣은 동전의 갯수를 나타내는 변수를 초기화 합니다.
numOfCoin = 0
#자판기의 잠금을 잠금상태로 합니다.
lock = 'on'

#꺼낼려고 하는 선택된 상품번호를 나타내는 변수를 정의합니다.
select_item_number = 1
#사용자가 넣은 금액을 나타내는 변수를 정의합니다.
input_money = 0

#동전의 색깔과 원화를 정의합니다.
#딕셔너리로 정의하며 key값은 색, value는 원화가치
coin_value = {
'red' : 50,    #5만원권
'cyan' : 10,    #만원권
'yellow' : 5,    #5천원권
'white': 1    #천원권
}

#상품의 위치를 나타내는 LED 매트릭스의 좌표 y와 x를 정의합니다.
#딕셔너리로 정의하며 key는 상품번호 value는 좌표값(튜플로 정의)임.
item_led_positon = {
1: (0, 0),
2: (0, 4),
3: (2, 0),
4: (2, 4),
5: (4, 0),
6: (4, 4),
}

#선택된 상품을 가리키기 위한 커서의 위치를 튜플로 정의합니다.
#튜플로 정의된 값은 아래의 딕셔너리의 value에 저장되며, 이 딕셔너리의 key값은
#상품의 번호입니다.
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
#모터가 연결된 허브의 포트번호와 모터 객체를 딕셔너리로 각각 정의합니다.
motors = {
    'A' : motor_F1,
    'C' : motor_F2,
    'E' : motor_F3
}

# Item클래스로부터 상품 객체를 만듭니다.-------------------------------------------------------
# 상품의 이름, 가격, 위치를 속성으로한 아이템 클래스의 인스턴스(객체)를 6개 선언한다.
#            이름                가격(천원)    상품위치
item1 = Item('dualRedPin',        2,    1)
item2 = Item('threeGear',        5,    2)
item3 = Item('whiteTwoWheel',    10,    3)
item4 = Item('GrayBulePin',        15,    4)
item5 = Item('GrayBrounPin',        50,    5)
item6 = Item('WhiteAngleAxisHole',70,    6)

#만들어진 아이템 클래스의 인스턴스를 모은 리스트를 만들어, 
#대괄호 [] 연산자로 각각 접근 할 수 있도록 합니다. (if else 문 개수를 줄이기 위해서 )
items = [item1, item2, item3 ,item4, item5, item6]




#-------------------함수를 선언합니다. --------------------------

#자판기에 동전 세개의 넣어,아래의 함수에서
#생성된 암호와 같은 순서로 동전을 넣으면 놓은 동전 금액과 관계없이
#자판기는 하나의 상품의 임의로 나오게 합니다.
#예를 들어서 make_password 함수가 pass_code 전역변수의 값을
# whiteyellowred으로 생성했다면, 사용자가 우연히
# 흰색-노랑-빨강 순서로 동전을 넣으면 자판기는 무작위로 1번부터 6번중
# 하나의 상품을 내어 줍니다.
def make_password():
    #전역변수 이름을 선언해준다. 그래야만 이 함수 내부에서 값을 수정 할 수 있음.
    global pass_code

    coin_color = ['white', 'yellow', 'cyan', 'red']
    pass_code = ''

    k = choice( coin_color )
    coin_color.remove(k)
    pass_code = pass_code + k

    k = choice( coin_color )
    coin_color.remove(k)
    pass_code = pass_code + k

    k = choice( coin_color )
    coin_color.remove(k)
    pass_code = pass_code + k

    print('-----------------------------')
    print('pass word --> ', pass_code)
    print('-----------------------------')
    wait_for_seconds(2)

# 색깔이 다른 동전을 넣은 순서가 암호에서 가리키는 동전 색깔의 순서와
# 일치하는지 확인하고 맞으면 상품을 하나 꺼내어 주는 함수입니다.
# 동전 3개 새로 넣어지면 이 함수는 상품을 꺼내어도 되는지 판단 처리를 합니다.
def happy_mode():
    global pass_code_input, numOfCoin, lock

    pass_code_input = pass_code_input + coin_Color
    print('coin history =', pass_code_input)
    print('num of coin = ', numOfCoin)


    #동전이 3개가 들어왔으면 아래의 코드를 실행합니다.
    if numOfCoin == 3:
        #동전의 개수를 0으로 초기화합니다.
        numOfCoin = 0
        #색깔이 다른 3개의 동전을 넣은 순서가 pass_code에 정의된 동전의 색깔 3개로 구성된 나열하고 일치하면
        #아래의 코드를 실행합니다.
        if pass_code_input == pass_code:
            #자판기의 잠금을 해제합니다.
            lock = 'off'
            #잠금이 해제됨을 나타내는 이모티콘을 콘솔에 출력합니다.
            print('''
                .---    --.
                / .-    -. \
                / /
                | |
                _| |________| |_
                .' |_|        |_| '.
                '._____ ____ _____.'
                |    .'____'.    |
                '.__.'.'    '.'.__.'
                '.__| YALE |__.'
                |'.'.____.'.'|
                '.____'.____.'____.'LGB
                '.________________.'
            ''')
            # 'Ha Ha Ha' 사운드를 재생하고 완료될 때까지 기다립니다
            hub.speaker.play_sound('Celebrate')
        else:
            # 'Ha Ha Ha' 사운드를 재생하고 완료될 때까지 기다립니다
            hub.speaker.play_sound('Ha Ha Ha')

        #어떤 색으로 된 동전을 넣었는지를 나타내는 아래의 변수를 초기화합니다.(동전 3개까지만 기록)
        pass_code_input = ''


# 동전을 감지하는 함수입니다.
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


#모터를 회전하여 아이템을 자판기에서 꺼내는 함수를 정의합니다.
def pop_item(n):

    #아이템 번호 n 에 따른 모터의 이름과 각도를 item_motor_position 딕셔너리에 정의한 정보들로부터 가져옵니다.
    motor_name = item_motor_position[n]['motor']
    motor_angle = item_motor_position[n]['angle']

    #모터를 해상 상품이 나오도록 해당 각도로 움직입니다.
    motors[motor_name].run_to_position(motor_angle, 'shortest path', 60)

    #모터를 다시 0도로 정렬합니다.
    motors[motor_name].run_to_position(0, 'shortest path', 60)


#하나의 아이템을 꺼내고 아이템의 수량을 1 감소시키는 함수입니다.
def pop_one_item(n):
    # 소리를 냅니다.
    hub.speaker.beep()

    #상품을 나오게 하고, (금액이 작거나 크면 놓은 금액을 모두 환불하고 금액을 초기화 한다.)
    #상품이 나오면, 해당 상품 위치를 가리키는 LED를 끈다. 그리고 금액을 초기화한다.

    # 자판기에서 상품을 내보냅니다.
    pop_item(n)

    # 이 아이템의 수량을 하나 감소 시킵니다.
    items[n-1].decrease_item()

    #상품의 상태를 다시 표시한다.
    for item in items:
        item.set_item_status()



#<<<<<<<<-----------프로그램을 시작합니다. ------------->>>>
# 모터를 0도 위치로 작동합니다.
motor_F3.run_to_position(0, 'shortest path', 20)
motor_F2.run_to_position(0, 'shortest path', 20)
motor_F1.run_to_position(0, 'shortest path', 20)
#커서의 위치를 상품1번을 지시하도록 합니다.
items[select_item_number-1].select_led()
#암호를 설정합니다.
make_password()


while True:

    #1. 동전이 들어 왔는지 또는 아닌지 확인한다.
    coin_Color = check_Coin()
    
    #2. 동전이 감지되면 누적된 금액을 계산(덧셈)하고 표시
    if coin_Color != 'not detected':
        input_money =input_money + coin_value[coin_Color]

        #들어온 동전을 누적하여 기록하기 위한 문자열을 갱신한다.
        numOfCoin  +=1
        #행운의 당첨이 된건지 확인하는 함수를 호출합니다.
        happy_mode()



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





    #4. 만약 왼쪽 버튼이 눌러지고, 넣은 금액이 선택된 상품의 값보다 같으면, 싱품이 나오도록 하세요.
    # 다르면, 동전을 밖으로 꺼내고 상품은 나오지 않도록 하세요
    if hub.left_button.is_pressed():
        #힌트 ------------------------------------- 
        #아래의 코드에서 ??? 대신 들어가야할 부분을 채우시오. ''' '''으로 처리된 주석은 지우시면 됩니다. 
        # input_money는 사용자가 넣은 총 금액입니다. 
        # pop_one_item는 상품을 꺼내기 위한 처리를 하는 함수 입니다. 
        # select_item_number 변수는 커서로 선택한 상품의 번호입니다. 
        '''
        if input_money   ==  ???? :
            pop_one_item(select_item_number)
        '''
        


    # 우연히 넣은 동전 3개가 암호와 같으면 자판기는 1에서6번 상품중에 하나를 밖으로 꺼내어 줍니다. 
    if lock == 'off':
        hub.speaker.beep()
        #상품을 하나 배출하기 
        pop_one_item(randint(1,6))
        lock = 'on'
        pass_code_input = ''
        #새로운 암호를 생성하기 
        make_password()








