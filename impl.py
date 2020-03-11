
import json


def table_to_dict_list(table):
    """
    2차원 배열. [{}...] 형태로 변경.
    0번째 로우는 헤더이기 때문에 배열의 인덱스로 헤더를 만들고 딕트 형태로 오브젝트 생성.
    """

    column_names = []
    dict_list = []

    for index, row in enumerate(table):
        if index != 0:
            row_data = dict();
            for column_index, column_value in enumerate(row):
                row_data[column_names[column_index]] = column_value
            dict_list.append(row_data)
        else:
            for column in row:
                column_names.append(column)

    return dict_list


########################################


def multiple_of_three(values):
    """
    3의 배수만 필러링. 파이썬 문법 활용하여 처리.
    """
    filtered = [i for i in values if i % 3 == 0]

    return filtered

########################################


def pick_gloss_term(dumpped_json, term):
    """
    제이슨 스트링을 딕트 형태로 바꾼 후
    찾으려는 키가 있을 때까지 와일문 활용하여 탐색.
    있을 경우 해당 키의 값을, 없을 경우 return None.

    출제의도 재귀..
    """
    json_dict = json.loads(dumpped_json)

    key_length = len(json_dict.keys())

    while key_length != 0:
        if term in json_dict:
            return json_dict[term]
        else:
            dict_count = 0
            for key in json_dict:


                if key in json_dict and isinstance(json_dict[key], dict):
                    json_dict = json_dict[key]
                    key_length = len(json_dict.keys())
                    dict_count += 1
            if dict_count == 0:
                key_length = 0

    return None


########################################


def sort_and_distinct(data):
    """
    셋으로 중복 제거한 후 소팅.
    """
    return sorted(set(data))


########################################


def sort_by_amount(data):
    """
    람다식 활용. 기준이 되는 키 역순으로 소팅.
    """
    return sorted(data, key=lambda x: -x.amount)


########################################


def calc(opname, x, y):
    """
    파이썬에는 스위치가 없기 때문에 딕트로 처리.
    제로디바이드 에러를 막기 뒤해 y의 값이 0일 경우는 return 0.
    """
    calculator = {
        'multiply': x * y,
        'divide': x / y if y != 0 else 0,
        'add': x + y,
        'subtract': x - y
    }

    return calculator.get(opname, 'not allowed opname')


########################################


def find_deepest_child(data):
    """
    딕트를 제이슨 스트링으로 변경하고 indent를 설정한 채로 변수화함.
    그 변수를 줄 단위로 읽고 indent의 값이 가장 큰 Row의 프로퍼를 리턴.
    """
    json_str = json.dumps(data, indent=2)
    indent_count = 0
    max_depth_key = ''
    readline_list = json_str.split('\n')

    for line in readline_list:
        line_indent_count = line.count(' ')
        if line_indent_count > indent_count:
            indent_count = line_indent_count
            max_depth_key = line.split(':')[0].replace('"', '').strip()

    return max_depth_key


def find_nodes_that_contains_more_than_three_children(data):
    """
    재귀 호출하여 완전 탐색하며 프로퍼티를 3개 이상 가지는 프로퍼티를 찾는다.
    """
    result = []

    for key in data:
        if isinstance(data[key], dict):
            if len(data[key].keys()) >= 3:
                result.append(key)
            extends = find_nodes_that_contains_more_than_three_children(data[key])
            if len(extends) != 0:
                result.extend(extends)

    return set(result)


def count_of_all_distributions_of_linux(data):
    """
    초기 호출 시에는 리눅스 자체의 데이터를 처리하고
    그 후로는 리눅스의 child 프로퍼티들을 처리한다.
    """
    result = 0

    if 'Linux' in data:
        result += len(data['Linux'].keys())
        linux_data = data['Linux']
        for key in linux_data:
            if isinstance(linux_data[key], dict):
                result += count_of_all_distributions_of_linux(linux_data[key])

    else:
        for key in data:
            if isinstance(data[key], dict):
                result += count_of_all_distributions_of_linux(data[key])
            else:
                result += 1

    return result


########################################

class Element:
    """
    Dom 문자열 만드는 클래스. Notice와 Message가 이를 상속한다
    """

    def generate_notice_li(self):
        return '<li class="notice">' + self.notice + '</li>'

    def generate_profile_li(self, class_name):
        return (
            '\n<li class="' + class_name + '">\n' +
            '    ' + '<img class="profile" src="${user_image(' + str(self.userid) + ')}">\n' +
            '    ' + '<div class="message-content">' + self.content + '</div>\n' +
            '</li>'
         )


class Notice(Element):

    def __init__(self, notice):
        self.notice = notice


class Message(Element):

    def __init__(self, userid, content):
        self.userid = userid
        self.content = content


def render_messages(messages, **kwargs):

    current_user = kwargs.get('current_userid')
    result = ''

    for message in messages:
        if isinstance(message, Notice):
            result += message.generate_notice_li()

        elif isinstance(message, Message):
            result += message.generate_profile_li('right' if current_user == message.userid else 'left')

    return result

