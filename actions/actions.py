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

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

DB_PATH = 'convert/entities.csv'

major_info = {
'kỹ thuật dệt':'Ngành Kỹ thuật dệt dành cho các sinh viên yêu thích kỹ thuật tạo sợi vải phục vụ cho may mặc, công nghiệp và các lĩnh vực khác. Chương trình học bao gồm các kiến thức chuyên sâu về vật liệu dệt, kỹ thuật tạo sợi, vải, in nhuộm hoàn tất, quản lý điều hành sản xuất sợi dệt nhuộm và thiết bị dệt. Ngoài ra, chương trình còn có các môn tự chọn về quản lý sản xuất hiện đại, các vấn đề thời sự trong ngành dệt may như sinh thái, môi trường và các kỹ thuật vật liệu hiệu năng cao, kỹ thuật dệt tiên tiến, ứng dụng tin học trong thiết kế và vận hành công nghiệp dệt.',
'kỹ thuật điện':'Ngành Kỹ thuật điện dành cho các sinh viên có sở thích liên quan đến điện năng. Chương trình bao gồm các môn học cốt lõi cần thiết về kỹ thuật điện – điện tử nói chung, và kỹ thuật điện nói riêng, cùng với nhiều môn học lựa chọn về thiết bị điện, điện tử công suất, nhà máy điện, mạng điện, hệ thống điện, và năng lượng tái tạo.',
'kỹ thuật hóa học':'Chương trình bao gồm các môn cốt lõi cần thiết về kỹ thuật hóa học và nhiều môn lựa chọn về công nghệ chuyên ngành. Ngoài ra, chương trình được gắn kết với chương trình đào tạo thạc sỹ/tiến sỹ ngành Kỹ thuật Hóa học tại trường đại học Bách Khoa TP.HCM',
'kỹ thuật môi trường':'Chương trình đào tạo (CTĐT) ngành Kỹ thuật Môi trường (KTMT) bao gồm cả môn học về kiến thức và kỹ năng. Sinh viên ngành KTMT được đào tạo và có đủ năng lực về kiến thức và kỹ năng phục vụ',
'kỹ thuật hàng không':'Ngành Kỹ Thuật Hàng Không (KTHK) dành cho các sinh viên có đam mê về máy bay và các phương tiện bay. Chương trình bao gồm các nhóm môn cốt lõi cần thiết về nền tảng của kỹ thuật hàng không như Khí Động Lực Học, Cơ học bay và điều khiển bay, Kết cấu hàng không, Hệ thống lực đẩy, Thiết kế và bảo dưỡng máy bay.',
'quản lý công nghiệp':'Chương trình đào tạo Cử nhân ngành Quản lý Công nghiệp nhằm cung ứng cho xã hội đội ngũ lao động có tiềm năng làm các nhà quản trị trong các công ty và tổ chức thuộc các ngành khác nhau, bao gồm cả sản xuất và dịch vụ.',
'công nghệ may':'Ngành Công nghệ may dành cho các sinh viên có sở thích và năng khiếu về kỹ thuật may công nghiệp và thời trang. Chương trình học bao gồm các kiến thức chuyên sâu về kỹ thuật may cơ bản và nâng cao, thiết bị may, mỹ thuật trang phục, quản lý sản xuất trong dây chuyền may công nghiệp hiện đại, ứng dụng tin học trong thiết kế và vận hành công nghiệp may.',
'công nghệ thực phẩm':'Chương trình bao gồm các môn học cốt lõi về kỹ thuật, công nghệ, khoa học thực phẩm và nhiều môn lựa chọn về công nghệ chế biến các sản phẩm thực phẩm như: sữa và sản phẩm từ sữa (phô mai, kem…), đường và bánh kẹo, trà – cà phê – cacao, thịt và các sản phẩm từ thịt (xúc xích, đồ hộp, paté…), sản phẩm từ thủy sản, dầu béo,…',
'kỹ thuật cơ khí':'Chương trình đào tạo Kỹ sư Cơ khí, được xây dựng theo hướng kỹ thuật, đào tạo kỹ sư cơ khí có năng lực chuyên môn để giải quyết những vấn đề liên quan đến thiết kế, chế tạo và vận hành các hệ thống sản xuất công nghiệp, có khả năng thích nghi và áp dụng các công nghệ tiên tiến của khu vực và thế giới nhằm phục vụ sự nghiệp công nghiệp hóa và hiện đại hóa đất nước; có phẩm chất chính trị, đạo đức và sức khoẻ tốt.',
'công nghệ sinh học':'Chương trình Công nghệ Sinh học dành cho các sinh viên yêu thích khoa học sự sống và quan tâm đến việc ứng dụng cũng như cải tạo các quy luật sinh học trong tự nhiên để tạo ra những sản phẩm có ích trong cuộc sống. Chương trình bao gồm các môn học cơ bản nhằm cung cấp cho sinh viên những kiến thức về khoa học tự nhiên, ngoại ngữ, những kiến thức cần thiết về chính trị, kinh tế, văn hóa, xã hội, ngoại ngữ, cũng như các môn học cơ sở ngành và chuyên ngành.',
'công nghệ kỹ thuật vật liệu xây dựng':'Chương trình đào tạo chuyên ngành Vật liệu Xây dựng dành cho những sinh viên có sở thích và đam mê về nghiên cứu chế tạo, quản lý kỹ thuật và công nghệ sản xuất các sản phẩm Vật liệu Xây dựng phục vụ cho công nghiệp xây dựng công trình dân dụng công nghiệp cũng như cơ sở hạ tầng.',
'logistics và quản lý chuỗi cung ứng':'Ngành Logistics và Quản lý chuỗi cung ứng trang bị cho người học đầy đủ kiến thức, kỹ năng chuyên môn và thái độ chuyên nghiệp làm nền tảng vững chắc cho sự thành công của kỹ sư Logistics và Quản lý Chuỗi cung ứng tại các doanh nghiệp.',
'kỹ thuật xây dựng công trình thủy':'Chuyên ngành Thủy lợi – Thủy điện thuộc ngành Kỹ thuật Xây dựng dành cho các sinh viên có sở thích về thiết kế xây dựng các công trình thủy lợi (bao gồm các công trình bảo vệ bờ sông, hồ chứa thủy lợi, hệ thống tưới), nhà máy thủy điện.',
'kỹ thuật hệ thống công nghiệp':'Chương trình đào tạo trang bị các kiến thức quản lý và điều hành hệ thống sản xuất hay dịch vụ, quản lý vật tư và hoạch định tồn kho, các kỹ thuật tối ưu hóa nguồn lực sản xuất, kỹ thuật hỗ trợ ra quyết định, quản lý và kiểm soát chất lượng, logistics và chuỗi cung ứng, kỹ thuật điều độ nguồn lực, thiết kế hệ thống thông tin, hay cách thức thiết kế và áp dụng hệ thống sản xuất tinh gọn cho tổ chức, …và nhiều kiến thức quan trọng khác rất cần thiết cho bất kỳ tổ chức sản xuất hay dịch vụ nào.',
'khoa học máy tính':'Ngành Khoa học Máy tính thuộc nhóm ngành Máy tính và Công nghệ thông tin. Mục tiêu của chương trình ngành Khoa học Máy tính là đào tạo ra những kỹ sư có chất lượng cao, có khả năng thiết kế, xây dựng và triển khai những hệ thống phần mềm đáp ứng nhu cầu trong nước và quốc tế. Kỹ sư tốt nghiệp ngành Khoa học Máy tính cũng được trang bị những kiến thức cần thiết để có thể học tiếp cao học và tiến sỹ trong lĩnh vực Máy tính và Công nghệ thông tin.',
'vật lý kỹ thuật':'Vật lý kỹ thuật là ngành đào tạo mang tính liên ngành, ứng dụng các nguyên lý vật lý và toán học để phân tích và giải quyết các vấn đề kỹ thuật và ứng dụng liên ngành. Mục tiêu tổng quát của ngành là đào tạo kỹ sư Vật lý Kỹ thuật có năng lực chuyên môn, được trang bị các kiến thức cơ sở vững vàng, có khả năng lãnh đạo, sáng tạo và khả năng tự học suốt đời trong lĩnh vực Vật lý kỹ thuật, đáp ứng nhu cầu lao động có trình độ kỹ thuật cao của đất nước. ',
'quản lý tài nguyên môi trường':'Sinh viên ngành Quản lý Tài nguyên và Môi trường (TNMT) được trang bị các kiến thức và kỹ năng về quản lý môi trường và tài nguyên bao gồm: Quản lý môi trường đô thị, khu công nghiệp và nông thôn, quản lý an toàn-sức khỏe-môi trường (HSE) tại các nhà máy/xí nghiệp và quản lý tài nguyên thiên nhiên (đất, nước, rừng, đới bờ)',
'kỹ thuật máy tính':'Ngành Kỹ thuật Máy tính thuộc nhóm ngành Máy tính và Công nghệ thông tin. Mục tiêu của chương trình ngành Kỹ thuật Máy tính là đào tạo ra những kỹ sư có chất lượng cao, có khả năng thiết kế, xây dựng và triển khai những hệ thống phần mềm và phần cứng cho máy tính và các thiết bị điều khiển nhằm đáp ứng nhu cầu trong nước và quốc tế.',
'công nghệ kỹ thuật ô tô':'Ngành Công nghệ Kỹ thuật Ô tô đào tạo kỹ sư có kiến thức cơ bản về Toán học, Khoa học tự nhiên và Kỹ thuật cơ sở đáp ứng việc tiếp thu các kiến thức chuyên ngành, cũng như có khả năng tự học nâng cao trình độ chuyên môn.',
'kỹ thuật điện tử viễn thông':'Ngành kỹ thuật điện tử-viễn thông dành cho sinh viên có sở thích và đam mê làm việc trong lĩnh vực công nghệ viễn thông và thông tin, vi mạch, bán dẫn, hệ thống nhúng và hệ thống điện tử ứng dụng, xử lý tín hiệu âm thanh, hình ảnh và đa phương tiện.',
'kỹ thuật vật liệu':'Kỹ sư Kỹ thuật vật liệu được đào tạo theo hướng ngành rộng. Kỹ sư Kỹ thuật vật liệu được trang bị đủ những kiến thức cơ bản và cơ sở khoa học của ngành Kỹ thuật Vật liệu để có thể hiểu biết nền tảng chung các nhóm vật liệu chính như Kim loại, Ceramic, Polyme, Compozit và các vật liệu tiên tiến như vật liệu bán dẫn, vật liệu siêu dẫn, vật liệu y sinh, vật liệu nano… từ đó có thể nắm bắt được mối quan hệ giữa cấu trúc và tính chất của vật liệu.',
'kiến trúc':'Ngành Kiến trúc dành cho các thí sinh có khả năng tư duy chiến lược (giỏi toán), năng khiếu nghệ thuật (hội họa, bố cục tạo hình), có tìm hiểu và đam mê Kiến trúc…',
'kỹ thuật nhiệt':'Sinh viên tốt nghiệp chuyên ngành Kỹ thuật nhiệt lạnh có thể tính toán thiết kế được các hệ thống nhiệt công nghiệp, nhiệt điện, hệ thống sấy, hệ thống lạnh công nghiệp, hệ thống điều hòa không khí trung tâm, các hệ thống sử dụng năng lượng tái tạo (mặt trời, gió), đưa ra các giải pháp sử dụng năng lượng hiệu quả và tiết kiệm trong các hệ thống đã thiết kế.',
'kỹ thuật địa chất':'Ngành KT Địa chất có 3 chuyên ngành: Địa kỹ thuật, Địa chất khoáng sản, Địa chấtmôi trường.\nNăm thứ nhất, CTĐT cung cấp một khối lượng kiến thức nền tảng cốt yếu đối với một kỹ sư (theo chuẩn mực chung của toàn trường Đại học Bách Khoa – ĐHQG HCM).',
'kỹ thuật tàu thủy':'Sinh viên tốt nghiệp từ chương trình Kỹ thuật Tàu Thủy có được sự giáo dục khoa học và nghề nghiệp (kỹ thuật và công nghệ), cho phép họ có thể thành công vởi công việc của người kỹ sư nói chung và nhất là trong ngành Kỹ thuật (lãnh vực) Tàu Thủy.',
'kỹ thuật trắc địa bản đồ':'Ngành Kỹ thuật Trắc địa – Bản đồ bao gồm Khoa học và công nghệ về việc thu thập, phân tích và biễu diễn các thông tin không gian (dựa trên Trái đất). Nó bao gồm những ứng dụng thú vị như định vị vệ tinh, viễn thám, trắc địa, địa chính và hệ thông tin địa lý.',
'kỹ thuật xây dựng cơ sở hạ tầng':'Ngành Kỹ thuật Cơ sở hạ tầng thuộc nhóm ngành Kỹ thuật Xây dựng dành cho các sinh viên có sở thích về thiết kế san nền, giao thông và hệ thống cấp thoát nước cho các dự án quy hoạch khu dân cư và hệ thống cấp thoát nước cho các công trình dân dụng – công nghiệp và nhà cao tầng.',
'cơ kỹ thuật':'Ngành Cơ Kỹ thuật dành cho sinh viên quan tâm đến lĩnh vực tính toán mô phỏng, đo lường, điều khiển các kết cấu cơ học (máy cơ khí, công trình xây dựng, phương tiện giao thông, thiết bị công nghiệp, y tế, quân sự, …) bằng cách lập trình hoặc sử dụng các chương trình ứng dụng máy tính, kết hợp thực nghiệm và chế tạo máy điều khiển chương trình số.',
'kỹ thuật cơ điện tử':'',
'kỹ thuật xây dựng công trình giao thông':'Ngành Kỹ Thuật Xây Dựng Công Trình Giao Thông là bộ phận quan trọng của nền kinh tế. Xã hội càng phát triển thì nhu cầu về xây dựng các Công Trình Giao Thông (cầu, đường, đường cao tốc, đường hầm, sân bay …) ngày càng lớn.',
'kỹ thuật dầu khí':'Chương trình đào tạo kỹ sư dầu khí là đào tạo kỹ sư có trách nhiệm chuyên môn, đạo đức nghề nghiệp, có tinh thần trách nhiệm với công việc và có khả năng:\nNắm bắt được những kiến thức và yêu cầu cơ bản của một trí thức trẻ trong cộng đồng xã hội và những kiến thức của một kỹ sư dầu khí.\nTư duy và tiếp cận các vấn đề của ngành dầu khí, khả năng tự nghiên cứu tiếp thu những kiến thức chuyên môn.',
'kỹ thuật công trình xây dựng':'Ngành Kỹ Thuật Công trình Xây Dựng dành cho các sinh viên có sở thích về các công trình xây dựng nói chung và các công trình phục vụ mục đích sử dụng trong dân dụng cũng như trong công nghiệp nói riêng. Chương trình bao gồm các môn cốt lõi cần thiết về Toán học, Vật Lý cơ học và nhiều môn chuyên ngành về kết cấu và nền móng công trình.',
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


class ActionResponseMajorInfo(Action):

    def name(self) -> Text:
        return "action_response_major_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        major_name = tracker.get_slot("major_name")
        major_name = LOWERCASE(major_name)
        if not major_name:
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
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
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
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
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
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
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
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
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
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
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
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
            dispatcher.utter_message(text="Tôi không hiểu!")
        elif(major_name not in list_major_name):
            dispatcher.utter_message(text="Trường không đào tạo ngành này!\nBạn hãy nhập ngành khác <3")
        else:
            result=get_major_criteria(major_name)
            dispatcher.utter_message(
                text=f"Năm 2022 ngành {major_name} dự kiến tuyển sinh khoảng "+result+" sinh viên")
        return []