

class Board(object):
    def __init__(self):
        self._boardId = None
        self._boardName = None
        self._userId = None


    @property
    def boardId(self):
        return self._boardId

    @property
    def boardName(self):
        return self._boardName

    @property
    def userId(self):
        return self._userId

    @boardId.setter
    def x(self, value):
        self._boardId = value

    @boardName.setter
    def x(self, value):
        self._boardName = value


    @userId.setter
    def x(self, value):
        self._userId = value

    @boardId.deleter
    def x(self):
        del self._boardId

    @boardName.deleter
    def x(self):
        del self._boardName

    @userId.deleter
    def x(self):
        del self._userId
