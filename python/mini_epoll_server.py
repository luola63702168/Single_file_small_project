import socket, re, gevent
import select
from gevent import monkey


def service_client(client_socket,client_request):

    client_request_lines = client_request.splitlines()  
    print(">>" * 20)
    print(client_request_lines)

    # GET /index.html HTTP/1.1
    ret = re.match(r"[^/]+(/[^ ]*)", client_request_lines[0])
    file_name = "" 
    if ret:
        file_name = ret.group(1)
        if file_name == "/":
            file_name = "/index.html"
    try:
        f = open("./html" + file_name, "rb")
        html_content = f.read()
        f.close()

        response_body = html_content
        response_header = "HTTP/1.1 200 OK\r\n" 
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"
        response = response_header.encode("gbk")+response_body
        client_socket.send(response)

    except Exception as a:
        f = open("./html/" + "404.html", "rb")
        html_content = f.read()
        f.close()
        
        response_body = html_content
        response_header = "HTTP/1.1 200 OK\r\n"  
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"
        response = response_header.encode("gbk") + response_body
        client_socket.send(response)

    pass


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind(("192.168.233.1", 7890))
    tcp_socket.listen(128)
    tcp_socket.setblocking(False)

    epl = select.epoll()
    epl.register(tcp_socket.fileno(),select.EPOLLIN)
    fd_event_dict = dict()
    while True:
        fd_event_list = epl.poll()  
        for fd, event in fd_event_list:  
            if fd == tcp_socket.fileno():
                client_socket, client_addr = tcp_socket.accept()
                epl.register(client_socket.fileno(), select.EPOLLIN) 
                fd_event_dict[client_socket.fileno()] = client_socket
            elif event == select.EPOLLIN: 
                recv_data = fd_event_dict[fd].recv(1024).decode("gbk")
                if recv_data:
                    service_client(fd_event_dict[fd], recv_data)  
                else:
                    fd_event_dict[fd].close()
                    epl.unregister(fd)
                    del fd_event_dict[fd]

    tcp_socket.close()
    pass


if __name__ == '__main__':
    main()

# 项目需求：浏览器作为客户端发送请求，服务器接收并处理返回对应的数据–也就是html文档。

