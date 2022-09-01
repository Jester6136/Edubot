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
import pandas as pd

DB_PATH = 'convert/entities.csv'

major_info = {
'kỹ thuật điện':'Ngành Kỹ thuật điện dành cho các sinh viên có sở thích liên quan đến điện năng. Chương trình bao gồm các môn học cốt lõi cần thiết về kỹ thuật điện – điện tử nói chung, và kỹ thuật điện nói riêng, cùng với nhiều môn học lựa chọn về thiết bị điện, điện tử công suất, nhà máy điện, mạng điện, hệ thống điện, và năng lượng tái tạo.',
'kỹ thuật hóa học':'Chương trình bao gồm các môn cốt lõi cần thiết về kỹ thuật hóa học và nhiều môn lựa chọn về công nghệ chuyên ngành. Ngoài ra, chương trình được gắn kết với chương trình đào tạo thạc sỹ/tiến sỹ ngành Kỹ thuật Hóa học tại trường đại học Bách Khoa TP.HCM',
'kỹ thuật hàng không':'Ngành Kỹ Thuật Hàng Không (KTHK) dành cho các sinh viên có đam mê về máy bay và các phương tiện bay. Chương trình bao gồm các nhóm môn cốt lõi cần thiết về nền tảng của kỹ thuật hàng không như Khí Động Lực Học, Cơ học bay và điều khiển bay, Kết cấu hàng không, Hệ thống lực đẩy, Thiết kế và bảo dưỡng máy bay.',
'công nghệ may':'Ngành Công nghệ may dành cho các sinh viên có sở thích và năng khiếu về kỹ thuật may công nghiệp và thời trang. Chương trình học bao gồm các kiến thức chuyên sâu về kỹ thuật may cơ bản và nâng cao, thiết bị may, mỹ thuật trang phục, quản lý sản xuất trong dây chuyền may công nghiệp hiện đại, ứng dụng tin học trong thiết kế và vận hành công nghiệp may.',
'công nghệ sinh học':'Chương trình Công nghệ Sinh học dành cho các sinh viên yêu thích khoa học sự sống và quan tâm đến việc ứng dụng cũng như cải tạo các quy luật sinh học trong tự nhiên để tạo ra những sản phẩm có ích trong cuộc sống. Chương trình bao gồm các môn học cơ bản nhằm cung cấp cho sinh viên những kiến thức về khoa học tự nhiên, ngoại ngữ, những kiến thức cần thiết về chính trị, kinh tế, văn hóa, xã hội, ngoại ngữ, cũng như các môn học cơ sở ngành và chuyên ngành.',
'logistics và quản lý chuỗi cung ứng':'Ngành Logistics và Quản lý chuỗi cung ứng trang bị cho người học đầy đủ kiến thức, kỹ năng chuyên môn và thái độ chuyên nghiệp làm nền tảng vững chắc cho sự thành công của kỹ sư Logistics và Quản lý Chuỗi cung ứng tại các doanh nghiệp.',
'khoa học máy tính':'Ngành Khoa học Máy tính thuộc nhóm ngành Máy tính và Công nghệ thông tin. Mục tiêu của chương trình ngành Khoa học Máy tính là đào tạo ra những kỹ sư có chất lượng cao, có khả năng thiết kế, xây dựng và triển khai những hệ thống phần mềm đáp ứng nhu cầu trong nước và quốc tế. Kỹ sư tốt nghiệp ngành Khoa học Máy tính cũng được trang bị những kiến thức cần thiết để có thể học tiếp cao học và tiến sỹ trong lĩnh vực Máy tính và Công nghệ thông tin.',
'kỹ thuật máy tính':'Ngành Kỹ thuật Máy tính thuộc nhóm ngành Máy tính và Công nghệ thông tin. Mục tiêu của chương trình ngành Kỹ thuật Máy tính là đào tạo ra những kỹ sư có chất lượng cao, có khả năng thiết kế, xây dựng và triển khai những hệ thống phần mềm và phần cứng cho máy tính và các thiết bị điều khiển nhằm đáp ứng nhu cầu trong nước và quốc tế.',
'công nghệ kỹ thuật ô tô':'Ngành Công nghệ Kỹ thuật Ô tô đào tạo kỹ sư có kiến thức cơ bản về Toán học, Khoa học tự nhiên và Kỹ thuật cơ sở đáp ứng việc tiếp thu các kiến thức chuyên ngành, cũng như có khả năng tự học nâng cao trình độ chuyên môn.',
'kỹ thuật điện tử viễn thông':'Ngành kỹ thuật điện tử-viễn thông dành cho sinh viên có sở thích và đam mê làm việc trong lĩnh vực công nghệ viễn thông và thông tin, vi mạch, bán dẫn, hệ thống nhúng và hệ thống điện tử ứng dụng, xử lý tín hiệu âm thanh, hình ảnh và đa phương tiện.',
'kỹ thuật cơ điện tử':'Cơ điện tử là sự kết hợp của kỹ thuật cơ khí, kỹ thuật điện tử và kỹ thuật máy tính. Đây là ngành rất quan trọng và không thể thiếu trong sự phát triển của khoa học kỹ thuật hiện đại. Mục đích của ngành khoa học tổng hợp liên ngành này là nhằm phát triển tối đa tư duy hệ thống trong thiết kế và phát triển sản phẩm để tạo ra những sản phẩm mới có những tính năng vượt trội. Robot chính là một sản phẩm tiêu biểu của ngành Kỹ thuật cơ điện tử.',
'kỹ thuật điều khiển và tự động hóa':'Ngành Kỹ thuật điều khiển & Tự động hóa dành cho các sinh viên có sở thích về điều khiển các đối tượng kỹ thuật, quá trình và công nghệ tự động hóa các quá trình sản xuất. Chương trình bao gồm hai hướng đó là Kỹ thuật điều khiển và Công nghệ tự động hóa.'
}

