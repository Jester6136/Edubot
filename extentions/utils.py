import random

def RANDOM(list):
    return random.choice(list)

def response_list_product(list):
    return '\n'.join('- {}'.format(item) for item in list)

def convert_to_float(point):
    try:
        result = float(point)
    except ValueError:
        return False
    return result


def LOWERCASE(entity):
    if not entity:
        return entity
    else:
        return entity.lower()


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
                    "kỹ thuật điều khiển và tự động hóa": ["kỹ thuật điều khiển và tự động hóa",'ky thuat dieu khien va tu dong hoa', 'điều khiển tự động hóa', 'đktđh', 'ĐKTĐH', 'dktdh',
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

