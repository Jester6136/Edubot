import random

def RANDOM(list):
    return random.choice(list)

def response_list_product(list):
    return '\n'+'\n'.join('\t\t\t • {}'.format(item.capitalize()) for item in list)

def convert_to_float(point):
    try:
        result = float(point)
    except ValueError:
        return False
    return result


def LOWERCASE(entity:str):
    if not entity:
        return entity
    else:
        return entity.lower()


def UPPERCASE(entity:str):
    if not entity:
        return entity
    else:
        return entity.upper()

def look_up_in_domain(major_name):
    look_up_dict = {"khoa học máy tính": ['khoa học máy tính','khmt', 'KHMT', 'khoa hoc may tinh', 'Khoa hoc may tinh'],
                    "kỹ thuật điện": ["kỹ thuật điện",'ktđ', 'ktd', 'ky thuat dien', 'KTĐ', 'KTD'],
                    "kỹ thuật hóa học": ["kỹ thuật hóa học",'kthh', 'KTHH', 'ky thuat hoa hoc', 'Ky thuat hoa hoc'],
                    "kỹ thuật hàng không": ["kỹ thuật hàng không",'kthk', 'KTHK', 'ky thuat hang khong', 'Ky thuat hang khong'],
                    "công nghệ may": ["công nghệ may",'cnm', 'CNM', 'Cong nghe may', 'cong nghe may'],
                    "công nghệ sinh học": ["công nghệ sinh học",'cnsh', 'CNSH', 'Cong nghe sinh hoc', 'cong nghe sinh hoc'],
                    "logistics và quản lý chuỗi cung ứng": ["logistics và quản lý chuỗi cung ứng",'logistics', 'logistic', 'Logistics', 'Logistic'],
                    "kỹ thuật máy tính": ["kỹ thuật máy tính",'ktmt', 'KTMT', 'ky thuat may tinh', 'Ky thuat may tinh'],
                    "công nghệ kỹ thuật ô tô": ["công nghệ kỹ thuật ô tô",'ô tô', 'kỹ thuật ô tô', 'o to', 'ky thuat o to', 'Ô TÔ', 'Kỹ thuật ô tô'],
                    "kỹ thuật điện tử viễn thông": ["kỹ thuật điện tử viễn thông",'điện tử viễn thông', 'ĐTVT', 'đtvt', 'ky thuat dien tu vien thong', 'DTVT', 'dtvt'],
                    "kỹ thuật cơ điện tử": ["kỹ thuật cơ điện tử",'ky thuat co dien tu', 'co dien tu', 'cơ điện tử', 'cđt', 'cdt', 'CĐT', 'CDT'],
                    "kỹ thuật điều khiển và tự động hóa": ["tdh","tđh","TĐH","TDH","kỹ thuật điều khiển và tự động hóa",'ky thuat dieu khien va tu dong hoa', 'điều khiển tự động hóa', 'đktđh', 'ĐKTĐH', 'dktdh',
                                                           'DKTDH', 'tự động hóa', 'tu dong hoa']
                    }
    # count = 0
    if (major_name):
        for key in look_up_dict.keys():
            if major_name in look_up_dict[key]:
                return key
        return major_name
    else:
        return major_name

def look_up_subject_group(subject_group):
    look_up_dict = {
        "A00": ['A','A00','A0','a','a00','a0'],
        "A01": ['A1','A01','a1','a01'],
        "B00": ['B','B0','B00','b','b0','b00'],
        "D07": ['D','D7','D07','d','d7','d07'],
        }
    # count = 0
    if (subject_group):
        for key in look_up_dict.keys():
            if subject_group in look_up_dict[key]:
                return key
        return subject_group
    else:
        return subject_group