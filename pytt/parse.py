import xml.etree.ElementTree as eTparse


class TTXMLParser:
    """XML parser for incoming data from SSU. Has methods to get infromation
    about department, group and each lesson. All the methods yields map to
    update method.
    """

    @staticmethod
    def parse_department_data(data):
        """Parse data about all the departments from SSU to save it
        in the database
        Paramereters:
            data (string): XML from SSU
        Return:
            yields (map str:str): name, tag, info and dtype
        """
        for dep in eTparse.fromstring(data.encode('utf-8')):
            yield {'name': dep.attrib['name'],
                   'tag': dep.attrib['id'],
                   'info': dep[0].text if not dep[0].text is None else '',
                   'dtype': int(dep.attrib['grid_type_id'])}

    @staticmethod
    def parse_group_data(data):
        """Parse data about groups of specific department
        Paramereters:
            data (string): XML from SSU
        Return:
            yields (map str:str): name, gfrom and gtype
        """
        for group in eTparse.fromstring(data.encode('utf-8')):
            form = group.attrib['edu_form']
            # do not add part-times
            if not form == '1':
                yield {'name': group.attrib['number_rus'].strip(),
                       'gform': form,
                       'gtype': group.attrib['grp_type']
                       }

    @staticmethod
    def parse_lesson_data(data, group):
        """Parse data about each group timetable via department page
        Paramereters:
            data (string): XML from SSU
            group (obj, models.Group): group object to get _exact_ group
        timetable
        Return:
            yields (map str:str): infromation to describe models.Cell and
        other Cell-related objects
        """
        grp_def = (group.name, group.gform, group.gtype)
        for group in eTparse.fromstring(data.encode('utf-8')):
            if grp_def == (group.attrib['number_rus'].strip(),
                           group.attrib['edu_form'],
                           group.attrib['grp_type']):
                for day in group:
                    for lessons in day:
                        for lesson in lessons:
                            dbegin = lesson.attrib['date_begin']
                            dend = lesson.attrib['date_end']
                            yield {'day': int(day.attrib['id']) - 1,
                                   'parity': lesson.attrib['weektype'],
                                   'begin_date': 0 if dbegin == '' else
                                   int(dbegin),
                                   'end_date': 0 if dend == '' else
                                   int(dend),
                                   'time':
                                       int(lesson.attrib['num']) - 1,
                                   'activity': lesson.attrib['type'],
                                   'name': lesson[0].text.strip(),
                                   'location': '' if lesson[1].text is None
                                               else lesson[1].text.strip(),
                                   'subgroup': '' if lesson[2].text is None
                                               else lesson[2].text.strip(),
                                   'teacher_name': ''
                                                   if lesson[3][3].text is None
                                                   else lesson[3][3].text
                                                   .strip(),
                                   'teacher_id': int(lesson[3].attrib['id'])
                                   }
