import re
import os


class ReutersDoc:

    def __init__(self, attributes_data: str, tagged_data: str):
        self.attributes_data = attributes_data.strip()
        self.tagged_data = tagged_data

    def get_attributes_dictionary(self):
        attribute_dictionary = dict()
        for attribute in self.attributes_data.split(' '):
            attribute_data = attribute.split('=')
            attribute_name = attribute_data[0]
            attribute_value = attribute_data[1]
            attribute_dictionary[attribute_name] = attribute_value
        return attribute_dictionary

    def get_topics(self):
        topics = list()
        topics_tag = re.search(r'(?:<TOPICS>)(.*?)(?:</TOPICS>)', self.tagged_data)
        if topics_tag:
            d_tags = re.findall(r'<D>(.*?)</D>', topics_tag.groups()[0])
            if d_tags:
                for d_tag in d_tags:
                    topics.append(d_tag)
        return topics

    def get_title(self):
        title_tag = re.search(r'(?:<TITLE>)(.*?)(?:</TITLE>)', self.tagged_data)
        if title_tag:
            return title_tag.groups()[0]
        return ''

    def get_article_content(self):
        content_tag = re.search(r'(?:<BODY>)(.*?)(?:</BODY>)', self.tagged_data)
        if content_tag:
            return content_tag.groups()[0]
        return ''


def read_data(data_folder_path):
    data = []
    if os.path.isdir(data_folder_path):
        for filepath in os.listdir(data_folder_path):
            filename, file_extension = os.path.splitext(filepath)
            if file_extension == '.sgm':
                with open(os.path.join(data_folder_path, filepath), 'r') as file:
                    file_data = file.read()
                    file_data = re.sub(r'\n', '', file_data)
                    reuters_tags = re.findall(r'<REUTERS(.*?)>(.*?)</REUTERS>', file_data)
                    for attr_data, tag_data in reuters_tags:
                        article = dict()
                        doc = ReutersDoc(attr_data, tag_data)
                        attributes = doc.get_attributes_dictionary()
                        content = doc.get_article_content()
                        title = doc.get_title()
                        topics = doc.get_topics()
                        article.update(attributes)
                        article['content'] = content
                        article['title'] = title
                        article['topics_list'] = topics
                        data.append(article)
    return data


if __name__ == '__main__':
    for doc in read_data(os.path.join(os.getcwd(), 'data', 'reuters')):
        print(doc)
