package main

import (
	"crypto/sha256"
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"time"
)

func main() {
	// Get the current working directory
	wd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}

	// Set the directory path where the CSV files are located
	dirPath := wd

	// Set the output directory path for the hashed files
	outputDir := wd

	// Get the current date and time
	now := time.Now()

	// Format the date and time according to the naming convention
	fileName := fmt.Sprintf("%s%d%d%d.csv", now.Weekday().String(), now.Day(), now.Month(), now.Year()%100)

	// Open the CSV file
	file, err := os.Open(filepath.Join(dirPath, fileName))
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Create a new SHA-256 hash
	hash := sha256.New()

	// Read the CSV file and hash its contents
	_, err = io.Copy(hash, file)
	if err != nil {
		log.Fatal(err)
	}

	// Get the hashed bytes
	hashedBytes := hash.Sum(nil)

	// Create a new file with the same name but with a `.sha256` extension
	outputFile, err := os.Create(filepath.Join(outputDir, fileName+".sha256"))
	if err != nil {
		log.Fatal(err)
	}
	defer outputFile.Close()

	// Write the hashed bytes to the output file
	_, err = outputFile.Write(hashedBytes)
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("Hashed file %s and saved to %s\n", fileName, outputFile.Name())
}th