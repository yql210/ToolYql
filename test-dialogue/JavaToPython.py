import socketserver

class myTCPhandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024).decode('UTF-8', 'ignore').strip()
            if not self.data : break
            print(self.data)

            # a = IntToOut.dialog(self.data)
            a = "机器人回复：" + self.data

            print(a)
            self.data = a
            self.feedback_data =(self.data).encode("utf8")
            print("发送成功")
            self.request.sendall(self.feedback_data)

host = '127.0.0.1'
port = 9007
server = socketserver.ThreadingTCPServer((host,port),myTCPhandler)
server.serve_forever()