def connect_database(conn=DB_PATH):
    data = pd.read_csv(conn)
    return data

def get_list_major_name_KEY():
    df = connect_database()
    return list(df.major_name)

def LOWERCASE(entity):
    if not entity:
        return entity
    else:
        return entity.lower()

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
        message = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn."
        dispatcher.utter_message(text=message)
        return []

class ActionResponseMajorInfo(Action):

    def name(self) -> Text:
        return "action_response_major_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            AllSlotsReset()
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            info = major_info[major_name]
            dispatcher.utter_message(text=str(info))
        return []

def get_type_edu(major_name):
    df = connect_database()
    type_edu_info = df[df['major_name'] == major_name]
    output = type_edu_info['type_edu'].iloc[0]
    return output.replace('@',', ')

class ActionResponseMajorTypeEdu(Action):

    def name(self) -> Text:
        return "action_response_major_type_edu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            result = get_type_edu(major_name)
            dispatcher.utter_message(
                text=f"Ngành {major_name} đào tạo những hệ "+ result)
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
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            result = get_major_point(major_name)
            dispatcher.utter_message(
                text=f"Hiện tại điểm sàn của ngành {major_name} là "+result)
        return []

def get_career(major_name):
    df = connect_database()
    career_info = df[df['major_name'] == major_name]
    output = career_info['career'].iloc[0]
    return str(output.replace('@',', '))

class ActionResponseMajorCareer(Action):

    def name(self) -> Text:
        return "action_response_major_career"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            result = get_career(major_name)
            dispatcher.utter_message(
                text=f"Cơ hội việc làm của ngành {major_name} là "+result)
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
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            result = get_major_tuition(major_name)
            dispatcher.utter_message(
                text=f"Học phí của ngành {major_name} là "+result)
        return []


def get_subject_group(major_name):
    df = connect_database()
    subject_group_info = df[df['major_name'] == major_name]
    output = subject_group_info['subject_group'].iloc[0]
    return str(output.replace('@',', '))
class ActionResponseSubjectGroup(Action):

    def name(self) -> Text:
        return "action_response_major_subject_group"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            result = get_subject_group(major_name)
            dispatcher.utter_message(
                text=f"Ngành {major_name} tuyển sinh các khối "+result)
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
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu, hãy cho tôi một trường hợp cụ thể")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
            return [SlotSet("major_name", None)]
        else:
            result=get_major_criteria(major_name)
            dispatcher.utter_message(
                text=f"Năm 2022 ngành {major_name} dự kiến tuyển sinh khoảng "+result+" sinh viên")
        return []