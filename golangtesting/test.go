package main

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"time"
)

func main() {
	// Set the log output to a file
	logFile, err := os.OpenFile("errors.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer logFile.Close()
	log.SetOutput(logFile)

	// Get the current working directory
	wd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}

	// Set the directory path where the JSON files are located
	dirPath := wd

	// Set the output directory path for the hashed files
	outputDir := wd

	// Get the current date and time
	now := time.Now()

	// Format the date and time according to the naming convention
	fileName := fmt.Sprintf("%s%d%d%d.json", now.Weekday().String(), now.Day(), now.Month(), now.Year()%100)

	// Open the JSON file
	file, err := os.Open(filepath.Join(dirPath, fileName))
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Create a new SHA-256 hash
	hash := sha256.New()

	// Read the JSON file and hash its contents
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

	// Get the list of .sha256 files in the directory
	files, err := filepath.Glob(filepath.Join(outputDir, "*.sha256"))
	if err != nil {
		log.Fatal(err)
	}

	// Extract the numbers from the file names
	numbers := make([]int, 0, len(files))
	for _, file := range files {
		base := filepath.Base(file)
		ext := filepath.Ext(base)
		numStr := strings.TrimSuffix(base, ext)
		num, err := strconv.Atoi(numStr)
		if err != nil {
			log.Fatal(err)
		}
		numbers = append(numbers, num)
	}

	// Sort the numbers in ascending order
	sort.Ints(numbers)

	// Get the maximum number
	maxNum := numbers[len(numbers)-1]

	// Use the maximum number as the limit for the naming format
	for i := 1; i <= maxNum; i++ {
		fileName := fmt.Sprintf("%d.sha256", i)
		log.Printf("Hashed file %s and saved to %s\n", fileName, outputFile.Name())
	}
}