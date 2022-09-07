# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#

from typing import Any, Text, Dict, List

from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from extentions.utils import RANDOM, response_list_product, convert_to_float, LOWERCASE, UPPERCASE, look_up_in_domain,look_up_subject_group
import pandas as pd

DB_PATH = 'convert/entities.csv'

major_info = {
    'kỹ thuật điện': 'Ngành Kỹ thuật điện dành cho các sinh viên có sở thích liên quan đến điện năng.\nChương trình bao gồm các môn học cốt lõi cần thiết về kỹ thuật điện - điện tử nói chung, và kỹ thuật điện nói riêng, cùng với nhiều môn học lựa chọn về thiết bị điện, điện tử công suất, nhà máy điện, mạng điện, hệ thống điện, và năng lượng tái tạo.',
    'kỹ thuật hóa học': 'Chương trình bao gồm các môn cốt lõi cần thiết về kỹ thuật hóa học và nhiều môn lựa chọn về công nghệ chuyên ngành.\n Ngoài ra, chương trình được gắn kết với chương trình đào tạo thạc sỹ/tiến sỹ ngành Kỹ thuật Hóa học tại trường đại học Bách Khoa TP.HCM',
    'kỹ thuật hàng không': 'Ngành Kỹ Thuật Hàng Không (KTHK) dành cho các sinh viên có đam mê về máy bay và các phương tiện bay.\n Chương trình bao gồm các nhóm môn cốt lõi cần thiết về nền tảng của kỹ thuật hàng không như Khí Động Lực Học, Cơ học bay và điều khiển bay, Kết cấu hàng không, Hệ thống lực đẩy, Thiết kế và bảo dưỡng máy bay.',
    'công nghệ may': 'Ngành Công nghệ may dành cho các sinh viên có sở thích và năng khiếu về kỹ thuật may công nghiệp và thời trang. Chương trình học bao gồm các kiến thức chuyên sâu về kỹ thuật may cơ bản và nâng cao, thiết bị may, mỹ thuật trang phục, quản lý sản xuất trong dây chuyền may công nghiệp hiện đại, ứng dụng tin học trong thiết kế và vận hành công nghiệp may.',
    'công nghệ sinh học': 'Chương trình Công nghệ Sinh học dành cho các sinh viên yêu thích khoa học sự sống và quan tâm đến việc ứng dụng cũng như cải tạo các quy luật sinh học trong tự nhiên để tạo ra những sản phẩm có ích trong cuộc sống. Chương trình bao gồm các môn học cơ bản nhằm cung cấp cho sinh viên những kiến thức về khoa học tự nhiên, ngoại ngữ, những kiến thức cần thiết về chính trị, kinh tế, văn hóa, xã hội, ngoại ngữ, cũng như các môn học cơ sở ngành và chuyên ngành.',
    'logistics và quản lý chuỗi cung ứng': 'Ngành Logistics và Quản lý chuỗi cung ứng trang bị cho người học đầy đủ kiến thức, kỹ năng chuyên môn và thái độ chuyên nghiệp làm nền tảng vững chắc cho sự thành công của kỹ sư Logistics và Quản lý Chuỗi cung ứng tại các doanh nghiệp.',
    'khoa học máy tính': 'Ngành Khoa học Máy tính thuộc nhóm ngành Máy tính và Công nghệ thông tin. Mục tiêu của chương trình ngành Khoa học Máy tính là đào tạo ra những kỹ sư có chất lượng cao, có khả năng thiết kế, xây dựng và triển khai những hệ thống phần mềm đáp ứng nhu cầu trong nước và quốc tế. Kỹ sư tốt nghiệp ngành Khoa học Máy tính cũng được trang bị những kiến thức cần thiết để có thể học tiếp cao học và tiến sỹ trong lĩnh vực Máy tính và Công nghệ thông tin.',
    'kỹ thuật máy tính': 'Ngành Kỹ thuật Máy tính thuộc nhóm ngành Máy tính và Công nghệ thông tin. Mục tiêu của chương trình ngành Kỹ thuật Máy tính là đào tạo ra những kỹ sư có chất lượng cao, có khả năng thiết kế, xây dựng và triển khai những hệ thống phần mềm và phần cứng cho máy tính và các thiết bị điều khiển nhằm đáp ứng nhu cầu trong nước và quốc tế.',
    'công nghệ kỹ thuật ô tô': 'Ngành Công nghệ Kỹ thuật Ô tô đào tạo kỹ sư có kiến thức cơ bản về Toán học, Khoa học tự nhiên và Kỹ thuật cơ sở đáp ứng việc tiếp thu các kiến thức chuyên ngành, cũng như có khả năng tự học nâng cao trình độ chuyên môn.',
    'kỹ thuật điện tử viễn thông': 'Ngành kỹ thuật điện tử-viễn thông dành cho sinh viên có sở thích và đam mê làm việc trong lĩnh vực công nghệ viễn thông và thông tin, vi mạch, bán dẫn, hệ thống nhúng và hệ thống điện tử ứng dụng, xử lý tín hiệu âm thanh, hình ảnh và đa phương tiện.',
    'kỹ thuật cơ điện tử': 'Cơ điện tử là sự kết hợp của kỹ thuật cơ khí, kỹ thuật điện tử và kỹ thuật máy tính. Đây là ngành rất quan trọng và không thể thiếu trong sự phát triển của khoa học kỹ thuật hiện đại. Mục đích của ngành khoa học tổng hợp liên ngành này là nhằm phát triển tối đa tư duy hệ thống trong thiết kế và phát triển sản phẩm để tạo ra những sản phẩm mới có những tính năng vượt trội. Robot chính là một sản phẩm tiêu biểu của ngành Kỹ thuật cơ điện tử.',
    'kỹ thuật điều khiển và tự động hóa': 'Ngành Kỹ thuật điều khiển & Tự động hóa dành cho các sinh viên có sở thích về điều khiển các đối tượng kỹ thuật, quá trình và công nghệ tự động hóa các quá trình sản xuất. Chương trình bao gồm hai hướng đó là Kỹ thuật điều khiển và Công nghệ tự động hóa.'
}


