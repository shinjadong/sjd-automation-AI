def calculator(num1, num2, operator):
    """간단한 계산기 함수"""
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            return "0으로 나눌 수 없습니다!"
    else:
        return "잘못된 연산자입니다!"
    
    return f"결과: {result}"

def interactive_calculator():
    """인터랙티브 계산기"""
    print("간단한 계산기 프로그램입니다.")
    print("연산자를 선택하세요: +, -, *, /")
    
    try:
        operator = input("연산자: ")
        num1 = float(input("첫 번째 숫자: "))
        num2 = float(input("두 번째 숫자: "))
        
        result = calculator(num1, num2, operator)
        print(result)
    except ValueError:
        print("올바른 숫자를 입력해주세요!")
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")

if __name__ == "__main__":
    # 테스트 실행
    print("=== 테스트 결과 ===")
    print(calculator(10, 5, '+'))
    print(calculator(10, 5, '-'))
    print(calculator(10, 5, '*'))
    print(calculator(10, 5, '/'))
    print(calculator(10, 0, '/'))
    print(calculator(10, 5, '%'))
    
    print("\n=== 인터랙티브 모드 ===")
    interactive_calculator()