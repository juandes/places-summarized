class summary(object):
    def __init__(self, result):
        self.next_page_token = result.get('next_page_token', '')