def connect_database(conn=DB_PATH):
    data = pd.read_csv(conn)
    return data


def get_list_major_name_KEY():
    df = connect_database()
    return list(df.major_name)


list_major_name = get_list_major_name_KEY()


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker: Tracker, domain):
        # output a message saying that the conversation will now be
        # continued by a human.
        message1 = "Úi, rất tiếc câu hỏi của bạn nằm ngoài tri thức của mình, bạn vui lòng hỏi câu khác nha!"
        message2 = "Opps, câu hỏi nằm ngoài tri thức của mình, bạn hãy hỏi lại câu khác giúp ad nha!!"
        dispatcher.utter_message(text=RANDOM((message1,message2)))
        return []


class ActionResponseMajorInfo(Action):
    def name(self) -> Text:
        return "action_response_major_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu, hãy cho mình tên một ngành cụ thể")
        elif(look_up_in_domain(major_name) not in list_major_name):
            AllSlotsReset()
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập lại giúp ad nha!")
            dispatcher.utter_message(
                text="Hịện trường đang đào tạo các ngành: "+response_list_product(list_major_name)+"\nBạn muốn hỏi về ngành nào nhỉ.")
            return [SlotSet("major_name", None)]
        else:
            try:
                mess = major_info[look_up_in_domain(major_name)]
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []


def get_type_edu(major_name):
    df = connect_database()
    type_edu_info = df[df['major_name'] == major_name]
    output = type_edu_info['type_edu'].iloc[0]
    return output.replace('@', ', ')


class ActionResponseMajorTypeEdu(Action):

    def name(self) -> Text:
        return "action_response_major_type_edu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Hãy cho mình một chuyên ngành cụ thể ạ")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, nên không có thông tin về hệ đào tạo của ngành này ạ!")
            return [SlotSet("major_name", None)]
        else:
            try:
                result = get_type_edu(major_name)
                mess = f"Dạ ngành {major_name} đào tạo những hệ " + \
                    result+" ạ.\n Bạn cần mình giúp gì nữa không ạ :3"
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []


def get_major_point(major_name):
    df = connect_database()
    point_info = df[df['major_name'] == major_name]
    output = point_info['point'].iloc[0]
    return str(output)


class ActionResponseMajorPoint(Action):

    def name(self) -> Text:
        return "action_response_major_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu ý của bạn, hãy cho mình một ngành học cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, nên không có thông tin về điểm ạ!")
            return [SlotSet("major_name", None)]
        else:
            try:
                result = get_major_point(major_name)
                mess = f"Dạ hiện tại điểm sàn của ngành {major_name} là " + \
                    result + ", thông tin đến bạn ạ"
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []


def get_career(major_name):
    df = connect_database()
    career_info = df[df['major_name'] == major_name]
    output = career_info['career'].iloc[0]
    return str(output)


class ActionResponseMajorCareer(Action):

    def name(self) -> Text:
        return "action_response_major_career"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu ý của bạn, hãy cho mình một ngành học cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập lại giúp ad nha!")
            return [SlotSet("major_name", None)]
        else:
            try:
                result = get_career(major_name)
                list_careers = result.split("@")

                mess1 = f"Cơ hội việc làm của ngành {major_name} là: \n"
                mess2 = ''
                for item in list_careers:
                    mess2 += ('\t\t\t • '+item.capitalize()+'\n')
                mess3 = 'Bạn tham khảo nhé !'
                mess = mess1 + mess2 + mess3
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []


