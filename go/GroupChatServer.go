package main

import (
	"fmt"
	"net"
	"strings"
	"time"
)

type Client struct {
	C    chan string // pipeline to send data
	Name string
	Addr string
}

//save online users. 
var onlineMap map[string]Client

var message = make(chan string)

func WriteMsgToClient(cli Client, conn net.Conn) {
	for msg := range cli.C {
		_, _ = conn.Write([]byte(msg + "\n"))
	}
}

func MakeMsg(cli Client, msg string) (buf string) {
	buf = "[" + cli.Addr + "]" + cli.Name + ": " + msg
	return
}

func HandleConn(conn net.Conn) {
	defer conn.Close()
	cliAddr := conn.RemoteAddr().String()
	cli := Client{make(chan string), cliAddr, cliAddr}
	onlineMap[cliAddr] = cli

	// Start a new association to send information to the current client
	go WriteMsgToClient(cli, conn)
	message <- MakeMsg(cli, "login")

	cli.C <- MakeMsg(cli, "i am here")

	// Record whether the other party voluntarily exits
	hasQuit := make(chan bool)
	// Whether the data of the opposite party is sent
	hasData := make(chan bool)
	// Open a new association to accept the data sent by users
	go func() {
		buf := make([]byte, 2048)
		for {
			n, err := conn.Read(buf) 
			fmt.Println(n)
			if n == 0 { 
				fmt.Println("此时n为0")
				hasQuit <- true
				fmt.Println("conn.Read err= ", err)
				return 
			}
			msg := string(buf[:n])
			if msg == "who" {
				_, _ = conn.Write([]byte("user list:\n"))
				for _, tmp := range onlineMap {
					userAddr := tmp.Addr + ":" + tmp.Name + "\n"
					_, _ = conn.Write([]byte(userAddr))

				}
			} else if len(msg) >= 8 && msg[:6] == "rename" {
				//rename
				newName := strings.Split(msg, "|")[1]
				cli.Name = newName
				onlineMap[cliAddr] = cli 
				_, _ = conn.Write([]byte("rename ok\n"))

			} else {
				message <- MakeMsg(cli, msg)
			}
			hasData <- true // Representative has data
		}

	}()

	// Disallow disconnection of server clients
	for {
		select {
		case <-hasQuit:
			delete(onlineMap, cliAddr)
			message <- MakeMsg(cli, "login out")
		case <-hasData:
		case <-time.After(30 * time.Second):
			delete(onlineMap, cliAddr)
			message <- MakeMsg(cli, "time out leave out")
			return 
		}
	}
}

func Manager() {
	onlineMap = make(map[string]Client)
	for {
		msg := <-message
		for _, cli := range onlineMap {
			cli.C <- msg
		}
	}
}

func main() {
	//listen
	lis, err := net.Listen("tcp", ":8888")
	if err != nil {
		fmt.Println("net.Listen err =", err)
		return
	}
	defer lis.Close()
	// new association,As soon as there is a message is coming,it will traverse the map and send the message.
	go Manager()
	// Master association, waiting for user link
	for {
		conn, err1 := lis.Accept()
		if err1 != nil {
			fmt.Println("is.Accept err1=", err1)
			continue
		}
		// Handle user links
		go HandleConn(conn)
	}
}
