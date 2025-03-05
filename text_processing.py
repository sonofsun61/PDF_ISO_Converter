import re


class TextProcessing:
    @staticmethod
    def extract_columns(file, page_num):
        page = file.load_page(page_num)
        text_instance = page.get_text('dict')['blocks']
        id, num_columns, headers_coords, used_headers = TextProcessing.extract_id_and_headers(text_instance)
        columns = {i: [] for i in range(num_columns)}
        no_coords = None
        flag = False
        words_to_remove = [
            'PIPE', 'PIPES', 'FITTINGS', 'FLANGES', 'GASKETS', 'BOLTS',
            'VALVES / IN-LINE ITEMS', 'PT', 'INSTRUMENTS',
            'ОПИСАНИЕ КОМПОНЕНТА', 'ИДЕНТ.КОД', 'КОЛ-ВО'
        ]
        for block in text_instance:
            if flag:
                break
            if block["type"] != 0 or "lines" not in block:
                continue
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    word = TextProcessing.replace_space(span['text'])
                    if word in used_headers:
                        continue
                    if 'SUPPORTS' in word or 'CUT LENGHT TABLE' in word:
                        flag = True
                        break
                    if word in words_to_remove:
                        continue
                    if word == 'NO':
                        no_coords = span['bbox'][0]
                    elif no_coords is not None and abs(span['bbox'][0] - no_coords) <= 0.1:
                        columns[1].append(word)
                    if headers_coords:
                        min_distance = float('inf')
                        closest_index = -1
                        for i, header_coord in enumerate(headers_coords):
                            distance = abs(span['bbox'][0] - header_coord)
                            if distance < min_distance:
                                min_distance = distance
                                closest_index = i
                        if closest_index != -1 and min_distance <= 3:
                            if re.match(r'^[A-Za-z0-9\s\-\.,/:(){}\[\]#&x°×="=*;]+$', word):
                                if closest_index + 1 == 3 and 'M' in word:
                                    word = word[:len(word) - 1]
                                    word = word.replace('.', ',')
                                    columns[closest_index + 1].append(word)
                                else:
                                    columns[closest_index + 1].append(word)
        return columns, id

    @staticmethod
    def replace_space(word):
        while word and word[-1] == ' ':
            word = word[:-1]
        while word and word[0] == ' ':
            word = word[1:]
        return word

    @staticmethod
    def extract_id_and_headers(text_instance):
        id = ''
        headers = ['COMPONENT DESCRIPTION', 'IDENT CODE', 'QTY']
        headers_coords = []
        used_headers = []
        for block in text_instance:
            if "lines" not in block or not block.get("lines"):
                continue
            for line in block['lines']:
                for span in line.get('spans', []):
                    word = TextProcessing.replace_space(span['text'])
                    if 'AGCC' in word:
                        id = word
                    elif word in headers and word not in used_headers:
                        used_headers.append(word)
                        headers_coords.append(span['bbox'][0])
        num_columns = len(used_headers) + 1
        return id, num_columns, headers_coords, used_headers

    @staticmethod
    def format_columns(columns, id):
        new_column_1 = []
        line = ''
        for item in columns[1]:
            if not item.isdigit():
                line += item
            else:
                if line:
                    new_column_1.append(line)
                line = ''
        if line:
            new_column_1.append(line)
        columns[1] = new_column_1
        columns[0] = [id] * len(new_column_1)
        return columns

    @staticmethod
    def insert_spaces(formatted_columns):
        append_indexes = []
        for i in range(len(formatted_columns)):
            for j in range(len(formatted_columns[i])):
                if formatted_columns[i][j] == '-':
                    append_indexes.append(j)
        for i in range(2, len(formatted_columns)):
            if len(formatted_columns[i]) < len(formatted_columns[1]):
                for index in append_indexes:
                    formatted_columns[i].insert(index, ' ')
        return formatted_columns