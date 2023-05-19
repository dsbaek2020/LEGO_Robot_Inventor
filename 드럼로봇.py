#만든사람:경훈,준언
#날짜:2023-05-17

from mindstorms import MSHub
from mindstorms import Motor
from mindstorms.control import Timer, wait_for_seconds

# 여기에서 객체를 만듭니다.
hub = MSHub()
motor_rightHand = Motor('F')
motor_leftHand = Motor('B')
# 여기에서 프로그램을 작성합니다.
#for i in range(3):
 #hub.speaker.beep()
#wait_for_seconds(3)

music = ['left', 'right', '', 'right', 'left', 'right']

def hit_green_drum():
    for i in range(1):
    #팔을 올리는 동작을 코딩하세요.
        motor_rightHand.run_to_position(100)
    #팔을 내리는 동작을 코딩하세요.
        motor_rightHand.run_to_position(200)

def hit_white_drum():
    for i in range(1):
        motor_leftHand.run_to_position(65)
        motor_leftHand.run_to_position(350)

hub.light_matrix.show_image('YES')
hub.light_matrix.rotate('counterclockwise')

while True:
    for i in range(len(music)):
        if music[i] == 'left':
             hit_white_drum()
        elif music[i] == 'right':
             hit_green_drum()
        else:
             wait_for_seconds(1)

'''
    if hub.left_button.is_pressed():
        # 뭔가를 합니다.
        hit_white_drum()
    else:
        if hub.right_button.is_pressed():
            #초록색 드럼을 치는 함수를 실행(호출)합니다.
            hit_green_drum()


            hub.light_matrix.show_image('HAPPY')
            hub.speaker.play_sound('Ouch')
#            hub.light_matrix.rotate('counterclockwise')
            wait_for_seconds(1)
            hub.light_matrix.off()

    
print('끝')
'''


