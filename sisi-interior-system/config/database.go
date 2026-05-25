package config

import (
	"log"
	"os"
	"sisi-interior-system/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectDB() {

	dsn := os.Getenv("DATABASE_URL")

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Gagal koneksi database:", err)
	}
	// AUTO MIGRATE
	err = db.AutoMigrate(
		&models.Admin{},
		&models.Portfolio{},
		&models.Project{},
		&models.Estimasi{},
	)

	if err != nil {
		log.Fatal("Gagal migrate:", err)
	}
	DB = db
	DB = db
	log.Println("Database connected & migrated")
}
