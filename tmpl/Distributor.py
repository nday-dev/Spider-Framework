#--coding:utf-8--
#Distributor
from multiprocessing import managers
import Queue

class BaseDistributor(object):
    """
    A dirtributor base on multiprocessing.managers.BaseManager and Queue.Queue
    Use two queues, one for server to client, the other for client to server.
    Automatically switch, or say change action accordingly (server or client, put or get)
    """
    class QueueManager(managers.BaseManager):
        pass

    def __init__(self, workerClass = None):
        """Use workerClass() to initialize a object"""
        self.workerClass = workerClass

    def __del__(self):
        """
        Autommatically call self.manager.shutdown()
        """
        try:
            self.status
        except AttributeError: # Start failed
            return

        if self.status == "started":
            self.manager.shutdown()

    def Start(self, address, authkey = None):
        """
        address is (str, int) of legal (IP address, port) if it is a client. For server IP is ''.
        authkey is a bit str.
        call only once for a object
        """
        if (address[0] == ''):
            self.Type = 'server'
            self._init = self._init_server()
        else:
            self.Type = 'client'
            self._init = self._init_client()

        next(self._init)
        self.manager = self.QueueManager(address = address, authkey = authkey)
        try:
            next(self._init) #Should receive "StopIteration" here.
        except StopIteration:
            pass
        self.TaskQueue = self.manager.GetTaskQueue()
        self.ResultQueue = self.manager.GetResultQueue()


    def _init_server(self):
        """
        Use yield to avoid code twice
        """
        self._TaskQueue = Queue.Queue()
        self._ResultQueue = Queue.Queue()
        yield
        self.QueueManager.register('GetTaskQueue', callable = lambda: self._TaskQueue)
        self.QueueManager.register('GetResultQueue', callable = lambda: self._ResultQueue)
        self.manager.start()
        self.status = "started"

    def _init_client(self):
        """
        Use yield to avoid code twice
        """
        self.QueueManager.register('GetTaskQueue')
        self.QueueManager.register('GetResultQueue')
        yield
        self.manager.connect()
        self.status = 'connected'

    def Put(self, item, block = True, timeout = None):
        """
        Pack self.ResultQueue.put(self, item, block = True, timeout = None)
        """
        if self.Type == 'server':
            return self.TaskQueue.put(item, block = True, timeout = None)
        else:
            return self.ResultQueue.put(item, block = True, timeout = None)

    def Get(self, block = True, timeout = None):
        """
        Pack self.TaskQueue.get(self, block = True, timeout = None)
        """
        if self.Type == 'server':
            return self.ResultQueue.get(block = True, timeout = None)
        else:
            return self.TaskQueue.get(block = True, timeout = None)

    def FlushPut(self):
        """
        Force flush the upload Queue (if using cache)
        """
        pass
    
    def FlushGet(self):
        """
        Force fluse the download Queu (if using cache)
        """
        pass

if __name__ == '__main__':
    raise EnvironmentError("DO NOT DIRECTLY RUN THIS TEMPLATE!")
