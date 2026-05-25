package main

import (
	"os"
	"sisi-interior-system/config"
	"sisi-interior-system/routes"

	"github.com/gin-gonic/gin"
)

func main() {
	//Init Connection ke DB
	config.ConnectDB()

	r := gin.Default()

	// Middleware CORS Manual
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")

		// Handle preflight request
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(200)
			return
		}

		c.Next()
	})

	r.Static("/uploads", "./uploads")

	//Set route yang akan digunakan pada System.
	routes.SetupRoutes(r)

	//Run pada port 8081
	port := os.Getenv("PORT")

	if port == "" {
		port = "8080"
	}

	r.Run(":" + port)
}
