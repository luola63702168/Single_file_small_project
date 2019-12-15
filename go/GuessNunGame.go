package main

import (
	"fmt"
	"math/rand"
	"time"
)

func CreateNum(numPon *int) {
	rand.Seed(time.Now().UnixNano())
	var num int
	for {
		num = rand.Intn(10000)
		if num > 999 {
			break
		}
	}
	*numPon = num
}

func GetNum(s []int, num int) {
	s[0] = num / 1000 
	s[1] = num % 1000 / 100
	s[2] = num % 100 / 10
	s[3] = num % 10
}

func OnGame(randSlice []int) {
	var num int
	keySlice := make([]int, 4)
	for {
		for {
			fmt.Printf("请输入一个四位数：")
			_, _ = fmt.Scan(&num) 
			if 999 < num && num < 10000 {
				break
			}
			fmt.Println("输入的数不符合要求")
		}
		GetNum(keySlice, num)
		n := 0
		for i := 0; i < 4; i++ {
			if keySlice[i] > randSlice[i] {
				fmt.Printf("第%d位大了一点\n", i+1)
			} else if keySlice[i] < randSlice[i] {
				fmt.Printf("第%d位小了一点\n", i+1)
			} else {
				fmt.Printf("第%d位猜对了\n", i+1)
				n++
			}
		}
		if n == 4 {
			fmt.Println("全部猜对啦")
			break
		}

	}

}

func main() {
	var randNum int

	//产生一个4位的随机数
	CreateNum(&randNum)

	//用切片保存每一位数
	randSlice := make([]int, 4)
	GetNum(randSlice, randNum)

	//开始游戏
	OnGame(randSlice)

}


//请输入一个四位数：1234
//第1位小了一点
//第2位小了一点
//第3位大了一点
//第4位小了一点
//请输入一个四位数：2325
//第1位小了一点
//第2位猜对了
//第3位大了一点
//第4位小了一点
//请输入一个四位数：3316
//第1位猜对了
//第2位猜对了
//第3位猜对了
//第4位小了一点
//请输入一个四位数：3317
//第1位猜对了
//第2位猜对了
//第3位猜对了
//第4位小了一点
//请输入一个四位数：3318
//第1位猜对了
//第2位猜对了
//第3位猜对了
//第4位猜对了
//全部猜对啦