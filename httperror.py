# encoding: UTF-8

class HttpError(Exception):


    def __init__(self, params):
        self.message = params
    
    def __str__(self):
        return 'HttpError'
    