package main

import (
    "fmt"

	"github.com/gin-gonic/gin"
)

type fcHeader struct {
	FcRequestHeader string `header:"x-fc-invocation-target"`
	FcRequestId     string `header:"x-fc-request-id"`
}

type json struct {
	Key string `json:"key"`
}

func fcHome(context *gin.Context) {
	// See FC docs for all the HTTP headers: https://www.alibabacloud.com/help/doc-detail/132044.htm#common-headers
	fcRequestId := context.GetHeader("x-fc-request-id")
	context.JSON(200, gin.H{
		"message": fmt.Sprintf("Hello Gin, from FC HTTP function!\nPowerd by FunctionCompute custom-container runtime\nRequestID: %s\n", fcRequestId),
	})
}

func fcEventInitialize(context *gin.Context) {
	// See FC docs for all the HTTP headers: https://www.alibabacloud.com/help/doc-detail/132044.htm#common-headers
	fcRequestId := context.GetHeader("x-fc-request-id")
	fmt.Println("Initialize finished, request ID: " + fcRequestId)

	context.JSON(200, gin.H{
		"message": fmt.Sprintf("Hello Gin, from FC Event function initializer!\nPowerd by FunctionCompute custom-container runtime\nRequestID: %s\n", fcRequestId),
	})
}

func fcEventInvoke(context *gin.Context) {
	// See FC docs for all the HTTP headers: https://www.alibabacloud.com/help/doc-detail/132044.htm#common-headers
	fcRequestId := context.GetHeader("x-fc-request-id")
	fmt.Println("Invoke finished, request ID: " + fcRequestId)

	context.JSON(200, gin.H{
		"message": fmt.Sprintf("Hello Gin, from FC Event function!\nPowerd by FunctionCompute custom-container runtime\nRequestID: %s\n", fcRequestId),
	})
}

func main() {
	router := gin.Default()

	// FC HTTP trigger
	router.GET("/", fcHome)

	// FC Event trigger
	router.POST("/initialize", fcEventInitialize)
	router.POST("/invoke", fcEventInvoke)

	// listen and serve on port 9000
	router.Run(":9000")
}
