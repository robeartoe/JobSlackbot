package main

import "github.com/gofiber/fiber"

func main() {
	app := fiber.New()

	app.Get("/test", func(c *fiber.Ctx) {
		c.Send("Hello, World!")
	})

	app.Static("/", "./public")
	app.Listen("localhost:3000")
}