def get_major_tuition(major_name):
    df = pd.read_csv(DB_PATH)
    tuition_info = df[df['major_name'] == major_name]
    output = tuition_info['tuition'].iloc[0]
    return str(output)


class ActionResponseMajorTuition(Action):

    def name(self) -> Text:
        return "action_response_major_tuition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu ý của bạn, hãy cho mình một ngành học cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập lại giúp ad nha!")
            return [SlotSet("major_name", None)]
        else:
            try:
                result = get_major_tuition(major_name)
                mess = f"Dạ học phí của ngành {major_name} là "+result + \
                    " trên một tín chỉ ạ. Bạn cần mình giúp gì nữa không ạ"
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []


def get_subject_group(major_name):
    df = connect_database()
    subject_group_info = df[df['major_name'] == major_name]
    output = subject_group_info['subject_group'].iloc[0]
    return str(output.replace('@', ', '))


class ActionResponseSubjectGroup(Action):

    def name(self) -> Text:
        return "action_response_major_subject_group"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu ý của bạn, hãy cho mình một ngành học cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập lại giúp ad nha!")
            return [SlotSet("major_name", None)]
        else:
            try:
                result = get_subject_group(major_name)
                mess = f"Dạ ngành {major_name} tuyển sinh các khối " + \
                    result+" thông tin đến bạn."
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []


def get_major_criteria(major_name):
    df = pd.read_csv(DB_PATH)
    criteria_info = df[df['major_name'] == major_name]
    output = criteria_info['criteria'].iloc[0]
    return str(output)


class ActionResponseMajorCriteria(Action):

    def name(self) -> Text:
        return "action_response_major_criteria"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)
        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu ý của bạn, hãy cho mình một ngành học cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập lại giúp ad nha!")
            return [SlotSet("major_name", None)]
        else:
            try:
                result = get_major_criteria(major_name)
                mess = f"Năm 2022 ngành {major_name} dự kiến tuyển sinh " + \
                    result+" sinh viên ạ"
            except:
                mess = "Câu hỏi của bạn nằm ngoài tri thức của mình, bạn có thể viết rõ hơn được không ạ"
            dispatcher.utter_message(
                text=mess)
        return []

# BEGIN RESPONSE LIST MAJOR BY POINT|SUBJECTGROUP


def get_major_by_point(point):
    df = pd.read_csv(DB_PATH)
    rows = df[df['point'] <= point]
    major_names = rows['major_name']
    return list(major_names)


class ActionResponseMajorNameByPoint(Action):

    def name(self) -> Text:
        return "action_response_major_name_by_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        point = tracker.get_slot("user_point")
        if ' điểm' in point:
            point = point.replace(' điểm', '')
            point = convert_to_float(point)
            if point is False:
                dispatcher.utter_message(
                    text="Mình chưa hiểu ý bạn, bạn vui lòng nhập lại điểm thi THPT QG giúp mình với ạ")
                return []

            # điểm đủ để vào trường là lớn hơn 15
            if(point < 15.0):
                mess = "Hiện tại điểm sàn các ngành mà trường đào tạo dao dộng trong khoảng từ 21 đến 26.5 điểm ạ.\n Mình rất tiếc ạ :("
            elif(point <= 0.0):
                mess = "Bạn từ sao Hỏa đến phải không @@!"
            elif(point > 35):
                mess = "Trên đời này còn có người giỏi như vậy sao ^^!" 
                #active form
                #point = 23
                #formmm
            else:
                major_names = get_major_by_point(point)
                mess = "Mình gửi bạn danh sách những ngành bạn có khả năng đỗ ạ :\n" + \
                    response_list_product(major_names)
        else:
            mess = "Xin lỗi, mình chưa hiểu\nBạn nên nhập theo ví dụ sau: '26.5 điểm'"
        dispatcher.utter_message(text=mess)
        return []


def get_major_by_subject_group(subject_group):
    df = pd.read_csv(DB_PATH)
    rows = df[['subject_group', 'major_name']]
    result = []
    for item in rows.values:
        if subject_group in item[0]:
            result.append(item[1])
    return result


class ActionResponseMajorNameBySubjectGroup(Action):
    def name(self) -> Text:
        return "action_response_major_name_by_subject_group"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject_group = tracker.get_slot("user_subject_group")
        if not subject_group:
            mess = "Mình chưa hiểu ạ, hãy cho mình một khối thi cụ thể"
        else:
            subject_group = UPPERCASE(subject_group)
            major_names = get_major_by_subject_group(subject_group)
            if(len(major_names) == 0):
                mess = "Trường chủ yếu đào tạo những ngành liên quan đến khoa học - kỹ thuật. Khối thi của bạn không phù hợp ạ :(("
            else:
                mess = "Danh sách các ngành tuyển sinh tân sinh viên khối "+subject_group + \
                    " là :" + \
                    response_list_product(major_names) + \
                    "\n Thông tin đến bạn ạ"
        dispatcher.utter_message(text=mess)
        return []

# END RESPONSE LIST MAJOR BY POINT|SUBJECTGROUP


# BEGIN PASS PASS PASS PASS PASS PASS PASS PASS YES/NO YES/NO YES/NO
def check_pass_point(major_name, point):
    df = pd.read_csv(DB_PATH)
    row = df[df['major_name'] == major_name]
    point_major = row['point'].iloc[0]
    return (point >= point_major), point_major


class ActionResponsePassPoint(Action):

    def name(self) -> Text:
        return "action_response_pass_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        point = tracker.get_slot("user_point")
        if ' điểm' in point:
            point = point.replace(' điểm', '')
            point = convert_to_float(point)
            major_name = tracker.get_slot("major_name")
            major_name = LOWERCASE(major_name)
            major_name = look_up_in_domain(major_name)

            if not major_name:
                dispatcher.utter_message(
                    text="Mình chưa hiểu ý bạn, hãy cho mình một tên chuyên ngành cụ thể nhé")
            elif(major_name not in list_major_name):
                dispatcher.utter_message(
                    text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập ngành khác giúp ad nha!")
                return [SlotSet("major_name", None)]
            else:
                # if point is False:
                #     dispatcher.utter_message(
                #         text="Mình chưa hiểu, bạn nhập lại điểm giúp mình được không ạ :(")
                #     return [SlotSet("user_point", None)]
                # else:
                    pass_point, major_point = check_pass_point(major_name, point)
                    if(pass_point):
                        dispatcher.utter_message(
                            text="Hiện tại điểm sàn của ngành {} là: {}, điểm chuẩn có thể tăng 1 đến 1.5 điểm. Mình tin bạn sẽ đỗ".format(major_name, major_point))
                    else:
                        dispatcher.utter_message(
                            text="Hiện tại điểm sàn của ngành {} là: {}, điểm chuẩn có thể tăng 1 đến 1.5 điểm. Bạn cố gắng chờ kết quả cuối cùng nhé".format(major_name, major_point))
        else:
            mess = "Xin lỗi, mình chưa hiểu\nBạn nên nhập theo ví dụ sau: '<26.5> điểm'"
            dispatcher.utter_message(mess)
        return []


def check_pass_subject_group(major_name, subject_group):
    df = pd.read_csv(DB_PATH)
    row = df[df['major_name'] == major_name]
    subject_group_major = row['subject_group'].iloc[0]
    if subject_group in subject_group_major:
        return True, str(subject_group_major)
    return False, str(subject_group_major)


class ActionResponsePassSubjectGroup(Action):
    def name(self) -> Text:
        return "action_response_pass_subject_group"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject_group = tracker.get_slot("user_subject_group")

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        major_name = look_up_in_domain(major_name)

        if not major_name:
            dispatcher.utter_message(
                text="Mình chưa hiểu, hãy cho mình một chuyên ngành cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(
                text="Dạ hiện tại trường chúng mình chưa đào tạo ngành này ạ, bạn vui lòng nhập lại giúp ad nha!")
            return [SlotSet("major_name", None)]
        else:
            if not subject_group:
                dispatcher.utter_message(
                    text="Mình không hiểu, hãy cho mình một khối thi cụ thể")
                return [SlotSet("user_subject_group", None)]
            else:
                subject_group = UPPERCASE(subject_group)
                subject_group = look_up_subject_group(subject_group)
                pass_subject_group, subject_group_major = check_pass_subject_group(
                    major_name, subject_group)
                if(pass_subject_group):
                    dispatcher.utter_message(text="Dạ ngành {} tuyển sinh các khối thi {}\n Chào mừng bạn đến với AIA University".format(
                        major_name, subject_group_major.replace('@', ', ').lstrip(', ')))
                else:
                    dispatcher.utter_message(text="Dạ ngành {} tuyển sinh các khối thi {}\n Bạn có thể tra cứu thông tin những ngành khác ạ".format(
                        major_name, subject_group_major.replace('@', ', ').lstrip(', ')))
        return []

# END PASS PASS PASS PASS PASS PASS PASS PASS YES/NO YES/NO YES/NO YES/NO


class ActionResponseMajorNames(Action):
    def name(self) -> Text:
        return "action_response_major_names"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Dạ các ngành đào tạo trường hiện đang đang đào tạo: "+response_list_product(list_major_name)+"\nBạn muốn hỏi về ngành nào nhỉ.")
        return [SlotSet("major_name", None)]